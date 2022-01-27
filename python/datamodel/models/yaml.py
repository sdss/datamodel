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
import re
from typing import List, Dict, Union
from pydantic import BaseModel, validator

from astropy.io import fits
from .releases import releases, Release as ReleaseMod


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
    design : bool
        If True, the datamodel is in the design phase, before any file exists yet

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
    releases: List[Union[str, ReleaseMod]] = None
    naming_convention: str
    generated_by: str
    design: bool = None

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
        needskwargs = re.findall("{(.*?)}", path)
        if in_access and needskwargs and not value:
            raise ValueError('path_kwargs cannot be None if path_template has {} kwargs')
        return value

class Header(BaseModel):
    """ Pydantic model representing a YAML header section

    Represents an individual FITS Header Key

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
    value: str = ''
    comment: str = ''
    
    def to_tuple(self):
        """ Convert the header key to a tuple """
        return (self.key, int(self.value) if self.value.isdigit() else self.value, self.comment)

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
    
    def to_fitscolumn(self) -> fits.Column:
        """ Convert the column to a fits.Column

        Converts the column entry in the yaml file to an 
        Astropy fits.Column object.  Performs a mapping between ``type`` 
        and ``format``, using the reverse of `.datamodel.generate.stub.Stub._format_type`.

        Returns
        -------
        fits.Column
            a valid astropy fits.Column object

        Raises
        ------
        TypeError
            when the column type cannot be coerced into a valid fits.Column format
        """
        tmap = {'char': 'A', 'int16': 'I', 'int32': 'J', 'int64': 'K', 
                'float32': 'E', 'float64': 'D', 'bool': 'L'}
        
        # regex search for the type
        patt = re.compile(r'(?P<dtype>char|bool|int\d{2}|float\d{2})(?P<charlength>\[(?P<charnum>\d+)\])?')
        match = re.search(patt, self.type)
        if match:
            col = match.groupdict()
            # convert the type to corresponding format
            if col['dtype'] == 'char':
                format = f"{col['charnum']}{tmap[col['dtype']]}"
            else:
                format = f"{tmap[col['dtype']]}"
            return fits.Column(name=self.name, format=format, unit=self.unit)
        else:
            raise TypeError(f'The column type {self.type} could not be properly coerced. '
                            'Check for a valid fits.Column format.') 


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
    
    def convert_header(self) -> fits.Header:
        """ Convert the list of header keys into a fits.Header """
        if not self.header:
            return None
        return fits.Header(i.to_tuple() for i in self.header)
    
    def convert_columns(self) -> List[fits.Column]:
        """ Convert the columns dict into a a list of fits.Columns """
        if not self.columns:
            return None
        return [i.to_fitscolumn() for i in self.columns.values()]
    
    def convert_hdu(self) -> Union[fits.PrimaryHDU, fits.ImageHDU, fits.BinTableHDU]:
        """ Convert the HDU entry into a valid fits.HDU """
        if self.name.lower() == 'primary':
            return fits.PrimaryHDU(header=self.convert_header())
        elif self.columns:
            return fits.BinTableHDU.from_columns(self.convert_columns(), name=self.name, 
                                                 header=self.convert_header())
        else:
            return fits.ImageHDU(name=self.name, header=self.convert_header())

class ParColumn(BaseModel):
    """ Pydantic model representing a YAML par column section

    Represents a typedef column definition in a Yanny parameter file
    
    Parameters
    ----------
    name : str
        The name of the column
    description : str
        A description of the column
    type : str
        The data type of the column
    unit : str
        The unit of the column, if any
    is_array : bool
        If the column is an array type
    is_enum : bool
        If the column is an enum type
    example : str
        An example value for the column
    """
    name: str
    type: str
    description: str
    unit: str
    is_array: bool
    is_enum: bool
    example: Union[str, int, float, list]
    
    _check_replace_me = validator('unit', 'description', allow_reuse=True)(replace_me)

class ParTable(BaseModel):
    """ Pydantic model representing a YAML par table section

    Represents the structure of a single Yanny parameter table

    Parameters
    ----------
    name : str
        The name of the table
    description : str 
        A description of the table
    n_rows : int
        The number of rows in the table
    structure : list
        A list of column definitions for the table
    """
    name: str
    description: str
    n_rows: int
    structure: List[ParColumn]
    
    _check_replace_me = validator('description', allow_reuse=True)(replace_me)


class ParModel(BaseModel):
    """ Pydantic model representing a YAML par section

    Represents a Yanny parameter file

    Parameters
    ----------
    comments : str
        Any header comments in the parameter file
    header : list
        A list of header key-value pairs in the parameter file
    tables : dict
        A dictionary of tables in the parameter file
    """
    comments: str = None
    header: List[Header] = None
    tables: Dict[str, ParTable]       

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
    par: ParModel = None
    
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

