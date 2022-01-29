# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import absolute_import, division, print_function

from io import StringIO
from typing import Type, Union

import six
from astropy.io import ascii as astropy_ascii
from astropy.table import Table

try:
    from astropy.utils.diff import report_diff_values
except ImportError:
    report_diff_values = None

from datamodel.generate.changelog.core import FileDiff


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
        self.table = self._check_data(self.file1)
        self.table2 = self._check_data(self.file2)

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
    def _check_data(data: Type[Table]) -> Table:
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