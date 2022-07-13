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


def get_new_products(release: str = None) -> tuple:
    """ Get new datamodel products for the tree

    Retrieves any valid JSON datamodels that do not
    yet have a corresponding tree entry, i.e. the `in_sdss_access`
    field is False.

    Parameters
    ----------
    release : str, optional
        the SDSS release, by default None

    Yields
    ------
    tuple
        The release and access string
    """
    for product, data in yield_products(release=release):
        # if not data, the skip
        if not data:
            continue

        if not release:
            # if no release specified, loop over all releases
            for rr, info in data.items():
                if info['in_sdss_access']:
                    continue
                log.info(f'new product {product} with access {info["access_string"]}.')
                yield rr, info["access_string"]
        elif not data['in_sdss_access']:
            log.info(f'new product {product} with access {data["access_string"]}.')
            yield release, data["access_string"]


def make_branch(repo: Repo, branch: str = 'dm_update_tree') -> Repo:
    """ Make a new branch in the tree repo

    Checkout or create a branch in the tree repo.

    Parameters
    ----------
    repo : Repo
        the git repo
    branch : _type_, optional
        the name of the branch, by default "dm_update_tree"

    Returns
    -------
    Repo
        the git repo
    """
    # set to master and fetch/pull
    log.info('Setting up tree repo.')
    repo.git.checkout('master')
    repo.remotes.origin.fetch()
    repo.remotes.origin.pull()

    # checkout a new branch
    if branch in repo.branches:
        log.info(f'Checking out existing branch {branch}.')
        repo.git.checkout(branch)
    else:
        log.info(f'Creating new working branch {branch}.')
        repo.git.checkout('HEAD', b=branch)
    return repo


def clone_tree(branch: str = 'dm_update_tree', local: bool = None, path: str = None) -> Repo:
    """ Clone the tree repo

    Clone the tree repo from either an existing local source
    or cloning the remote repo into a temporary directory.

    Parameters
    ----------
    branch : str, optional
        the name of the branch, by default None
    local : bool, optional
        if True, use a local tree repo, by default None
    path : str, optional
        a path to check out the tree repo to

    Returns
    -------
    Repo
        the git repo
    """
    treedir = os.getenv("TREE_DIR")
    if local and treedir:
        log.info(f'Using local tree repository at {treedir}')
        r = Repo(treedir)
        return make_branch(r, branch=branch)

    tmpdir = path or tempfile.TemporaryDirectory()
    log.info(f'Cloning tree repository at {tmpdir}')
    r = Repo.clone_from("https://github.com/sdss/tree", tmpdir)
    return make_branch(r, branch=branch)


def add_and_commit(repo: Repo, file: str, message: str = None):
    """ Add and commit a file to the tree

    Add and commit a file to the tree repo.

    Parameters
    ----------
    repo : Repo
        _description_
    file : str
        _description_
    message : str, optional
        _description_, by default None
    """
    repo.index.add(file)
    repo.index.commit(message or "datamodel auto updating tree with new paths")
    log.info(f'Committing changes to file {file}.')


def pull_and_push(repo: Repo):
    """ Pull and push the tree repo

    Pull and push the current tree repo head to the remote.

    Parameters
    ----------
    repo : Repo
        the git repo
    """
    # if the branch has a remote tracking branch, pull
    if repo.active_branch.tracking_branch():
        repo.remotes.origin.pull()

    # push the branch
    repo.remotes.origin.push(repo.active_branch, set_upstream=True)
    log.info('Pushing changes to origin.')


def update_tree(release: str = None, work_ver: str = None, branch: str = 'dm_update_tree',
                local: bool = None, test: bool = None, skip_push: bool = False):
    """ Update the tree repo with new paths

    Updates the tree repo with new paths for datamodel products.  Gets all new
    JSON datamodels that do not yet have tree paths, and adds them to the PATH
    ini section of the respective release config file.  Clones the tree repo and
    makes all commits in a new branch, by default 'dm_update_tree'.  Commits and
    pushes the branch to the remote.  Makes a backup of the tree config file before
    writing any new changes.  On failure, the backup is restored.

    Use the test flag to skip all write operations and just print the new paths.
    Use the skip_push flag to bypass the push to the remote.

    Parameters
    ----------
    release : str, optional
        the SDSS release, by default None
    work_ver : str, optional
        the tree config work version, by default None
    branch : str, optional
        the tree repo branch name, by default 'dm_update_tree'
    local : bool, optional
        if set, uses an existing local repo, by default None
    test : bool, optional
        if set, turns on testing, by default None
    skip_push : bool, optional
        if set, skips the git push, by default None
    """

    # clone the tree repo
    repo = clone_tree(branch=branch, local=local)

    # update tree dir to point to cloned path
    new_tree_dir = repo.git_dir.split('/.git')[0]
    os.environ['TREE_DIR'] = new_tree_dir

    # iterate over all the new products, grouped by release
    new_items = []
    for rr, items in itertools.groupby(sorted(get_new_products(release=release)), key=lambda x: x[0]):
        # do nothing if no new products
        if not rr or not items:
            log.info("Nothing to update.")
            break

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

    # if no new items, return
    if not new_items:
        log.info("Nothing to update.")
        return

    # push the changes
    if not test and not skip_push:
        try:
            pull_and_push(repo)
        except GitCommandError:
            log.error('Failed to push changes to origin. Cleaning up and removing local branch.')
            repo.checkout('master')
            repo.delete_head(repo.heads[branch])


def write_no_comments(cfgfile: str, paths: list):
    """ Update a tree config file

    Write a tree config file with new paths added into it.
    This removes all comments from the tree ini config file.
    The list of paths to add is a list of tuples of
    path_name, path_template.  Does not add them if they already
    exist in the config file.

    Parameters
    ----------
    cfgfile : str
        the tree config file path
    paths : list
        a list of paths to add
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
    """ Update a tree config file

    Write a tree config file with new paths added into it.
    This preserves all comments from the tree ini config file.
    The list of paths to add is a list of tuples of
    path_name, path_template.  Does not add them if they already
    exist in the config file.

    Parameters
    ----------
    cfgfile : str
        the tree config file path
    paths : list
        a list of paths to add
    """
    # preserve comments
    config = ConfigObj(cfgfile)

    for name, template in paths:
        if name in config["PATHS"] and config["PATHS"][name] == template:
            log.info(f'Path {name} = {template} already exists in {cfgfile}.')
            continue

        config["PATHS"][name] = template

    config.write()


def update_datamodel_access(branch: str = 'dm_update_models', test: bool = None, commit_to_git: bool = False):
    """ Updates the datamodel access info sections

    Checks all "new" JSON datamodels for updated access info.  Creates a new
    datamodel instance using the product file species, and updates YAML file
    and all stubs with the updated access info for the indicated release.

    Parameters
    ----------
    branch : str, optional
        the datamodel repo branch name, by default 'dm_update_models'
    test : bool, optional
        if set, skips all write operations, by default None
    commit_to_git : bool, optional
        if set, commits to git, by default False
    """
    # loop for new JSON datamodel products
    for release, access_string in get_new_products():
        # no missing products
        if not release or not access_string:
            continue

        if test:
            log.info('Test mode: not writing datamodel stubs.')

        # load the datamodel from the relevant YAML file
        species = access_string.split(' = ')[0]

        dm = DataModel.from_yaml(species, release)

        # checkout a branch
        if not test:
            dm._git.checkout(branch)

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
        if commit_to_git:
            try:
                dm.commit_stubs()
            except RuntimeError as err:
                log.error(f'Could not commit stubs to git.  Check for errors and try again. Error - {err}')
