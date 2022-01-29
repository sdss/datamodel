# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import absolute_import, division, print_function

import abc
import pathlib
from typing import Union

from datamodel import log

class ChangeLog(list):
    """ Class that holds the change logs for all input files

    Contains a list of all FileDiff objects.  Mainly used as a container to
    iterate over many changelogs and generate a string report or dictionary object
    for each item in the list.

    Parameters
    ----------
    the_list : list
        A list of FileDiff objects
    """
    def __init__(self, the_list: list, **kwargs):
        super(ChangeLog, self).__init__(the_list, **kwargs)

    def generate_report(self, split: bool = None, insert: bool = True) -> Union[str, list]:
        """ Generate a string report of all changelogs

        Iterates over all changelogs and builds a complete report containing
        all differences.

        Parameters
        ----------
        split : bool, optional
            If True, splits the string, by default None
        insert : bool, optional
            If True, inserts a divider between changelogs, by default True

        Returns
        -------
        str | list
            A generated report of all changelogs
        """

        full_report = [] if split else ''
        for item in self:
            lines = item.report(split=split)
            if split:
                if insert:
                    full_report.append('---------------------')
                full_report.extend(lines)
            else:
                if insert:
                    full_report += '\n---------------------\n'
                full_report += lines
        return full_report

    def get_changes(self) -> dict:
        return {item.changes['version_1']: {
                'from': item.changes['version_2'],
                'delta_nhdu': item.delta_nhdu,
                'added_hdus': item.added_hdus,
                'removed_hdus': item.removed_hdus,
                'primary_keys_ndiff': item.diff_keycount,
                'added_primary_header_kwargs': item.added_kwargs,
                'removed_primary_header_kwargs': item.removed_kwargs,
            } for item in self}


class FileDiff(abc.ABC, object):
    """ Class that holds the difference between two files

    Creates an object that compares the difference between two files.  Base class
    that is subclassed by FitsDiff and CatalogDiff.

    Parameters
    ----------
    file1 : str
        the filepath to compute the changes against
    file2 : str
        the filepath to compute the changes from
    versions : list, optional
        the named releases/versions corresponding to the two input files, by default None
    diff_type : str, optional
        the object data type of which to compute the difference, by default None
    """

    def __init__(self, file1: str, file2: str, versions: list = None, diff_type: str = None):
        self.diff_type = diff_type
        self.versions = versions or ['A', 'B']
        self.file1 = str(file1)
        self.file2 = str(file2)

    def __repr__(self) -> str:
        return f"<FileDiff (versions='{','.join(self.versions)}', diff_type='{self.diff_type}')>"

    @abc.abstractmethod
    def report(self):
        ''' Print a report '''

    @abc.abstractstaticmethod
    def _check_data(self):
        ''' Check the data type '''


def compute_diff(oldfile: str, otherfile: str, change: str = 'fits', versions: list = None) -> FileDiff:
    """ Produce a single changelog between two files

    Produce a difference object for two files

    Parameters
    ----------
    oldfile : str
        The filepath to check changes against
    otherfile : str
        The filepath to check changes from
    change : str, optional
        The type of data input, by default 'fits'
    versions : list, optional
        The named releases/versions of the corresponding file inputs, by default None

    Returns
    -------
    FileDiff
        An instance containing the differences between the two files

    Raises
    ------
    ValueError
        when no valid input filepath is given
    """

    # check old filename
    name = pathlib.Path(oldfile)
    if not name.exists():
        raise ValueError(f'File {name} does not exist!')

    # check other filename
    other_name = pathlib.Path(otherfile)
    if not other_name.exists():
        raise ValueError(f'File {otherfile} must exist!')


    # check the type of file
    if change == 'fits':
        diffobj = FitsDiff
    elif change == 'catalog':
        diffobj = CatalogDiff
    elif change == 'par':
        diffobj = ParDiff
    else:
        log.warning(f'Diffs for type "{change}" is not currently supported.  Cannot produce changelog.')
        return

    # compute file difference
    fd = diffobj(name, other_name, versions=versions)

    return fd

def compute_changelog(items: list, change: str = 'fits') -> ChangeLog:
    """ Compute the changelogs between a list of datamodels

    Given an input list of DataModel objects, computes the differences
    between them using the on-disk real file location.  By default computes
    the FITS differences.

    Parameters
    ----------
    items : list
        A list of datamodels
    change : str, optional
        The type of object, by default fits

    Returns
    -------
    ChangeLog
        A list of changelogs
    """
    zipped = list(zip(items[:-1], items[1:]))
    fds = []
    for item in zipped:
        v1 = str(item[0].release)
        v2 = str(item[1].release)
        exist1 = item[0].file_exists
        exist2 = item[1].file_exists
        if exist1 and exist2:
            fds.append(compute_diff(str(item[0].file), str(
                item[1].file), versions=[v1, v2], change=change))
        else:
            log.warning('One or more files does not exist.  Cannot compute changelog '
                        f'for this changeset. Version {v1}: exists={exist1}; '
                        f'Version {v2}: exists={exist2}')
    return ChangeLog(fds)
