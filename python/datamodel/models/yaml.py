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

import orjson
from typing import List, Dict
from pydantic import BaseModel, validator

from .releases import releases


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default, 
                        option=orjson.OPT_INDENT_2|
                        orjson.OPT_SERIALIZE_NUMPY).decode()


def replace_me(value: str) -> str:
    """ Validator for datamodel text fields

    Validator for yaml fields where the string values have the text
    "replace me" within it.  This text indicates a template text that
    must be replaced.

    Parameters
    ----------
    value : str
        the value of the field

    Returns
    -------
    str
        the value of the field

    Raises
    ------
    ValueError
        when "replace me" is the in the value text
    """
    if 'replace me' in value:
        raise ValueError('Generic text needs to be replaced with specific content!')
    return value


def check_release(value: dict) -> str:
    """ Validator for datamodel release keys

    Validator for yaml "releases" fields.  Checks the "releases" keys against
    valid SDSS releases, from the Releases Model.

    Parameters
    ----------
    value : dict
        the value of the field

    Returns
    -------
    str
        the value of the field

    Raises
    ------
    ValueError
        when the release key is not a valid release
    """
    rr = [i.name for i in releases]
    badkeys = set(value.keys()) - set(rr)
    if badkeys:
        raise ValueError(f"Invalid key(s) {','.join(badkeys)} in releases dict.")
    return value

class GeneralSection(BaseModel):
    """ Pydantic model representing the YAML general section """
    name: str
    short: str
    description: str
    environments: List[str] = None
    datatype: str
    filesize: str
    releases: List[str] = None
    naming_convention: str
    generated_by: str

    _check_replace_me = validator('short', 'description', 'naming_convention',
                                  'generated_by', allow_reuse=True)(replace_me)

    @validator('releases', each_item=True)
    def check_release(cls, value: str) -> str:
        if value not in releases:
            raise ValueError(f'{value} is not a valid release')
        return value

class ChangeRelease(BaseModel):
    """ Pydantic model representing a YAML changelog release section """
    from_: str
    delta_nhdus: int = None
    added_hdus: List[str] = None
    removed_hdus: List[str] = None
    primary_delta_nkeys: int = None
    added_primary_header_kwargs: List[str] = None
    removed_primary_header_kwargs: List[str] = None
    note: str = None

    class Config:
        fields = {
            'from_': 'from'
        }

class ChangeLog(BaseModel):
    """ Pydantic model representing the YAML changelog section """
    description: str
    releases: Dict[str, ChangeRelease] = None

    _check_releases = validator('releases', allow_reuse=True)(check_release)


class Access(BaseModel):
    """ Pydantic model representing the YAML releases access section """
    in_sdss_access: bool
    path_name: str
    path_template: str
    path_kwargs: List[str]
    access_string: str

class Header(BaseModel):
    """ Pydantic model representing a YAML header section """
    key: str
    value: str
    comment: str


class Column(BaseModel):
    """ Pydantic model representing a YAML column section """
    name: str
    description: str
    type: str
    unit: str

    _check_replace_me = validator('unit', 'description', allow_reuse=True)(replace_me)


class HDU(BaseModel):
    """ Pydantic model representing a YAML hdu section """
    name: str
    is_image: bool
    description: str
    size: str
    header: List[Header] = None
    columns: Dict[str, Column] = None

    _check_replace_me = validator('description', allow_reuse=True)(replace_me)


class Release(BaseModel):
    """ Pydantic model representing a YAML releases section """
    template: str
    example: str
    location: str
    environment: str
    access: Access
    hdus: Dict[str, HDU] = None


class YamlModel(BaseModel):
    """ Pydantic model representing a YAML file """
    general: GeneralSection
    changelog: ChangeLog
    releases: Dict[str, Release]

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
        stuff
    changelog : `.ChangeLog`
        An automated 
    releases : Dict[str, `.Release`]
        stuff
    """
    class Config:
        """ Pydantic custom config """
        json_loads = orjson.loads
        json_dumps = orjson_dumps

