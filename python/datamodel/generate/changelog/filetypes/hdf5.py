# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import absolute_import, division, print_function

from datamodel.generate.changelog.yaml import YamlDiff


class YamlHDF5(YamlDiff):
    """ Class for supporting YAML changelog generation for HDF5 files """
    suffix = 'H5'
    cache_key = 'hdfs'

    @staticmethod
    def _get_attrs_diff(nattrs: list, oattrs: list):
        n_attrs = len(nattrs)
        n_attrs2 = len(oattrs)
        hdr = [i['key'] for i in nattrs]
        hdr2 = [i['key'] for i in oattrs]
        delta_nattrs = abs(n_attrs - n_attrs2)
        added_attrs = list(set(hdr) - set(hdr2))
        removed_attrs = list(set(hdr2) - set(hdr))
        return delta_nattrs, added_attrs, removed_attrs

    def _get_changes(self, version1: str, version2: str, simple: bool = None) -> dict:
        """ Changelog computer for HDF5 files """
        hdfs = self.releases.get(version1, {}).get('hdfs', {})
        hdfs2 = self.releases.get(version2, {}).get('hdfs', {})

        if not hdfs or not hdfs2:
            raise ValueError('No hdfs object found for input versions.')

        # look for changes
        #'n_members group; dataset ndim, shape, size; attrs in each group/dataaset'

        # HDF5 library version change
        new_libver = hdfs['libver'] if hdfs['libver'] != hdfs2['libver'] else []

        # top level members change
        delta_nmembers = abs(hdfs['n_members'] - hdfs2['n_members'])
        added_members = list(set(hdfs['members']) - set(hdfs2['members']))
        removed_members = list(set(hdfs2['members']) - set(hdfs['members']))

        # top level HDF5 attributes change
        delta_nattrs, added_attrs, removed_attrs = self._get_attrs_diff(hdfs['attrs'], hdfs2['attrs'])

        # HDF5 member changes
        mdiffs = {}
        for name, data in hdfs['members'].items():
            if name not in hdfs2['members']:
                continue
            m2 = hdfs2['members'][name]

            delta_gnmembers = abs(data['n_members'] - m2['n_members']) if data['object'] == 'group' else None
            delta_mnattrs, added_mattrs, removed_mattrs = self._get_attrs_diff(data['attrs'], m2['attrs'])

            delta_ndim = abs(data['ndim'] - m2['ndim']) if data['object'] == 'dataset' else None
            new_shape = (data['shape'] if data['shape'] != m2['shape'] else []) if data['object'] == 'dataset' else None
            delta_size = abs(data['size'] - m2['size']) if data['object'] == 'dataset' else None

            mdiffs[name] = {
                'delta_nmembers': delta_gnmembers,
                'delta_nattrs': delta_mnattrs,
                'added_attrs': added_mattrs,
                'removed_attrs': removed_mattrs,
                'delta_ndim': delta_ndim,
                'new_shape': new_shape,
                'delta_size': delta_size
            }

        changes = {
            version1: {
                'from': version2,
                'new_libver': new_libver,
                'delta_nattrs': delta_nattrs,
                'added_attrs': added_attrs,
                'removed_attrs': removed_attrs,
                'delta_nmembers': delta_nmembers,
                'added_members': added_members,
                'removed_members': removed_members,
                'members': mdiffs,
                }
            }

        # return only entries that are not null
        if simple:
            changes[version1] = self.clean_empty(changes[version1])

        return changes