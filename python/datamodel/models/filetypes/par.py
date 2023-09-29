# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import re
from typing import List, Union, Dict
from pydantic import validator, Field
from ..base import CoreModel
from ..validators import replace_me
from .fits import Header

try:
    from pydl.pydlutils.yanny import yanny
except ImportError:
    yanny = None


class ChangeTable(CoreModel):
    """ Pydantic model representing a YAML changelog Yanny table section

    Represents a computed section of the changelog, for a specific Yanny table.
    For each similar Yanny table between releases, the changes in row number
    and structure columns are computed.

    Parameters
    ----------
    delta_nrows : int
        The difference in rows between Yanny tables
    added_cols : List[str]
        A list of any added Yanny table columns
    removed_cols : List[str]
        A list of any removed Yanny table columns
    """
    delta_nrows: int = None
    added_cols: List[str] = Field(None, repr=False)
    removed_cols: List[str] = Field(None, repr=False)


class ChangePar(CoreModel):
    """ Pydantic model representing the Yanny par fields of the YAML changelog release section

    Represents a computed section of the changelog, for the specified
    release.  Changelog is computed between the data products of release (key)
    and the release indicated in `from`.

    Parameters
    ----------
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
    """
    delta_nkeys: int = None
    addead_header_keys: List[str] = Field(None, repr=False)
    removed_header_keys: List[str] = Field(None, repr=False)
    delta_ntables: int = None
    addead_tables: List[str] = Field(None, repr=False)
    removed_tables: List[str] = Field(None, repr=False)
    tables: Dict[str, ChangeTable] = None


class ParColumn(CoreModel):
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
    is_array: bool = Field(..., repr=False)
    is_enum: bool = Field(..., repr=False)
    enum_values: list = Field(None, repr=False)
    example: Union[str, int, float, list] = Field(..., repr=False)

    _check_replace_me = validator('unit', 'description', allow_reuse=True)(replace_me)

    def parse_type(self):
        """ Parse the yanny YAML column type """
        match = re.match(r"(?P<type>\w+)(?P<size>\[\d+\])?", self.type).groupdict()
        return f"{match['type']} {self.name}{match['size'] or ''}"


class ParTable(CoreModel):
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
    structure: List[ParColumn] = Field(..., repr=False)

    _check_replace_me = validator('description', allow_reuse=True)(replace_me)

    def create_typedef(self):
        """ Create a Yanny typedef struct string """
        cols = " ".join([f"\n\t\t{c.parse_type()};" for c in self.structure])
        return f"typedef struct {{{ cols }\n}} {self.name};"

    def create_enum(self):
        """ Create a Yanny typedef enum string """
        enum = []
        for c in self.structure:
            # do only when column is an enum
            if not c.is_enum:
                continue

            # do only when there are enum values present
            if not c.enum_values:
                continue

            # create enum definiton
            names = "".join([f"\n\t{v};" for v in c.enum_values])
            enum.append(f"typedef enum {{{ names }\n}} {c.type};")
        return enum

    def convert_table(self):
        """ Create a dictionary to prepare a Yanny table """
        table = {'symbols': {'enum': self.create_enum(),
                             'struct': self.create_typedef(),
                             self.name: [c.name for c in self.structure]}
                 }
        table[self.name] = {c.name: [c.example] for c in self.structure}
        return table


class ParModel(CoreModel):
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
    comments: str = Field(None, repr=False)
    header: List[Header] = Field(None, repr=False)
    tables: Dict[str, ParTable]

    def convert_header(self) -> dict:
        """ Convert the header into a dicionary """
        return {i.key: i.value for i in self.header}

    def convert_par(self):
        """ Convert the YAML par section into a Yanny par object """
        if not yanny:
            raise ImportError('Converting YAML par sections to Yanny files requires the pydl package installed.')

        # create a blank Yanny structure
        tmp = yanny()
        # add generic content so yanny is not None
        tmp._contents = "#%yanny"
        # add header info
        tmp.update(self.convert_header())
        # add defaults symbols
        tmp._symbols["enum"] = []
        tmp._symbols["struct"] = []
        # add table data
        for tname, tdata in self.tables.items():
            tt = tdata.convert_table()
            tmp[tname] = tt[tname]
            tmp._symbols[tname] = tt["symbols"][tname]
            tmp._symbols["struct"].append(tt["symbols"]["struct"])
            tmp._symbols["enum"].extend(tt["symbols"]["enum"])
        return tmp
