# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: cli.py
# Project: datamodel
# Author: Brian Cherinka
# Created: Friday, 7th May 2021 8:24:29 am
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Friday, 7th May 2021 8:24:29 am
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import os

import click
from datamodel.command import Install
from datamodel.generate import DataModel
from datamodel.validate import (check_products, validate_models, revalidate,
                                update_tree, update_datamodel_access)
from datamodel.io.move import dm_move, construct_new_path, dm_move_species
from datamodel.io.loaders import get_yaml_files
from datamodel import log

import cloup
from cloup import OptionGroup, option_group, option
from cloup.constraints import mutually_exclusive, If, all_or_none, RequireExactly, AcceptAtMost


@click.group(name='datamodel')
def cli():
    """ Command-line tool for handling SDSS datamodels """
    pass


data_grp = OptionGroup('Product Options', help='options for specifying a data product.')
rel_grp = OptionGroup("Release Options", help='options for specifying the release or environment.')
stb_grp = OptionGroup("Stub Options", help='options for writing out datamodel stubs.')

@cloup.command(short_help='Generate a datamodel file for a SDSS data product', show_constraints=True)
@option_group('Product Options', 'options for specifying a data product.',
    option('-n', '--filename', help='the name of a file on disk', type=click.Path(exists=True)),
    option('-f', '--file_species', help='unique name of the product file species'),
    option('-p', '--path', help='symbolic path to the file'),
    option('-l', '--location', help='symbolic location of the file'),
    option('-e', '--env_label', help='environment variable name of the root location'),
    option("-k", "--keywords", multiple=True, help="template variable keyword=value pair(s)"),
    option('-a', '--access_path_name', help='name of the sdss_access path, if different than file species'),
    option('-s', '--science_product', help='set product as a recommended science product', is_flag=True, default=False)
    )
@option_group('Release Options', 'options for specifying the release or environment.',
    option('-t', '--tree_ver', help='the SDSS tree configuration'),
    option('-r', '--release', help='the SDSS data release')
    )
@option_group('Stub Options', 'options for writing out datamodel stubs.',
    option('-F', '--force', help='force override of a stub cache', is_flag=True, default=False),
    option("-c", "--use-cache", help="specify an existing cached release to use", default=None),
    option('-h', "--hdus-only", help="set to True to only use the user descriptions/comments from the specified cached release", is_flag=True, default=False)
    )
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
@click.option("-w", "--with-git", help="set to use the auto git commit process", is_flag=True, default=False)
@cloup.constraint(AcceptAtMost(1) & mutually_exclusive, ['tree_ver', 'release'])
@cloup.constraint(all_or_none, ['location', 'env_label'])
@cloup.constraint(mutually_exclusive, ['path', 'location'])
@cloup.constraint(RequireExactly(1), ['filename', 'file_species'])
@cloup.constraint(If('file_species', then=RequireExactly(1)), ['path', 'location'])
def generate(filename, file_species, path, location, env_label, keywords, tree_ver, release,
             force, use_cache, hdus_only, verbose, with_git, access_path_name, science_product):
    """ Generate a datamodel file for a SDSS data product """

    # create a datamodel object
    dm = DataModel(tree_ver=tree_ver, file_spec=file_species,
                path=path, keywords=keywords,
                env_label=env_label, location=location,
                verbose=verbose, release=release,
                filename=filename, access_path_name=access_path_name,
                science_product=science_product)

    # write out all the datamodel stubs
    dm.write_stubs(force=force, use_cache_release=use_cache,
                full_cache=not hdus_only)

    # only run if we using the git commit option
    if with_git:
        # commit the stubs into git
        try:
            dm.commit_stubs()
        except RuntimeError as err:
            log.error(f'Could not commit stubs to git.  Check for errors and try again. Error - {err}')


cli.add_command(generate)


