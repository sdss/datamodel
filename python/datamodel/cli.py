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

import click
from datamodel.command import Install
from datamodel.generate import DataModel
from datamodel.validate import check_products, validate_models, revalidate
from datamodel import log

import cloup
from cloup import OptionGroup
from cloup.constraints import mutually_exclusive, If, all_or_none, RequireExactly, AcceptAtMost


@click.group(name='datamodel')
def cli():
    """ Command-line tool for handling SDSS datamodels """
    pass


data_grp = OptionGroup('Product Options', help='options for specifying a data product.')
rel_grp = OptionGroup("Release Options", help='options for specifying the release or environment.')
stb_grp = OptionGroup("Stub Options", help='options for writing out datamodel stubs.')

@cloup.command(short_help='Generate a datamodel file for a SDSS data product', show_constraints=True)
@data_grp.option('-n', '--filename', help='the name of a file on disk', type=click.Path(exists=True))
@data_grp.option('-f', '--file_species', help='unique name of the product file species')
@data_grp.option('-p', '--path', help='symbolic path to the file')
@data_grp.option('-l', '--location', help='symbolic location of the file')
@data_grp.option('-e', '--env_label', help='environment variable name of the root location')
@data_grp.option("-k", "--keywords", multiple=True, help="template variable keyword=value pair(s)")
@data_grp.option('-a', '--access_path_name', help='name of the sdss_access path, if different than file species')
@rel_grp.option('-t', '--tree_ver', help='the SDSS tree configuration')
@rel_grp.option('-r', '--release', help='the SDSS data release')
@stb_grp.option('-F', '--force', help='force override of a stub cache', is_flag=True, default=False)
@stb_grp.option("-c", "--use-cache", help="specify an existing cached release to use", default=None)
@stb_grp.option('-h', "--hdus-only", help="set to True to only use the user descriptions/comments from the specified cached release", is_flag=True, default=False)
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
@click.option("-s", "--skip-git", help="skip the git commit process", is_flag=True, default=False)
@cloup.constraint(AcceptAtMost(1) & mutually_exclusive, ['tree_ver', 'release'])
@cloup.constraint(all_or_none, ['location', 'env_label'])
@cloup.constraint(mutually_exclusive, ['path', 'location'])
@cloup.constraint(RequireExactly(1), ['filename', 'file_species'])
@cloup.constraint(If('file_species', then=RequireExactly(1)), ['path', 'location'])
def generate(filename, file_species, path, location, env_label, keywords, tree_ver, release,
             force, use_cache, hdus_only, verbose, skip_git, access_path_name):
    """ Generate a datamodel file for a SDSS data product """

    # create a datamodel object
    dm = DataModel(tree_ver=tree_ver, file_spec=file_species,
                path=path, keywords=keywords,
                env_label=env_label, location=location,
                verbose=verbose, release=release,
                filename=filename, access_path_name=access_path_name)

    # write out all the datamodel stubs
    dm.write_stubs(force=force, use_cache_release=use_cache,
                full_cache=not hdus_only)

    # only run if we are not skipping the git commit stage
    if not skip_git:
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


@click.group(name='tree')
def tree():
    """ Interact with the SDSS tree product """


@tree.command('check', short_help='Check datamodel paths against tree')
@click.option('-r', '--release', help='the SDSS data release')
@click.option('-v', '--verbose', help='turn on verbosity', is_flag=True, default=False)
def check_paths(release: str, verbose: bool):
    """ Check the product path definitions are correct in tree """
    check_products(release, verbose=verbose)
    log.info('All products paths are correct in tree.')


# @tree.command(short_help='Add datamodel paths to the tree')
# def add(branch: str, force: bool, verbose: bool, debug: bool, test: bool):
#     """ Add new tree paths  """
#     pass


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


if __name__ == '__main__':
    cli()



