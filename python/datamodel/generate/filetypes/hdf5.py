# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from typing import Union
from datamodel import log
from .base import BaseFile

from datamodel.models.yaml import HdfModel

import os
import shutil
import numpy as np

try:
    import h5py
except ImportError:
    h5py = h5types = h5file = None
else:
    # specify type annotations
    h5types = Union[h5py.Group, h5py.Dataset]
    h5file = h5py.File

class HdfFile(BaseFile):
    """ Class for supporting HDF5 files """
    suffix = 'H5'
    aliases = ['HDF5']
    cache_key = 'hdfs'
    _hdf5data = None

    def _generate_new_cache(self) -> dict:
        """ Generates the new cache for an HDF5 file """

        if not h5py:
            raise ImportError('Generating datamodels for HDF5 files requies the h5py package installed.')

        with h5py.File(self.filename, "r") as data:
            pytables = "PYTABLES_FORMAT_VERSION" in data.attrs
            self._hdf5data = {"name": data.name, "parent": data.parent.name, "object": "group",
                              "description": "replace me - with a description of this group",
                              "libver": data.libver, "n_members": len(data), 'pytables': pytables,
                              "attrs": self._create_attrs(data), "members": {}}
            # traverse the HDF5 hierarchy
            data.visititems(self._build_cache)
            return self._hdf5data

    def _build_cache(self, name: str, h5obj: h5types):
        """ Build the Yaml cache from a HDF5 object """
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

    def _create_attrs(self, h5obj: h5types) -> list:
        """ Convert HDF5 attributes to a list of YAML attr dicts """
        return [{'key': k,
                 'value': self._parse_attr_value(v),
                 'comment': 'replace me - with a description of this attribute',
                 'dtype': self._parse_attr_value(v, field='dtype'),
                 'is_empty': isinstance(v, h5py.Empty),
                 'shape': self._parse_attr_value(v, field='shape')}
                for k, v in h5obj.attrs.items()]

    @staticmethod
    def _parse_attr_value(value, field: str = 'value'):
        """ Parse an HDF5 attribute value """
        # convert to numpy type if needed - useful for test data
        if not isinstance(value, np.generic):
            value = np.dtype(type(value)).type(value)

        # return the dtype, shape, or value of the numpy object
        if field == 'dtype':
            return str(value.dtype)
        elif field == 'shape':
            return value.shape
        else:
            if isinstance(value, h5py.Empty):
                return None
            elif isinstance(value, np.generic):
                return str(value.item()) if isinstance(value.item(), bytes) else value.item()
            else:
                return value

    def _create_dataset(self, name: str, h5obj: h5types) -> dict:
        """ Convert HDF5 dataset to a YAML dataset dict """
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

    def _update_partial_cache(self, cached_data: dict, old_cache: dict) -> dict:
        """ Updates the partial cache for HDF5 files

        Parameters
        ----------
        cached_data : dict
            The new cache to update
        old_cache : dict
            The old cache to pull info from

        Returns
        -------
        dict :
            The updated cached data
        """

        # update the root level cache
        self._update_hdf_entry(cached_data, old_cache)

        # update core members
        for key, val in cached_data['members'].items():
            if key in old_cache["members"]:
                self._update_hdf_entry(val, old_cache["members"][key])

        return cached_data

    def _update_hdf_entry(self, new_cache: dict, old_cache: dict) -> None:
        """ Updates the cache entry for an HDF5 member

        Parameters
        ----------
        new_cache : dict
            The new YAML cache to update
        old_cache : dict
            The old YAML to pull info from
        """
        # update core description
        new_cache['description'] = old_cache['description']

        # update core attrs
        oldattrs = [c['key'] for c in old_cache['attrs']]
        for item in new_cache['attrs']:
            if item['key'] in oldattrs:
                item['comment'] = old_cache['attrs'][oldattrs.index(item['key'])]['comment']

    def design_content(self, name: str = '/', description: str = None, hdftype: str = 'group',
                       attrs: list = None, ds_shape: tuple = None, ds_dtype: str = None):
        """ Design a new HDF5 section for the datamodel

        Design a new HDF entry for the given datamodel.  Specify h5py groups or dataset definitions,
        with optional list of attributes.  Each new entry is added to the members entry in the
        YAML structure.  Use ``name``, and ``description`` to specify the name and description of each new
        group or dataset the new table.  Use ``hdftype`` to specify a "group" or "dataset" entry.  For
        datasets, use ``ds_shape``, ``ds_size``, and ``ds_dtype`` to specify the shape, size, and
        dtype of the array dataset.

        New HDF5 members are added to the datamodel in a flattened structure.  To add a new group or dataset
        as a child to an existing group, specify the full path in ``name``, e.g ``/mygroup/mydataset``.

        ``attrs`` can be a list of tuples of header keywords,
        conforming to (key, value, comment, dtype), or list of dictionaries conforming to
        {"key": key, "value": value, "comment": comment, "dtype": dtype}.

        Allowed attribute or dataset dtypes are any valid string representation of numpy dtypes.  For
        example, "<i8", "int32", "S10", etc.

        Parameters
        ----------
        name : str, optional
            the name of the HDF group or dataset, by default '/'
        description : str, optional
            a description of the HDF group or dataset, by default None
        hdftype : str, optional
            the type of HDF5 object, by default 'group'
        attrs : list, optional
            a list of HDF5 Attributes, by default None
        ds_shape : tuple, optional
            the shape of an HDF5 array dataset, by default None
        ds_dtype : str, optional
            the dtype of an HDF5 array dataset, by default None

        Raises
        ------
        ValueError
            when an invalid hdftype is specified
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
            hdf5ver = f"v{h5py.version.hdf5_version.rsplit('.',1)[0].replace('.','')}" if h5py else 'v112'
            cached_hdf['libver'] = ('earliest', hdf5ver)
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
                member['size'] = np.prod(member['shape']).item()
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
            return [dict(zip(("key", "value", "comment", "dtype", "shape"), i)) for i in attrs]
        elif isinstance(attrs[0], dict):
            if {"key", "value", "comment", "dtype"}.issubset(attrs[0]):
                return attrs
            return [{"key": k, "value": v, "comment": f"description for {k}"} for k, v in attrs[0].items()]

    @staticmethod
    def _get_designed_object(data: dict):
        """ Return a valid h5py File

        Parses and validates the hdfs YAML cache into a proper Pydantic model
        and converts the model into an h5py.File object.  The object is closed, with
        the file object written to a temporary file, and the name saved as ``temp_filename``
        attribute on the object.

        Parameters
        ----------
        data : dict
            The hdfs cache

        Returns
        -------
        h5py.File
            A valid h5py.File object
        """
        return HdfModel.model_validate(data).convert_hdf()

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