@cli.command(short_help='Install a user copy of the datamodel product at Utah')
@click.option('-b', '--branch', help='install a specific branch of the datamodel product', default='main')
@click.option('-F', '--force', help='force a (re)install of the datamodel product', is_flag=True, default=False)
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
@click.option('-d', '--debug', help='turn on debugging', is_flag=True, default=False)
@click.option('-t', '--test', help='test the install without installing', is_flag=True, default=False)
def install(branch: str, force: bool, verbose: bool, debug: bool, test: bool):
    """ Install the datamodel product at Utah """

    install = Install(branch=branch, force=force, verbose=verbose, debug=debug, test=test)
    install.set_directory()
    install.clone()
    install.checkout_branch()
    install.set_modulefile()
    install.done()


create_grp = OptionGroup('Create Options', help='options for creating a file from a designed datamodel.')

@cloup.command(short_help='Design a new datamodel for a new file', show_constraints=True)
@data_grp.option('-f', '--file_species', help='unique name of the product file species', required=True)
@data_grp.option('-p', '--path', help='symbolic path to the file')
@data_grp.option('-l', '--location', help='symbolic location of the file')
@data_grp.option('-e', '--env_label', help='environment variable name of the root location')
@create_grp.option('-c', '--create', help='create a file on disk from a designed datamodel', is_flag=True, default=False)
@create_grp.option("-k", "--keywords", multiple=True, help="optional keywords into DataModel.generate_designed_file")
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
@cloup.constraint(all_or_none, ['location', 'env_label'])
@cloup.constraint(mutually_exclusive, ['path', 'location'])
@cloup.constraint(If('file_species', then=RequireExactly(1)), ['path', 'location'])
@cloup.constraint(If('keywords', then=RequireExactly(1)), ['create'])
def design(file_species, path, location, env_label, verbose, create, keywords):
    """ Design a datamodel for a new file """

    # create a datamodel object
    dm = DataModel(file_spec=file_species, path=path, env_label=env_label, location=location,
                   verbose=verbose, release='WORK', design=True)

    # write out all the datamodel stubs
    dm.write_stubs()

    # sort out any keywords
    if keywords:
        kwargs = {k.split('=')[0]:k.split('=')[1] for k in keywords}

    # create a designed file if requested
    if create:
        dm.generate_designed_file(**kwargs)


cli.add_command(design)


@cloup.group(name='tree')
def tree():
    """ Interact with the SDSS tree product """


@tree.command('check', short_help='Check datamodel paths against tree')
@click.option('-r', '--release', help='the SDSS data release')
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
def check_paths(release: str, verbose: bool):
    """ Check the product path definitions are correct in tree """
    check_products(release, verbose=verbose)
    log.info('All products paths are correct in tree.')


@tree.command(short_help='Add datamodel paths to the tree')
@click.option('-r', '--release', help='the SDSS data release')
@click.option('-w', '--work-ver', help='the SDSS tree config work version, i.e. sdss5 or sdsswork')
@click.option('-b', '--branch', help='install a specific branch of the tree product', default='dm_update_tree')
@click.option('-l', '--local', help='use an existing local tree repo', is_flag=True, default=False)
@click.option('-t', '--test', help='test the update without performing write ops', is_flag=True, default=False)
@click.option('-s', '--skip-push', help='skips the git push step', is_flag=True, default=False)
@cloup.constraint(AcceptAtMost(1) & mutually_exclusive, ['work_ver', 'release'])
def add(release: str, work_ver: str, branch: str, local: bool, test: bool, skip_push: bool):
    """ Add new access paths into the tree git product """
    update_tree(release=release, work_ver=work_ver, branch=branch, local=local, test=test, skip_push=skip_push)


@tree.command(short_help='Update the datamodel stubs with new access paths', aliases=['updm', 'up', 'update'])
@click.option('-b', '--branch', help='install a specific branch of the datamodel product', default='dm_update_models')
@click.option('-t', '--test', help='test the update without performing write ops', is_flag=True, default=False)
@click.option('-c', '--commit-to-git', help='manually commit to git', is_flag=True, default=False)
def update_dm(branch: str, test: bool, commit_to_git: bool):
    """ Update datamodel stubs with new access paths  """
    update_datamodel_access(branch=branch, test=test, commit_to_git=commit_to_git)


cli.add_command(tree)


@click.group(name='validate')
def validate():
    """ Commands related to datamodel validation """

