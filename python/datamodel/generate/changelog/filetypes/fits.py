# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import absolute_import, division, print_function

from typing import Type, Union

import six
from astropy.io import fits

from datamodel.generate.changelog.core import FileDiff
from datamodel.generate.changelog.yaml import YamlDiff


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
    suffix = 'FITS'

    def __init__(self, file1: Union[str, fits.HDUList], file2: Union[str, fits.HDUList],
                 full: bool = None, versions: list = None):
        super(FitsDiff, self).__init__(file1, file2, diff_type='fits', versions=versions)

        # get the HDU lists
        self.hdulist = self._check_data(self.file1)
        self.hdulist2 = self._check_data(self.file2)

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
    def _check_data(data: Union[str, Type[fits.HDUList]]) -> fits.HDUList:
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


class YamlFits(YamlDiff):
    """ Class for supporting YAML changelog generation for FITS files """
    suffix = 'FITS'
    cache_key = 'hdus'

    def _get_changes(self, version1: str, version2: str, simple: bool = None) -> dict:
        """ Changelog computer for FITS files """
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
            #changes[version1] = {k: v for k, v in changes[version1].items() if v}
            changes[version1] = self.clean_empty(changes[version1])

        return changes