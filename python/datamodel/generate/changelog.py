# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: changelog.py
# Project: generate
# Author: Brian Cherinka
# Created: Wednesday, 10th March 2021 1:09:33 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Wednesday, 10th March 2021 1:09:33 pm
# Modified By: Brian Cherinka


from __future__ import absolute_import, division, print_function

import abc
import pathlib
import re
from io import StringIO
from typing import Type, Union

import six
import yaml
from astropy.io import ascii as astropy_ascii
from astropy.io import fits
from astropy.table import Table

from datamodel import log

try:
    from astropy.utils.diff import report_diff_values
except ImportError:
    report_diff_values = None


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

    @abc.abstractclassmethod
    def report(self):
        ''' Print a report '''


class FitsDiff(FileDiff):
    """ Compute the difference between two FITS files

    Computes the differences in HDUList content between two input FITS
    files.  Looks for changes in HDU extension number, any added or removed HDU
    extensions, as well as any changes in the primary header keywords.

    Parameters
    ----------
    file1 : Union[str, fits.HDUList]
        the filepath or HDUList to compute the changes against
    file2 : Union[str, fits.HDUList]
        the filepath or HDUList to compute the changes from
    full : bool, optional
        If True, compute the full Astropy FITS HDUList differences, by default None
    versions : list, optional
        the named releases/versions corresponding to the two input files, by default None
    """

    def __init__(self, file1: Union[str, fits.HDUList], file2: Union[str, fits.HDUList],
                 full: bool = None, versions: list = None):
        super(FitsDiff, self).__init__(file1, file2, diff_type='fits', versions=versions)

        # get the HDU lists
        self.hdulist = self._check_fits(self.file1)
        self.hdulist2 = self._check_fits(self.file2)

        # HDU differences
        n_hdus = len(self.hdulist)
        n_hdu2s = len(self.hdulist2)
        self.delta_nhdu = abs(n_hdus - n_hdu2s)

        self.n_hdu_diffs = (n_hdus, n_hdu2s)
        hdu_names = [n.name for n in self.hdulist]
        hdu2_names = [n.name for n in self.hdulist2]

        self.added_hdus = list(set(hdu_names) - set(hdu2_names))
        self.removed_hdus = list(set(hdu2_names) - set(hdu_names))

        # PRIMARY header differences
        hd = fits.HDUDiff(self.hdulist['PRIMARY'], self.hdulist2['PRIMARY'],
                          ignore_comments=['*'], rtol=10.0)
        self.diff_keycount = hd.diff_headers.diff_keyword_count
        self.added_kwargs = hd.diff_headers.diff_keywords[0] if self.diff_keycount else []
        self.removed_kwargs = hd.diff_headers.diff_keywords[1] if self.diff_keycount else []

        # get the full report
        self.astropy_diff = self.get_astropy_diff() if full else None

        # build diff dictionary
        self.changes = {'version_1': self.versions[0], 'version_2': self.versions[1],
                        'file_1': self.file1, 'file_2': self.file2,
                        'delta_nhdu': self.delta_nhdu, 'nhdu_diffs': self.n_hdu_diffs,
                        'added_hdus': self.added_hdus, 'removed_hdus': self.removed_hdus,
                        'primary_header_key_diffs': self.diff_keycount,
                        'primary_header_added_kwargs': self.added_kwargs,
                        'primary_header_removed_kwargs': self.removed_kwargs}

        # close the HDU lists
        self.hdulist.close()
        self.hdulist2.close()

    @staticmethod
    def _check_fits(data: Union[str, Type[fits.HDUList]]) -> fits.HDUList:
        """ Check the input for proper FITS file name or object

        Checks for and opens a valid FITS file

        Parameters
        ----------
        data : str | Type[fits.HDUList]
            a FITS filepath or a valid HDUList

        Returns
        -------
        fits.HDUList
            the FITS content
        """

        if not isinstance(data, fits.hdu.hdulist.HDUList):
            assert isinstance(
                data, six.string_types), 'input must be string filename or a FITS HDUList '
            assert '.fits' in data, 'No .fits suffix found.  Is this a proper FITS file?'
            data = fits.open(data)
        return data

    def get_astropy_diff(self) -> fits.FITSDiff:
        """ Returns the full Astropy FITSDiff

        Returns
        -------
        fits.FITSDiff
            the complete difference between the two FITS files
        """
        return fits.FITSDiff(self.hdulist, self.hdulist2)

    def report(self, split: bool = None) -> str:
        """ Print the FITS difference report

        Returns the FITS differences as a string blob.  Can optionally
        return the report as a list of string lines.

        Parameters
        ----------
        split : bool, optional
            if True, splits the report into a list of string lines, by default None

        Returns
        -------
        str
            The difference report as a string blob
        """

        diffreport = f"Version: {self.changes['version_1']} to {self.changes['version_2']}\n"

        # print the HDU differences
        diffreport += f'Changes in HDU number: {self.delta_nhdu}\n'
        diffreport += f'Added HDUs: {", ".join(self.added_hdus)}\n'
        diffreport += f'Removed HDUs: {", ".join(self.removed_hdus)}\n\n'

        # print the PRIMARY header differences
        diffreport += 'Primary Header Differences:\n'
        diffreport += f'Added Keywords: {", ".join(self.added_kwargs)}\n'
        diffreport += f'Removed Keywords: {", ".join(self.removed_kwargs)}\n'

        # print the Astropy FITS difference report
        if self.astropy_diff:
            fullreport = self.astropy_diff.report()
            diffreport += '\nFull Report:\n'
            diffreport += fullreport

        # split the report
        if split:
            diffreport = diffreport.split('\n')

        return diffreport