@validate.command('check', short_help='Check JSON datamodel validation.')
def check_models():
    """ Check that all YAML datamodel have corresponding JSON datamodels """

    validate_models()
    log.info('All YAML datamodels have validated JSON models.')


@validate.command(short_help='Revalidate a datamodel stub.')
@click.option('-f', '--file_species', help='unique name of the product file species', required=True)
@click.option('-r', '--release', help='the SDSS data release')
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
def redo(file_species: str, release: str, verbose: bool):
    """ Rewrite all datamodel stubs for a given file species  """

    revalidate(species=file_species, release=release, verbose=verbose)
    log.info(f'Regenerating datamodel stubs for {file_species}.')

cli.add_command(validate)


@cloup.command(short_help='Move a datamodel from one location to another')
@click.option('-s', '--file_species', help='unique name of the product file species', required=True)
@click.option('-f', '--from-release', help='the release to move from', required=True, default="WORK")
@click.option('-t', '--to-release', help='the release to move to', required=True)
@click.option('-p', '--to-path', help='the new abstract path')
@click.option('-e', '--to-envvar', help='the new envvar')
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
@click.option('-m', '--move', help='move the example file ', is_flag=True, default=True)
@click.option('-r', '--parent', help='move the example file parent directory ', is_flag=True, default=False)
@click.option('-l', '--symlink', help='create a symlink from the old to the new file', is_flag=True, default=True)
@click.option('-c', '--species', help='move an entire file species', is_flag=True, default=False)
@click.option('-n', '--test', help='test without moving', is_flag=True, default=False)
@cloup.constraint(mutually_exclusive, ['to_path', 'to_envvar'])
@cloup.constraint(If('file_species', then=RequireExactly(1)), ['to_path', 'to_envvar'])
def move(file_species: str, from_release: str, to_release: str,
         to_path: str = None, to_envvar: str = None, verbose: bool = None,
         move: bool = False, parent: bool = False, symlink: bool = False,
         species: bool = None, test: bool = None):
    """ Move a datamodel from a SANDBOX to a final location """

    # get the existing old datamodel
    olddm = DataModel.from_yaml(file_species, release=from_release, verbose=verbose)

    # construct the new path
    if to_path:
        new_path = to_path
    elif to_envvar:
        new_path = f'{to_envvar}/{olddm.path.split("/", 1)[-1]}'

    if move and species:
        # move all file species
        log.info(f'Moving all files from file species {file_species}.')
        dm_move_species(olddm.path, new_path, to_release, test=test)
    elif move:
        # get and move the file
        newfile = construct_new_path(new_path=new_path, release=to_release, kwargs=olddm.kwargs)
        log.info(f'Moving {file_species} to {newfile}.')
        if not test:
            dm_move(olddm.file, newfile, parent=parent, symlink=symlink)

    # get any access path name
    access_name = olddm._access_path_name or olddm.access[from_release].get("path_name", None)

    # write out the new datamodel
    newdm = DataModel(file_spec=olddm.file_species,
                      path=new_path,
                      keywords=olddm.keywords,
                      release=to_release, verbose=verbose, access_path_name=access_name)

    if not os.path.exists(newdm.file):
        log.error('New datamodel file does not exist at new location. Cannot write out stubs.')
        return

    # write out new stubs
    if not test:
        newdm.write_stubs(use_cache_release=from_release)


cli.add_command(move)

@cli.command(short_help='Update datamodels with new template content')
@click.option('-f', '--file_species', help='unique name of the product file species')
@click.option('-r', '--release', help='the SDSS data release', required=True, default='WORK')
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
def update(file_species: str, release: str, verbose: bool):
    """ Update existing datamodels with any new content added into the template """

    if file_species:
        files = [get_yaml_files(file_species)]
    else:
        files = get_yaml_files("products")

    for file in files:
        log.info(f"Updating datamodel {file.stem}.")
        try:
            dm = DataModel.from_yaml(file.stem, release=release, verbose=verbose)
        except Exception as e:
            log.error(f'DM update failed. Failed to instantiate datamodel {file.stem}.')
        else:
            try:
                dm.write_stubs()
            except Exception as e:
                log.error(f'DM update failed. Could not write stubs for {file.stem}. Error: {e}')



if __name__ == '__main__':
    cli()



