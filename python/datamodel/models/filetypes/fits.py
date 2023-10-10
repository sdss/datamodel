# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import re

from typing import List, Union, Dict, Optional, Annotated
from pydantic import validator, Field, BeforeValidator
from astropy.io import fits
from ..base import CoreModel
from ..validators import replace_me


LaxStr = Annotated[str, BeforeValidator(lambda x: str(x))]


class ChangeFits(CoreModel):
    """ Pydantic model representing the FITS hdu fields of the YAML changelog release section

    Represents a computed section of the changelog, for the specified
    release.  Changelog is computed between the data products of release (key)
    and the release indicated in `from`.

    Parameters
    ----------
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
    delta_nhdus: int = None
    added_hdus: List[str] = Field(None, repr=False)
    removed_hdus: List[str] = Field(None, repr=False)
    primary_delta_nkeys: int = None
    added_primary_header_kwargs: List[str] = Field(None, repr=False)
    removed_primary_header_kwargs: List[str] = Field(None, repr=False)


class Header(CoreModel):
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
    value: Optional[LaxStr] = ''
    comment: str = Field(default='', repr=False)

    def to_tuple(self):
        """ Convert the header key to a tuple """
        return (self.key, int(self.value) if self.value.isdigit() else self.value, self.comment)


class Column(CoreModel):
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
    description: str = Field(..., repr=False)
    type: str
    unit: str = ''

    _check_replace_me = validator('unit', 'description')(replace_me)

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


class HDU(CoreModel):
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
    description: str = Field(..., repr=False)
    size: str
    header: List[Header] = Field(default=None, repr=False)
    columns: Optional[Dict[str, Column]] = Field(default=None, repr=False)

    _check_replace_me = validator('description')(replace_me)

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