class CatalogDiff(FileDiff):
    """ Compute the difference between two catalog files

    Computes the differences in catalog content between two input ascii
    catalog files, e.g. CSV.  Looks for changes in row number, column number,
    and any added or removed column names.

    Parameters
    ----------
    file1 : Union[str, Table]
        the filepath or Table to compute the changes against
    file2 : Union[str, Table]
        the filepath or Table to compute the changes from
    full : bool, optional
        If True, compute the full Astropy Ascii Table differences, by default None
    versions : list, optional
        the named releases/versions corresponding to the two input files, by default None
    """

    def __init__(self, file1: Union[str, Table], file2: Union[str, Table],
                 full: bool = None, versions: list = None):
        super(CatalogDiff, self).__init__(file1, file2, diff_type='catalog', versions=versions)

        # get the catalog tables
        self.table = self._check_catalog(self.file1)
        self.table2 = self._check_catalog(self.file2)

        # Table row differences
        n_rows = len(self.table)
        n_row2s = len(self.table2)
        self.delta_rows = abs(n_rows - n_row2s)
        self.n_row_diffs = (n_rows, n_row2s)

        # Table column differences
        col_names = self.table.colnames
        col2_names = self.table2.colnames
        self.delta_cols = len(set(col_names) ^ set(col2_names))
        self.added_cols = list(set(col_names) - set(col2_names))
        self.removed_cols = list(set(col2_names) - set(col_names))

        # get the full report
        self.astropy_diff = self.get_astropy_diff() if full else None

        # build diff dictionary
        self.changes = {'version_1': self.versions[0], 'version_2': self.versions[1],
                        'file_1': self.file1, 'file_2': self.file2,
                        'delta_rows': self.delta_rows, 'nrow_diffs': self.n_row_diffs,
                        'added_cols': self.added_cols, 'removed_cols': self.removed_cols,
                        'delta_cols': self.delta_cols}

    @staticmethod
    def _check_catalog(data: Type[Table]) -> Table:
        """ Check the input for proper catalog file name or object

        Checks for and opens a valid csv file

        Parameters
        ----------
        data : str | Type[Table]
            a catalog filepath or a valid Astropy Ascii Table

        Returns
        -------
        astropy.table.Table
            the catalog content as an astropy table
        """
        if not isinstance(data, Table):
            assert isinstance(
                data, six.string_types), 'input must be string filename or a Table '
            assert '.csv' in data, 'No .csv suffix found.  Is this a proper catalog file?'
            data = astropy_ascii.read(data)
        return data

    def get_astropy_diff(self) -> str:
        """ Returns the full Astropy diff using report_diff_values

        Returns
        -------
        str
            the complete difference between the two catalog files
        """
        report = None
        if report_diff_values:
            s = StringIO()
            same = report_diff_values(self.table, self.table2, s)
            if not same:
                s.seek(0)
                report = ''.join(s.readlines())
                s.close()
        return report

    def report(self, split: bool = None, full: bool = None) -> str:
        """  Print the catalog difference report

        Returns the catalog differences as a string blob.  Can optionally
        return the report as a list of string lines.

        Parameters
        ----------
        split : bool, optional
            if True, splits the report into a list of string lines, by default None
        full : bool, optional
            if True, appends the full Astropy catalog diff report

        Returns
        -------
        str
            The difference report as a string blob
        """

        diffreport = f"Version: {self.changes['version_1']} to {self.changes['version_2']}\n"

        # print the column differences
        diffreport += f'Changes in row number: {self.delta_rows}\n'
        diffreport += f'Changes in column number: {self.delta_cols}\n'
        if self.delta_cols > 0:
            diffreport += f'Added Columns: {", ".join(self.added_cols)}\n'
            diffreport += f'Removed Columns: {", ".join(self.removed_cols)}\n\n'

        # print the Astropy Table difference report
        if self.astropy_diff or full:
            fullreport = self.astropy_diff or self.get_astropy_diff()
            diffreport += '\nFull Report:\n'
            diffreport += fullreport

        # split the report
        if split:
            diffreport = diffreport.split('\n')

        return diffreport


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



