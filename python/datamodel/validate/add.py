# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import itertools
import tempfile
import shutil
from configparser import ConfigParser
from git import Repo, GitCommandError
from configobj import ConfigObj

from tree import Tree
from datamodel import log
from datamodel.generate import DataModel
from .check import yield_products


def get_new_products(release: str = None):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    release : str, optional
        _description_, by default None

    Yields
    ------
    _type_
        _description_
    """
    for product, data in yield_products(release=release):
        if not data:
            continue

        if not release:
            for rr, info in data.items():
                if info['in_sdss_access']:
                    continue
                #print(f'new product {product} with access {info["access_string"]}.')
                yield rr, info["access_string"]
        elif not data['in_sdss_access']:
            #print(f'new product {product} with access {data["access_string"]}.')
            yield release, data["access_string"]


def make_branch(repo: Repo, branch=None):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    repo : Repo
        _description_
    branch : _type_, optional
        _description_, by default None

    Returns
    -------
    _type_
        _description_
    """
    log.info('Setting up tree repo.')
    repo.git.checkout('master')
    repo.remotes.origin.fetch()
    repo.remotes.origin.pull()
    branch = branch or 'dm_update_tree'
    if branch in repo.branches:
        log.info(f'Checking out existing branch {branch}.')
        repo.git.checkout(branch)
    else:
        log.info(f'Creating new working branch {branch}.')
        repo.git.checkout('HEAD', b=branch)
    return repo


def clone_tree(branch: str = None, local: bool = None):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    branch : str, optional
        _description_, by default None
    local : bool, optional
        _description_, by default None

    Returns
    -------
    _type_
        _description_
    """
    treedir = os.getenv("TREE_DIR")
    if local and treedir:
        log.info(f'Using local tree repository at {treedir}')
        r = Repo(treedir)
        return make_branch(r, branch=branch)

    tmpdir = tempfile.TemporaryDirectory()
    log.info(f'Cloning tree repository at {tmpdir}')
    r = Repo.clone_from("https://github.com/sdss/tree", tmpdir)
    return make_branch(r, branch=branch)


def add_and_commit(repo: Repo, file: str, message: str = 'datamodel auto updating tree with new paths'):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    repo : Repo
        _description_
    file : str
        _description_
    message : str, optional
        _description_, by default 'datamodel auto updating tree with new paths'
    """
    repo.index.add(file)
    repo.index.commit(message)
    log.info(f'Committing changes to file {file}.')
    #repo.remotes.origin.push(repo.active_branch, set_upstream=True)
    #repo.remotes.origin.push(repo.active_branch, delete=True)

def pull_and_push(repo: Repo):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    repo : Repo
        _description_
    """
    if repo.active_branch.tracking_branch():
        repo.remotes.origin.pull()
    repo.remotes.origin.push(repo.active_branch, set_upstream=True)
    log.info('Pushing changes to origin.')


def update_tree(release: str = None, work_ver: str = None, branch: str = 'dm_update_tree',
                local: bool = None, test: bool = None, skip_push: bool = False):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    release : str, optional
        _description_, by default None
    work_ver : str, optional
        _description_, by default None
    branch : str, optional
        _description_, by default 'dm_update_tree'
    local : bool, optional
        _description_, by default None
    test : bool, optional
        _description_, by default None
    skip_push : bool, optional
        _description_, by default None
    """

    # clone the tree repo
    repo = clone_tree(branch=branch, local=local)

    # iterate over all the new products, grouped by release
    for rr, items in itertools.groupby(sorted(get_new_products(release=release)), key=lambda x: x[0]):
        # split the access path into a name and template
        paths = [p[1].replace(" = ", "=").split("=") for p in items]

        # set the tree config for the given release
        cfg = work_ver.lower() if work_ver and rr == 'WORK' else 'sdss5' if rr == 'WORK' else rr.lower()
        tree = Tree(cfg)

        # skip things if testing
        if test:
            log.info(f'Test mode: not writing to {cfg} tree.')
            log.info(f'Found new paths to add: {[i[0] for i in paths]}')
            continue

        # backup the existing file
        backup_cfg = tree.config_file.replace(f"{cfg}.cfg", f'{cfg}.cfg.backup')
        shutil.copy2(tree.config_file, backup_cfg)

        # update the config files with the new paths
        write_comments(tree.config_file, paths)

        # add and commit the files
        try:
            add_and_commit(repo, tree.config_file, message=f'datamodel auto updating {cfg} tree with new paths')
        except GitCommandError:
            # replace original file
            shutil.move(backup_cfg, tree.config_file)
        else:
            # remove the backup file
            os.remove(backup_cfg)

    # push the changes
    if not test and not skip_push:
        try:
            pull_and_push(repo)
        except GitCommandError:
            log.error('Failed to push changes to origin. Cleaning up and removing local branch.')
            repo.checkout('master')
            repo.delete_head(repo.heads[branch])


def write_no_comments(cfgfile: str, paths: list):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    cfgfile : str
        _description_
    paths : list
        _description_
    """
    # no comments
    cfg = ConfigParser()
    cfg.read(cfgfile)

    for name, template in paths:
        if name in cfg["PATHS"] and cfg["PATHS"][name] == template:
            log.info(f'Path {name} = {template} already exists in {cfgfile}.')
            continue
        cfg["PATHS"][name] = template

    with open(cfgfile, "w") as fp:
        cfg.write(fp)


def write_comments(cfgfile: str, paths: list):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    cfgfile : str
        _description_
    paths : list
        _description_
    """
    # preserve comments
    config = ConfigObj(cfgfile)

    for name, template in paths:
        if name in config["PATHS"] and config["PATHS"][name] == template:
            log.info(f'Path {name} = {template} already exists in {cfgfile}.')
            continue

        config["PATHS"][name] = template

    config.write()


def update_datamodel_access(test: bool = None):
    """_summary_

    _extended_summary_
    """
    # loop for new JSON datamodel products
    for release, access_string in get_new_products():

        if test:
            log.info('Test mode: not writing datamodel stubs.')

        # load the datamodel from the relevant YAML file
        species = access_string.split(' = ')[0]

        dm = DataModel.from_yaml(species, release)
        # if the access is updated, write out the stubs
        if dm.access[release]['in_sdss_access'] and not test:
            dm.write_stubs()

        # for WORK releases, the path could be in sdsswork or sdss5.  If sdsswork above fails
        # then try sdss5.
        if release == 'WORK' and not dm.access[release]['in_sdss_access']:
            dm = DataModel.from_yaml(species, tree_ver="sdss5")
            if dm.access[release]['in_sdss_access'] and not test:
                dm.write_stubs()

        if dm.access[release]['in_sdss_access']:
            log.info(f'Found updated path for file species {species}, release {release}.')


        if test:
            continue

        # commit the stubs into git
        try:
            dm.commit_stubs()
        except RuntimeError as err:
            log.error(f'Could not commit stubs to git.  Check for errors and try again. Error - {err}')
