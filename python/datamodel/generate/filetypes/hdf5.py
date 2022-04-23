# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from turtle import shape
from typing import Union
from datamodel import log
from .base import BaseFile

from datamodel.models.yaml import HdfModel

import h5py
import os
import shutil

class HdfFile(BaseFile):
    """ Class for supporting HDF5 files """
    suffix = 'H5'
    cache_key = 'hdfs'
    _hdf5data = None

    def _generate_new_cache(self) -> dict:
        """ Generates the new cache for an HDF5 file """
        with h5py.File(self.filename, "r") as data:
            pytables = "PYTABLES_FORMAT_VERSION" in data.attrs
            self._hdf5data = {"name": data.name, "parent": data.parent.name, "object": "group",
                              "description": "replace me - with a description of this group",
                              "libver": data.libver, "n_members": len(data), 'pytables': pytables,
                              "attrs": self._create_attrs(data), "members": {}}
            data.visititems(self._build_cache)
            return self._hdf5data

    def _update_partial_cache(self, cached_data: dict, old_cache: dict) -> dict:
        """ Updates the partial cache for HDF5 files"""

        self._update_hdf_entry(cached_data, old_cache)

        # update core members
        for key, val in cached_data['members'].items():
            if key in old_cache["members"]:
                self._update_hdf_entry(val, old_cache["members"][key])

        return cached_data

    def _update_hdf_entry(self, new_cache: dict, old_cache: dict) -> None:
        # update core description
        new_cache['description'] = old_cache['description']

        # update core attrs
        oldattrs = [c['key'] for c in old_cache['attrs']]
        for item in new_cache['attrs']:
            if item['key'] in oldattrs:
                item['comment'] = old_cache['attrs'][oldattrs.index(item['key'])]['comment']

    def design_content(self, name: str = '/', description: str = None, hdftype: str = 'group',
                       attrs: list = None, ds_shape: tuple = None, ds_size: int = None, ds_dtype: str = None):
        """ Abstract method to be implemented by subclass, for designing file content

        _extended_summary_

        Parameters
        ----------
        name : str, optional
            _description_, by default '/'
        description : str, optional
            _description_, by default None
        hdftype : str, optional
            _description_, by default 'group'
        attrs : list, optional
            _description_, by default None
        ds_shape : tuple, optional
            _description_, by default None
        ds_size : int, optional
            _description_, by default None
        ds_dtype : str, optional
            _description_, by default None

        Raises
        ------
        ValueError
            _description_
        """
        if not self.design or (self.filename and os.path.exists(self.filename)):
            log.warning('Cannot design an new HDF5 member when not in the datamodel design phase or '
                        'if a real file already exists.')
            return

        cached_hdf = self._cache['releases']['WORK'][self.cache_key]

        # get the parent
        levels = name.rsplit('/', 1)[0]
        parent = '/' if not levels or '/' not in name else levels

        # if initial cache is empty, or name is the parent, create a top level group
        if not cached_hdf or name == '/':
            cached_hdf['name'] = name
            cached_hdf['parent'] = parent
            cached_hdf['object'] = 'group'
            cached_hdf['description'] = description or 'a parent group description'
            cached_hdf['libver'] = ('earliest', 'v112')
            cached_hdf['n_members'] = 0
            cached_hdf['attrs'] = self._design_attrs(attrs) or []
            cached_hdf['members'] = {}

        if hdftype not in ['group', 'dataset']:
            raise ValueError('Invalid HDF5 type specified.  Can only be "group" or "dataset".')

        # update any member entry
        member = None
        if name != '/':
            member = cached_hdf['members'].get(name, {})
            member['name'] = name
            member['parent'] = parent
            member['object'] = hdftype
            member['description'] = description or 'a group description'
            member['attrs'] = self._design_attrs(attrs) or []
            if hdftype == 'dataset':
                member['shape'] = ds_shape or (10,)
                member['size'] = ds_size or 10
                member['dtype'] = ds_dtype or 'S10'
                member['ndim'] = len(member['shape'])
            elif hdftype == 'group':
                member['n_members'] = 0

            cached_hdf['members'][name] = member

        # update the group n_members
        if parent == '/' and member:
            cached_hdf['n_members'] += 1
        elif parent in cached_hdf['members']:
            cached_hdf['members'][parent]['n_members'] += 1

        # update the cached hdf
        self._cache['releases']['WORK'][self.cache_key] = cached_hdf

    def _design_attrs(self, attrs: list) -> list:
        """ Convert a list of input attributes into valid YAML attrs format """
        if not attrs:
            return None

        if isinstance(attrs[0], (tuple, list)):
            return [dict(zip(("key", "value", "comment", "dtype"), i)) for i in attrs]
        elif isinstance(attrs[0], dict):
            if {"key", "value", "comment", "dtype"}.issubset(attrs[0]):
                return attrs
            return [{"key": k, "value": v, "comment": f"description for {k}"} for k, v in attrs[0].items()]

    def create_from_cache(self, release: str = 'WORK') -> h5py.File:
        """ Create a HDF5 file from the yaml cache

        Converts the hdfs dictionary entry in the YAML cache into
        a HDF5 h5py.File object.

        Parameters
        ----------
        release : str, optional
            the name of the data release, by default 'WORK'

        Returns
        -------
        h5py.File
            a valid h5py.File object

        Raises
        ------
        ValueError
            when the release is not in the cache
        ValueError
            when the release is not WORK when in the datamodel design phase
        """

        if release not in self._cache['releases']:
            raise ValueError(f'Release {release} not found in list of cached releases.')

        if self.design and release != 'WORK':
            raise ValueError(f'Release {release} can only be "WORK" when in the datamodel design phase.')

        hdfs = self._cache['releases'][release][self.cache_key]
        self._designed_object = HdfModel.parse_obj(hdfs).convert_hdf()
        return self._designed_object

    def write_design(self, file: str, overwrite: bool = None) -> None:
        """ Write out the designed file

        Write out a designed HDF5 object to a file on disk.  Must have run
        create_from_cache method first.

        Parameters
        ----------
        file : str
            The designed filename
        overwrite : bool, optional
            If True, overwrites any existing file, by default True

        Raises
        ------
        AttributeError
            when the designed object does not exit
        """
        # check if designed object is None, ("not designed_object" returns True for closed h5py.File)
        if self._designed_object is None:
            raise AttributeError('Cannot write.  Designed object does not exist.')

        # remove the existing file
        if overwrite and os.path.exists(file):
            os.remove(file)

        shutil.copy2(self._designed_object.temp_filename, file)
        os.remove(self._designed_object.temp_filename)

    def _create_attrs(self, h5obj: Union[h5py.Group, h5py.Dataset]) -> list:
        return [{'key': k,
                 'value': None if isinstance(v, h5py.Empty) else str(v.item()) if isinstance(v.item(), bytes) else v.item(),
                 'comment': 'replace me - with a description of this attribute',
                 'dtype': str(v.dtype),
                 'is_empty': isinstance(v, h5py.Empty),
                 'shape': v.shape}
                for k, v in h5obj.attrs.items()]

    def _create_dataset(self, name: str, h5obj: Union[h5py.Group, h5py.Dataset]) -> dict:
        return {
            "name": name,
            "parent": h5obj.parent.name,
            "object": "dataset",
            "description": "replace me - with a description of this dataset",
            "attrs": self._create_attrs(h5obj),
            "shape": h5obj.shape,
            "size": h5obj.size.item(),
            "ndim": h5obj.ndim,
            "dtype": str(h5obj.dtype),
            "nbytes": h5obj.nbytes.item(),
            "is_virtual": h5obj.is_virtual,
            "is_empty": isinstance(h5obj, h5py.Empty),
        }

    def _build_cache(self, name: str, h5obj: Union[h5py.Group, h5py.Dataset]):
        mem = self._hdf5data["members"]
        mem[name] = {"name": name, "parent": h5obj.parent.name}
        mem[name]["object"] = (
            "group"
            if isinstance(h5obj, h5py.Group)
            else "dataset"
            if isinstance(h5obj, h5py.Dataset)
            else "null"
        )
        if isinstance(h5obj, h5py.Group):
            mem[name]["description"] = "replace me - with a description of this group"
            mem[name]["n_members"] = len(h5obj)
        elif isinstance(h5obj, h5py.Dataset):
            mem[name] = self._create_dataset(name, h5obj)
        mem[name]["attrs"] = self._create_attrs(h5obj)