class YamlDiff(object):
    """ Computes the difference between two releases in YAML cache

    Computes the differences in HDU content between releases in a given
    YAML datamodel file, or cached dictionary.

    Parameters
    ----------
    content : dict, optional
        The yaml cache content for a given datamodel, by default None
    file : str, optional
        A path to a yaml datamodel file, by default None

    Raises
    ------
    ValueError
        when no yaml filepath or cache content is provided
    ValueError
        when no releases can be identified from the yaml content
    """

    def __init__(self, content: dict = None, file: str = None) -> None:
        self.content = content
        self.file = file

        if not self.file and not self.content:
            raise ValueError('Either a yaml filepath or yaml content dict must be specified.')

        if self.file:
            self._read_content()

        # attempt to get the file species name
        self.name = self.content.get('general', {}).get('name', '')

        if 'releases' in self.content:
            self.releases = self.content['releases']
        elif re.findall(r'WORK|DR\d{1,2}|MPL\d{1,2}|IPL\d{1,2}', ';'.join(self.content.keys())):
            self.releases = self.content
        else:
            raise ValueError('Cannot identify releases dict from input content or file')

    def __repr__(self) -> str:
        return f'<YamlDiff (name="{self.name}")>'

    def _read_content(self) -> None:
        """ Reads the content of YAML file """
        with open(self.file, 'r') as f:
            self.content = yaml.load(f.read(), Loader=yaml.FullLoader)

    def compute_changelog(self, version1: str = 'A', version2: str = 'B', simple: bool = False) -> dict:
        """ Compute the changelog between two releases

        Computes the changes between two releases in a given YAML cache.  Compares the
        "hdus" entries in each release, and looks for differences in HDU extension number,
        added or removed HDU extensions, differences in primary header keyword number, and
        any added or removed primary header keywords.

        Parameters
        ----------
        version1 : str, optional
            The release to check differences against, by default 'A'
        version2 : str, optional
            The release to check differences from, by default 'B'
        simple : bool, optional
            If True, simplfies the changelog entries to only non-null values, by default False

        Returns
        -------
        dict
            a dictionary of found changes

        Raises
        ------
        ValueError
            when no HDULists are found in the YAML cache
        """
        hdulist = self.releases.get(version1, {}).get('hdus', {})
        hdulist2 = self.releases.get(version2, {}).get('hdus', {})

        if not hdulist or not hdulist2:
            raise ValueError('No hdulist found for input versions.')

        n_hdus = len(hdulist.keys())
        n_hdus2 = len(hdulist.keys())
        delta_nhdu = abs(n_hdus - n_hdus2)

        hdu_names = [i['name'] for i in hdulist.values()]
        hdu2_names = [i['name'] for i in hdulist2.values()]

        added_hdus = list(set(hdu_names) - set(hdu2_names))
        removed_hdus = list(set(hdu2_names) - set(hdu_names))

        keys = [k['key'] for k in hdulist['hdu0']['header']]
        keys2 = [k['key'] for k in hdulist2['hdu0']['header']]
        delta_nkeys = abs(len(keys) - len(keys2))
        added_kwargs = list(set(keys) - set(keys2))
        removed_kwargs = list(set(keys2) - set(keys))

        changes = {
            version1: {
                'from': version2,
                'delta_nhdu': delta_nhdu,
                'added_hdus': added_hdus,
                'removed_hdus': removed_hdus,
                'primary_delta_nkeys': delta_nkeys,
                'added_primary_header_kwargs': added_kwargs,
                'removed_primary_header_kwargs': removed_kwargs,
            }
            }

        # return only entries that are not null
        if simple:
            changes[version1] = {k: v for k, v in changes[version1].items() if v}

        return changes

    def has_changes(self, version1: str = 'A', version2: str = 'B') -> bool:
        """ Check if there are any changes between two releases

        Computes the changelog between two releases and returns a flag if changes
        are detected.  Compares the differences of release "version1" from release
        "version2".

        Parameters
        ----------
        version1 : str, optional
            The release to check differences against, by default 'A'
        version2 : str, optional
            The release to check differences from, by default 'B'

        Returns
        -------
        bool
            True if any changes detected
        """
        changes = self.compute_changelog(version1=version1, version2=version2)
        values = changes[version1]
        return any(values['delta_nhdu'] != 0 or values['added_hdus'] or values['removed_hdus'] or
                values['primary_delta_nkeys'] != 0 or values['added_primary_header_kwargs'] or
                values['removed_primary_header_kwargs'])

    def generate_changelog(self, order: list = None, simple: bool = False) -> dict:
        """ Generate a full changelog dictionary across all releases

        Iterate over all releases and generate a complete changelog from one release
        to another.  The release order to compute the changelog can be specified by passing
        in a desired list of releases to the `order` keyword.  Set `simple` to True to produce
        a cleaner, simpler changelog, containing only non-null entries.

        Parameters
        ----------
        order : list, optional
            The order of releases to generate changelog from, by default None
        simple : bool, optional
            If True, simplfies the changelog entries to only non-null values, by default False

        Returns
        -------
        dict
            A complete changelog dictionary over all releases
        """
        changes = {}

        # build the release order
        rel_list = list(self.releases.keys())
        if order:
            rev_list = [rel_list[rel_list.index(i)] for i in order]
        else:
            rev_list = list(reversed(rel_list))

        zipped_rels = zip(rev_list[:-1], rev_list[1:])
        for item in zipped_rels:
            if self.has_changes(item[0], item[1]):
                changes.update(self.compute_changelog(item[0], item[1], simple=simple))
            else:
                changes.update({item[0]: {'from': item[1], 'note': 'No changes'}})
        return changes
