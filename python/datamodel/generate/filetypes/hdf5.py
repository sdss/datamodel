# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from typing import Union
from datamodel import log
from .base import BaseFile

import h5py

class HdfFile(BaseFile):
    """ Class for supporting HDF5 files """
    suffix = 'H5'
    cache_key = 'hdfs'
    _hdf5data = None

    def _generate_new_cache(self) -> dict:
        """ Generates the new cache for an HDF5 file """
        with h5py.File(self.filename, "r") as data:
            self._hdf5data = {"name": data.name, "parent": data.parent.name, "object": "group",
                              "description": "replace me - with a description of this group",
                              "libver": data.libver, "n_members": len(data),
                              "attrs": self._create_attrs(data.name, data), "members": {}}
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

    def design_content(self):
        """ Abstract method to be implemented by subclass, for designing file content """
        pass

    def create_from_cache(self, release: str = 'WORK') -> h5py.File:
        """ Abstract method to be implemented by subclass, for creating a valid object from cache """
        pass

    def write_design(self, file: str, overwrite: bool = None) -> None:
        """ Abstract method to be implemented by subclass, for writing a design to a file """
        pass

    def _create_attrs(self, name: str, h5obj: Union[h5py.Group, h5py.Dataset]) -> list:
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
            "attrs": self._create_attrs(name, h5obj),
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
        mem[name]["attrs"] = self._create_attrs(name, h5obj)
