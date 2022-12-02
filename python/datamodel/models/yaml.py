# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: yaml.py
# Project: models
# Author: Brian Cherinka
# Created: Friday, 2nd April 2021 2:28:24 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Friday, 2nd April 2021 2:28:24 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import, annotations

import re
from typing import List, Dict, Union

import orjson
from astropy.io import fits
from pydantic import BaseModel, validator

from .releases import releases, Release
from .surveys import surveys, Survey
from .validators import replace_me, check_release
from .filetypes import HDU, ParModel, HdfModel, ChangeFits, ChangePar, ChangeHdf


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default,
                        option=orjson.OPT_INDENT_2|
                        orjson.OPT_SERIALIZE_NUMPY).decode()

class GeneralSection(BaseModel):
    """ Pydantic model representing the YAML general section

    Parameters
    ----------
    name : str
        The file species name of the data product (or sdss_access path_name)
    short : str
        A one sentence summary of the data product
    description : str
        A longer description of the data product
    environments : List[str]
        A list of environment variables associated with the data product
    datatype : str
        The type of data product, e.g. FITS
    filesize : str
        An estimated size of the data product
    releases : List[str]
        A list of SDSS releases the data product is in
    naming_convention : str
        A description of the naming convention
    generated_by : str
        An identifiable piece of the code that generates the data product
    design : bool
        If True, the datamodel is in the design phase, before any file exists yet
    vac: bool
        True if the datamodel is a VAC

    Raises
    ------
    ValueError
        when any of the releases are not a valid SDSS Release
    """
    name: str
    short: str
    description: str
    environments: List[str] = None
    surveys: List[Union[str, Survey]] = None
    datatype: str
    filesize: str
    releases: List[Union[str, Release]] = None
    naming_convention: str
    generated_by: str
    design: bool = None
    vac: bool = None
    recommended_science_product: bool = None

    _check_replace_me = validator('short', 'description', 'naming_convention',
                                  'generated_by', allow_reuse=True)(replace_me)

    @validator('releases', each_item=True)
    def check_release(cls, value: str) -> str:
        """ Validator to check release against list of releases """
        if value not in releases:
            raise ValueError(f'{value} is not a valid release')
        return releases[value]

    @validator('design')
    def no_design(cls, value: bool):
        """ Validator to check if the design flag is set to True """
        if value:
            raise ValueError('Design is set to True. YAML will not validate until out of design phase.')
        return value

    @validator('surveys', each_item=True)
    def check_survey(cls, value: str):
        """ Validator to check survey against list of surveys """
        if value not in surveys:
            raise ValueError(f'{value} is not a valid survey')
        return surveys[value]

class ChangeBase(BaseModel):
    """ Base Pydantic model representing a YAML changelog release section"""
    from_: str
    note: str = None
    class Config:
        """ Pydantic model configuration """
        fields = {
            'from_': 'from'
        }

