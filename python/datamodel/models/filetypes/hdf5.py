# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import tempfile
import numpy as np
from enum import Enum
from typing import List, Union, Dict, Optional
from pydantic import validator, root_validator, Field
from ..base import CoreModel
from ..validators import replace_me

try:
    import h5py
except ImportError:
    h5py = None



class ChangeMember(CoreModel):
    """ Pydantic model representing a YAML changelog HDF5 member section

    Represents a computed section of the changelog, for a specific HDF member.
    For each similar HDF5 member between releases, the changes in member number,
    attributes, and dataset dimensions, size and shape are computed.

    Parameters
    ----------
    delta_nmembers : int
        The difference in member number between HDF5 groups
    delta_nattrs : int
        The difference in attribute number between HDF5 members
    added_attrs : List[str]
        A list of any added HDF5 Attributes
    removed_attrs : List[str]
        A list of any removed HDF5 Attributes
        The difference in dataset dimension number between HDF5 members
    new_shape : int
        The difference in dataset shape between HDF5 members
    delta_size : int
        The difference in dataset size between HDF5 members
    """
    delta_nmembers: int = None
    delta_nattrs: int = None
    added_attrs: List[str] = Field(None, repr=False)
    removed_attrs: List[str] = Field(None, repr=False)
    delta_ndim: int = None
    new_shape: tuple = Field(None, repr=False)
    delta_size: int = None


class ChangeHdf(CoreModel):
    """ Pydantic model representing the HDF5 fields of the YAML changelog release section

    Represents a computed section of the changelog, for the specified
    release.  Changelog is computed between the data products of release (key)
    and the release indicated in `from`.

    Parameters
    ----------
    new_libver : tuple
        The difference in HDF5 library version
    delta_nattrs : int
        The difference in the number of HDF5 Attributes
    added_attrs : List[str]
        A list of any added HDF5 Attributes
    removed_attrs : List[str]
        A list of any removed HDF5 Attributes
    delta_nmembers : int
        The difference in number members in HDF5 file
    added_members : List[str]
        A list of any added HDF5 groups or datasets
    removed_members : List[str]
        A list of any removed HDF5 groups or datasets
    members : Dict[str, ChangeMember]
        A dictionary of HDF5 group/dataset member changes
    """
    new_libver: tuple = None
    delta_nattrs: int = None
    addead_attrs: List[str] = Field(None, repr=False)
    removed_attrs: List[str] = Field(None, repr=False)
    delta_nmembers: int = None
    addead_members: List[str] = Field(None, repr=False)
    removed_members: List[str] = Field(None, repr=False)
    members: Dict[str, ChangeMember] = None



class HdfAttr(CoreModel):
    """ Pydantic model representing a YAML hdfs attrs section

    Represents the Attributes of an HDF5 file.  Each group or dataset has a
    set of attributes (attrs), which contains metadata about the group or dataset.

    Parameters
    ----------
    key : str
        The name of the attribute
    value : str
        The value of the attribute
    comment : str
        A description of the attribute
    dtype : str
        The numpy dtype of the attribute
    is_empty : bool
        If the attribute is an HDF5 Empty atribute
    shape : tuple
        The shape of the attribute, if any
    """
    key: str
    value: Union[str, int, float, bool] = None
    comment: str = Field(..., repr=False)
    dtype : str = Field(..., repr=False)
    is_empty: bool = Field(None, repr=False)
    shape: Optional[tuple] = Field(default_factory=(), repr=False)

    _check_replace_me = validator('comment', allow_reuse=True)(replace_me)

    @root_validator
    def check_value(cls, values):
        is_empty, shape, value = values.get('is_empty'), values.get('shape'), values.get('value')
        if not is_empty and (value is None or shape is None):
            errfield = 'value' if value is None else 'shape'
            raise ValueError(f'attrs field "{errfield}" cannot be none')
        return values


class HdfEnum(str, Enum):
    """ Pydantic Enum for HDF5 Group or Dataset """
    group = 'group'
    dataset = 'dataset'


class HdfBase(CoreModel):
    """ Base Pydantic model representing a YAML hdfs section

    Represents  of an HDF5 file.  Each group or dataset has a
    set of attributes (attrs), which contains metadata about the group or dataset.

    Parameters
    ----------
    name : str
        The name of the attribute
    parent : str
        The value of the attribute
    object : str
        A description of the attribute
    description : str
        The numpy dtype of the attribute
    pytables : bool
        Flag is object is a PyTables object
    attrs : list
        If the attribute is an HDF5 Empty object
    """
    name: str
    parent: str
    object: HdfEnum = Field(..., repr=False)
    description: str
    pytables : bool = None
    attrs: List[HdfAttr] = Field(default_factory=[], repr=False)

    _check_replace_me = validator('description', allow_reuse=True)(replace_me)


class HdfGroup(HdfBase):
    """ Pydantic model representing a YAML HDF Group section

    Represents a Group of an HDF5 file.

    Parameters
    ----------
    n_members : int
        The number of members in the group
    """
    n_members: int


class HdfDataset(HdfBase):
    """ Pydantic model representing a YAML HDF Dataset section

    Represents a Dataset of an HDF5 file.

    Parameters
    ----------
    shape : tuple
        The dimensional shape of the dataset
    size : int
        The size or number or elements in the dataset
    ndim : int
        The number of dimensions in the dataset
    dtype : str
        The numpy dtype of the dataset
    nbytes : int
        The number of bytes in the dataset
    is_virutal : bool
        Whether the dataset is virtual
    is_empty : bool
        Whether the dataset is an HDF5 Empty object
    """
    shape: tuple
    size: int
    ndim: int
    dtype: str
    nbytes: int = None
    is_virtual: bool = Field(None, repr=False)
    is_empty: bool = Field(None, repr=False)


class HdfModel(HdfGroup, smart_union=True):
    """ Pydantic model representing a YAML hfds section

    Represents a base HDF5 file, which is also an HDF5 Group.
    See HdfGroup, HdfDataset, and HdfBase Moodels for more information on
    the fields.

    Parameters
    ----------
    libver : tuple
        The HDF5 library version used to create the file
    members : dict
        All groups and datasets in the HDF5 file
    """
    libver: tuple = []
    members: Dict[str, Union[HdfGroup, HdfDataset]] = Field(default_factory={}, repr=False)

    def _create_attrs(self, hdf, attrs):
        for attr in attrs:
            if attr.is_empty:
                hdf.attrs.create(attr.key, h5py.Empty(attr.dtype))
            else:
                hdf.attrs.create(attr.key, attr.value, shape=attr.shape, dtype=np.dtype(attr.dtype))

    def convert_hdf(self):
        """ Convert the hdfs to a h5py.File """
        if not h5py:
            raise ImportError('Converting YAML hdf sections to HDF5 files requires the h5py package installed.')

        with tempfile.NamedTemporaryFile(delete=False) as ntf:
            new = h5py.File(ntf, 'a', libver=self.libver)
            new.temp_filename = ntf.name

            self._create_attrs(new, self.attrs)

            for v in self.members.values():
                if v.object == "group":
                    new.create_group(v.name)
                elif v.object == "dataset":
                    new.create_dataset(v.name, v.shape, dtype=np.dtype(v.dtype))
                self._create_attrs(new[v.name], v.attrs)
            new.close()
        return new
