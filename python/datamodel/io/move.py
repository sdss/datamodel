# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pathlib
import re
import shutil

from typing import Iterator, Union

from tree import Tree
from datamodel import log


def dm_move(old: str, new: str, parent: bool = None, symlink: bool = True):
    """_summary_

    _extended_summary_

    Parameters
    ----------
    old : str
        _description_
    new : str
        _description_
    parent : bool, optional
        _description_, by default None
    symlink : bool, optional
        _description_, by default True
    """

    oldfile = pathlib.Path(old)
    newfile = pathlib.Path(new)

    # if parent set, use the parent directories
    if parent:
        oldfile = oldfile.parent
        newfile = newfile.parent

    # check if new directory exists, and make them
    if not newfile.parent.exists():
        newfile.parent.mkdir(parents=True, exist_ok=True)

    # move old to new
    if parent:
        shutil.move(str(oldfile), str(newfile.parent))
    else:
        shutil.move(str(oldfile), str(newfile))

    # and create symlink
    if symlink:
        os.symlink(newfile, oldfile, target_is_directory=parent)


def find_files_from_species(path: str) -> Iterator:
    """ Find all files species from an abstract path

    Finds all files matching the species pattern in a given
    abstract path.

    Parameters
    ----------
    path : str
        an abstract file species path

    Returns
    -------
    Iterator
        Iterator over all matching files found

    """
    # create a path from
    wild_path = re.sub('{(.*?)}', '*', path)
    wild_path = wild_path if wild_path.startswith("$") else f"${wild_path}"
    tmp_path = pathlib.Path(os.path.expandvars(wild_path))

    # find the appropriate parent
    if '*' in tmp_path.parts:
        idx = len(tmp_path.parents) - tmp_path.parts.index('*')
        parent = tmp_path.parents[idx]
    else:
        parent = tmp_path.parent

    # return any files
    return parent.rglob(tmp_path.name)


def dm_move_species(abstract_path: str, new_path: str, release: str, parent: bool = None,
                    symlink: bool = True, test: bool = None):
    """ Moves all files from a species to a new location

    Moves all files from a given file species.  Finds all real files that match
    an existing file species abstract path, and moves them to a new location.  The
    location is determined by the original filename, a new abstract path location, and
    a given release.

    Parameters
    ----------
    abstract_path : str
        the existing species abstract path
    new_path : str
        the new species abstract path
    release : str
        the SDSS release
    parent : bool, optional
        flag to move the entire parent directory, by default None
    symlink : bool, optional
        flag to create a symlink from new location to old one, by default True
    test : bool, optional
        flag to test the move, by default None
    """
    # get all the files matching a file species
    files = find_files_from_species(abstract_path)

    # loop over all files and move them to their new location
    for file in files:
        if 'v4_0_0_orig' in str(file):
            continue
        new_filepath = construct_new_path(file=file, old_path=abstract_path, new_path=new_path, release=release)
        log.info(f'Moving {file} to {new_filepath}.')
        if not test:
            dm_move(file, new_filepath, parent=parent, symlink=symlink)


def construct_new_path(file: Union[str, pathlib.Path] = None,
                       old_path: Union[str, pathlib.Path] = None,
                       new_path: Union[str, pathlib.Path] = None,
                       release: str = None, kwargs: dict = None) -> pathlib.Path:
    """ Construct a new filepath

    Constructs a new filepath, either from an abstract path location and a set of
    keyword arguments, or from an existing (old) filepath and abstract location.

    Parameters
    ----------
    file : Union[str, pathlib.Path], optional
        the existing full filepath, by default None
    old_path : Union[str, pathlib.Path], optional
        the existing species abstract path, by default None
    new_path : Union[str, pathlib.Path], optional
        the new species abstract path, by default None
    release : str, optional
        the SDSS release, by default None
    kwargs : dict, optional
        a set of path keyword arguments, by default None

    Returns
    -------
    pathlib.Path
        a full filepath
    """

    # construct a file path using a new abstract path and a set of kwargs
    if new_path and kwargs:
        tree = Tree(release.lower(), update=True)
        return pathlib.Path(os.path.expandvars(f"${str(new_path).format(**kwargs)}"))

    # construct a file path using an old file path and and old abstract path
    if file and old_path:
        # get the environment variable names
        oldenvar = os.environ.get(old_path.split('/')[0])

        # get the new envvar from either a specifed new abstract path or the old one
        newenvar = str(new_path).split('/')[0] if new_path else str(old_path).split('/')[0]

        # update the tree with the new release
        tree = Tree(release.lower(), update=True)

        # build a new full file path
        fullnew = os.path.expandvars(f'${newenvar}')
        if fullnew.startswith('$') or 'work' in fullnew:
            fullnew = re.sub(r"/(\w+work|dr\d{1,2})/", f'/{release.lower()}/', str(file))
        else:
            fullnew = str(file).replace(oldenvar, fullnew)
        return pathlib.Path(fullnew)

