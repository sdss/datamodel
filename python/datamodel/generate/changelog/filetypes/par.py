# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import absolute_import, division, print_function

import six
from typing import Type, Union

from datamodel.generate.changelog.core import FileDiff
from datamodel.generate.changelog.yaml import YamlDiff

try:
    from pydl.pydlutils.yanny import yanny
except ImportError:
    yanny = None

class ParDiff(FileDiff):
    """ Class for computing differences between Yanny par files

    Computes the differences in table content between two Yanny par
    files.  Looks for changes in header keys, table number, and any added
    or removed keys, tables, or table columns.

    Parameters
    ----------
    file1 : Union[str, Table]
        the filepath or Table to compute the changes against
    file2 : Union[str, Table]
        the filepath or Table to compute the changes from
    versions : list, optional
        the named releases/versions corresponding to the two input files, by default None
    """
    suffix = 'PAR'

    def __init__(self, file1: Union[str, yanny], file2: Union[str, yanny],
                 versions: list = None):
        super(ParDiff, self).__init__(file1, file2, diff_type='par', versions=versions)

        # get the Yanny par objects
        self.par = self._check_data(self.file1)
        self.par2 = self._check_data(self.file2)

        # Yanny header differences
        hdr = self.par.pairs()
        hdr2 = self.par2.pairs()
        n_keys = len(hdr)
        n_keys2 = len(hdr2)
        self.delta_nkeys = abs(n_keys - n_keys2)
        self.added_keys = list(set(hdr) - set(hdr2))
        self.removed_keys = list(set(hdr2) - set(hdr))

        # Yanny table differences
        tables = self.par.tables()
        tables2 = self.par2.tables()
        n_tables = len(tables)
        n_tables2 = len(tables2)
        self.delta_ntables = abs(n_tables - n_tables2)
        self.added_tables = list(set(tables) - set(tables2))
        self.removed_tables = list(set(tables2) - set(tables))

        # Yanny table column differences
        self.table_diffs = {}
        for table in tables:
            if table in tables2:
                cols = self.par.columns(table)
                cols2 = self.par2.columns(table)
                self.table_diffs[table] = {
                    'added_cols': list(set(cols) - set(cols2)),
                    'removed_cols': list(set(cols2) - set(cols)),
                    'n_rows': self.par.size(table),
                    'n_rows2': self.par2.size(table),
                    'delta_rows': abs(self.par.size(table) - self.par2.size(table))
                }

        # build diff dictionary
        self.changes = {'version_1': self.versions[0], 'version_2': self.versions[1],
                        'file_1': self.file1, 'file_2': self.file2,
                        'added_keys': self.added_keys, 'removed_keys': self.removed_keys,
                        'added_tables': self.added_tables, 'removed_tables': self.removed_tables,
                        'table_diffs': self.table_diffs}

    @staticmethod
    def _check_data(data: Union[str, Type[yanny]]) -> yanny:
        """ Check the input for proper Yanny par file name or object

        Checks for and opens a valid Yanny par file

        Parameters
        ----------
        data : str | Type[yanny]
            a Yanny par filepath or a valid Yanny object

        Returns
        -------
        yanny
            the Yanny content
        """
        if not yanny:
            raise ImportError('Computing Yanny file changelog diffs requies the pydl package installed.')

        if not isinstance(data, yanny):
            assert isinstance(
                data, six.string_types), 'input must be string filename or a yanny object'
            assert '.par' in data, 'No .par suffix found.  Is this a proper Yanny par file?'
            data = yanny(data)
        return data

    def report(self, split: bool = None, full: bool = None) -> str:
        """  Print the yanny par difference report """

        diffreport = f"Version: {self.changes['version_1']} to {self.changes['version_2']}\n"

        # print the Yanny header differences
        diffreport += f'Changes in header number: {self.delta_nkeys}\n'
        diffreport += f'Added header keys: {", ".join(self.added_keys)}\n'
        diffreport += f'Removed header keys: {", ".join(self.removed_keys)}\n\n'

        # print the Yanny table differences
        diffreport += f'Changes in table number: {self.delta_ntables}\n'
        diffreport += f'Added Tables: {", ".join(self.added_tables)}\n'
        diffreport += f'Removed Tables: {", ".join(self.removed_tables)}\n\n'

        # print the Yanny table column differences
        for table, data in self.table_diffs.items():
            diffreport += f'Table: {table}\n'
            diffreport += f'Added Columns: {", ".join(data["added_cols"])}\n'
            diffreport += f'Removed Columns: {", ".join(data["removed_cols"])}\n'
            diffreport += f'Old row number: {data["n_rows2"]}\n'
            diffreport += f'New row number: {data["n_rows"]}\n'
            diffreport += f'Changes in row number: {data["delta_rows"]}\n\n'

        return diffreport


class YamlPar(YamlDiff):
    """ Class for supporting YAML changelog generation for Yanny par files """
    suffix = 'PAR'
    cache_key = 'par'

    def _get_changes(self, version1: str, version2: str, simple: bool = None) -> dict:
        """ Changelog computer for Yanny par files """
        par = self.releases.get(version1, {}).get('par', {})
        par2 = self.releases.get(version2, {}).get('par', {})

        if not par or not par2:
            raise ValueError('No par object found for input versions.')

        # Yanny header differences
        n_keys = len(par['header'])
        n_keys2 = len(par2['header'])
        hdr = [i['key'] for i in par['header']]
        hdr2 = [i['key'] for i in par2['header']]
        delta_nkeys = abs(n_keys - n_keys2)
        added_keys = list(set(hdr) - set(hdr2))
        removed_keys = list(set(hdr2) - set(hdr))

        # Yanny table differences
        n_tables = len(par['tables'])
        n_tables2 = len(par2['tables'])
        delta_ntables = abs(n_tables - n_tables2)
        tables = par['tables'].keys()
        tables2 = par2['tables'].keys()
        added_tables = list(set(tables) - set(tables2))
        removed_tables = list(set(tables2) - set(tables))

        # Yanny table column differences
        tdiffs = {}
        for table, data in par['tables'].items():
            if table not in tables2:
                continue
            t2 = par2['tables'][table]
            delta_nrows = abs(data['n_rows'] - t2['n_rows'])
            cols = [i['name'] for i in data['structure']]
            cols2 = [i['name'] for i in t2['structure']]
            tdiffs[table] = {
                'added_cols': list(set(cols) - set(cols2)),
                'removed_cols': list(set(cols2) - set(cols)),
                'delta_nrows': delta_nrows,
            }

        changes = {
            version1: {
                'from': version2,
                'delta_nkeys': delta_nkeys,
                'added_header_keys': added_keys,
                'removed_header_keys': removed_keys,
                'delta_ntables': delta_ntables,
                'added_tables': added_tables,
                'removed_tables': removed_tables,
                'tables': tdiffs,
                }
            }

        # return only entries that are not null
        if simple:
            changes[version1] = self.clean_empty(changes[version1])

        return changes