class ChangeRelease(ChangeHdf, ChangePar, ChangeFits, ChangeBase):
    """ Pydantic model representing a YAML changelog release section

    Represents a computed section of the changelog, for the specified
    release.  Changelog is computed between the data products of release (key)
    and the release indicated in `from`.

    Parameters
    ----------
    from_ : str
        The release the changelog is computed from
    delta_nhdus : int
        The difference in number of HDUs
    added_hdus : List[str]
        A list of any added HDUs
    removed_hdus : List[str]
        A list of any removed HDUs
    primary_delta_nkeys : int
        The difference in primary header keywords
    added_primary_header_kwargs : List[str]
        A list of any added primary header keywords
    removed_primary_header_kwargs : List[str]
        A list of any removed primary header keywords
    delta_nkeys : int
        The difference in number of Yanny header keys
    added_header_keys : List[str]
        A list of any added Yanny header keywords
    removed_header_keys : List[str]
        A list of any removed Yanny header keywords
    delta_tables : int
        The difference in number of Yanny tables
    added_tables : List[str]
        A list of any added Yanny tables
    removed_tables : List[str]
        A list of any removed Yanny tables
    tables : Dict[str, ChangeTable]
        A dictionary of table column and row changes
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

class ChangeLog(BaseModel):
    """ Pydantic model representing the YAML changelog section

    Parameters
    ----------
    description : str
        A description of the changelog
    releases : Dict[str, `.ChangeRelease`]
        A dictionary of the file changes between the given release and previous one
    """
    description: str
    releases: Dict[str, ChangeRelease] = None

    _check_releases = validator('releases', allow_reuse=True)(check_release)

    def json(self, **kwargs):
        """ override json method to exclude none fields by default """
        kwargs.pop('exclude_none', None)
        return super().json(exclude_none=True, **kwargs)

    def dict(self, **kwargs):
        """ override dict method to exclude none fields by default

        Need to override this method as well when serializing YamlModel to json,
        because nested models are already converted to dict when json.dumps is called.
        See https://github.com/samuelcolvin/pydantic/issues/1778

        """
        kwargs.pop('exclude_none', None)
        return super().dict(exclude_none=True, **kwargs)

class Access(BaseModel):
    """ Pydantic model representing the YAML releases access section

    Parameters
    ----------
    in_sdss_access : bool
        Whether or not the data product has an sdss_access entry
    path_name : str
        The path name in sdss_access for the data product
    path_template : str
        The path template in sdss_access for the data product
    path_kwargs : List[str]
        A list of path keywords in the path_template for the data product
    access_string : str
        The full sdss_access entry, "path_name=path_template"
    """
    in_sdss_access: bool
    path_name: str = None
    path_template: str = None
    path_kwargs: List[str] = None
    access_string: str = None

    @validator('path_name', 'path_template', 'access_string')
    def check_path_nulls(cls, value, values, field):
        in_access = values.get('in_sdss_access')
        if in_access and not value:
            raise ValueError(f'{field.name} cannot be None if in_sdss_access is True')
        return value

    @validator('path_kwargs')
    def check_path_kwargs(cls, value, values):
        in_access = values.get('in_sdss_access')
        path = values.get('path_template')
        needskwargs = re.findall("{(.*?)}", path) if path else None
        if in_access and needskwargs and not value:
            raise ValueError('path_kwargs cannot be None if path_template has {} kwargs')
        return value

class ReleaseModel(BaseModel):
    """ Pydantic model representing an item in the YAML releases section

    Contains any information on the data product that is specific to a given
    release, or that changes across releases.

    Parameters
    ----------
    template : str
        The full template representation of the path to the data product
    example : str
        A real example path of the data product
    location : str
        The symbolic location of the data product
    environment : str
        The SAS environment variable the product lives under
    access : `.Access`
        Information on any relevant sdss_access entry
    hdus : Dict[str, `.HDU`]
        A dictionary of HDU content for the product for the given release
    """
    template: str
    example: str
    location: str
    environment: str
    survey: str = None
    access: Access
    hdus: Dict[str, HDU] = None
    par: ParModel = None
    hdfs: HdfModel = None

    def convert_to_hdulist(self) -> fits.HDUList:
        """ Convert the hdus to a fits.HDUList """
        hdus = [HDU.parse_obj(v).convert_hdu() for v in self.hdus.values()]
        return fits.HDUList(hdus)


class YamlModel(BaseModel):
    """ Pydantic model representing a YAML file

    Parameters
    ----------
    general : `.GeneralSection`
        The general metadata section of the datamodel
    changelog : `.ChangeLog`
        An automated log of data product changes across releases
    releases : Dict[str, `.ReleaseModel`]
        A dictionary of information specific to that release
    notes : str
        A string or multi-line text blob of additional information

    """
    general: GeneralSection
    changelog: ChangeLog
    releases: Dict[str, ReleaseModel]
    notes: str = None

    _check_releases = validator('releases', allow_reuse=True)(check_release)

    class Config:
        """ Pydantic custom config """
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ProductModel(YamlModel):
    """ Pydantic model representing a data product JSON file

    Parameters
    ----------
    general : `.GeneralSection`
        The general metadata section of the datamodel
    changelog : `.ChangeLog`
        An automated log of data product changes across releases
    releases : Dict[str, `.ReleaseModel`]
        A dictionary of information specific to that release
    """
    class Config:
        """ Pydantic custom config """
        json_loads = orjson.loads
        json_dumps = orjson_dumps

