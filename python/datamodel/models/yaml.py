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

    Raises
    ------
    ValueError
        when any of the releases are not a valid SDSS Release 
    """
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
    """
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
    path_name: str
    path_template: str
    path_kwargs: List[str]
    access_string: str

class Header(BaseModel):
    """ Pydantic model representing a YAML header section

    Represents a FITS Header

    Parameters
    ----------
    key : str
        The name of the header keyword
    value : str
        The value of the header keyword
    comment : str
        A comment for the header keyword, if any
    """
    key: str
    value: str
    comment: str


class Column(BaseModel):
    """ Pydantic model representing a YAML column section

    Represents a FITS binary table column 
    
    Parameters
    ----------
    name : str
        The name of the table column
    description : str
        A description of the table column
    type : str
        The data type of the table column
    unit : str
        The unit of the table column
    """
    name: str
    description: str
    type: str
    unit: str

    _check_replace_me = validator('unit', 'description', allow_reuse=True)(replace_me)


class HDU(BaseModel):
    """ Pydantic model representing a YAML hdu section

    Represents a FITS HDU extension
    
    Parameters
    ----------
    name : str
        The name of the HDU extension
    is_image : bool
        Whether the HDU is an image extension
    description : str
        A description of the HDU extension
    size : str
        An estimated size of the HDU extension
    header : List[`.Header`]
        A list of header values for the extension
    columns : Dict[str, `.Column`]
        A list of any binary table columns for the extension
    """
    name: str
    is_image: bool
    description: str
    size: str
    header: List[Header] = None
    columns: Dict[str, Column] = None

    _check_replace_me = validator('description', allow_reuse=True)(replace_me)


class Release(BaseModel):
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
    access: Access
    hdus: Dict[str, HDU] = None


class YamlModel(BaseModel):
    """ Pydantic model representing a YAML file 

    Parameters
    ----------
    general : `.GeneralSection`
        The general metadata section of the datamodel
    changelog : `.ChangeLog`
        An automated log of data product changes across releases
    releases : Dict[str, `.Release`]
        A dictionary of information specific to that release

    """
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
        The general metadata section of the datamodel
    changelog : `.ChangeLog`
        An automated log of data product changes across releases
    releases : Dict[str, `.Release`]
        A dictionary of information specific to that release
    """
    class Config:
        """ Pydantic custom config """
        json_loads = orjson.loads
        json_dumps = orjson_dumps

