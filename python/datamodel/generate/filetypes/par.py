# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import numpy as np
import yaml
import os
import re

from typing import Union

try:
    from pydl.pydlutils.yanny import yanny
except ImportError:
    yanny = None

from datamodel import log
from datamodel.models.yaml import ParModel
from .base import BaseFile

#
# used to output a string as a literal scalar string block in the YAML file
# usually indicated with "|", e.g. "key: |".  This preserves the block nature of
# a string broken up across multiple lines, ("\n")
#
class literal(str):
    pass

def literal_presenter(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")

yaml.add_representer(literal, literal_presenter)


class ParFile(BaseFile):
    """ Class for supporting Yanny par files """
    suffix = 'PAR'
    cache_key = 'par'

    def __init__(self, *args, **kwargs):
        super(ParFile, self).__init__(*args, **kwargs)

        if not yanny:
            raise ImportError('Generating datamodels for Yanny par files requies the pydl package installed.')

        # read the par file
        self._par = yanny(self.filename)

    def _generate_header(self) -> list:
        """ Generate a new header section of the Yanny cache

        Creates a list of any header keywords found in the Yanny par file.
        Returns each entry with key name, value, and comment.

        Returns
        -------
        list
            A list of header keywords
        """
        head = []
        for key in self._par.pairs():
            out = {'key': key, 'value': self._par[key], 'comment': 'replace me - with a description of this header keyword'}
            head.append(out)
        return head

    def _generate_comments(self) -> str:
        """ Generate a new comments section of the Yanny cache

        Extracts any commented lines of a Yanny par file and returns them as
        a literal scalar block.  Only the comment (#) lines before the "typedef" definition
        in a Yanny file are returned.  Returns as a literal block for formatting purposes
        in the output YAML file, i.e. "comments: |".
        """
        comments = []
        for i in self._par._contents.splitlines():
            if i.startswith('#'):
                comments.append(i.strip())
            if i.startswith('typedef'):
                break
        comments = literal('\n'.join(comments))
        return comments

    def _generate_tables(self) -> dict:
        """ Generate a new Yanny tables section in the cache

        Creates a new "tables" section of a Yanny par cache.  A Yanny par
        file can contain multiple tables.  This makes each table a new key
        in the dictionary.  For each table, creates an entry with the table name,
        description, number of rows, and column definitions.

        Returns
        -------
        dict
            A new tables cache
        """
        out = {}
        for table in self._par.tables():
            out[table] = {
                'name': table,
                'description': 'replace me - with a description of this table',
                'n_rows': self._par.size(table),
                'structure': self._generate_table_structure(table)
            }
        return out

    def _generate_row(self, table: str) -> dict:
        """ Generate a row from the existing Yanny table

        Returns an example data row from a Yanny table as a dictionary
        with column names as keys.

        Parameters
        ----------
        table : str
            The name of a table in a Yanny par file

        Returns
        -------
        dict
            A dictionary of column/value pairs
        """
        row = self._par.row(table, 0)
        cols = self._par.columns(table)
        dd = dict(zip(cols, row))
        return {k: self._par.convert(table, k, v.decode("utf-8") if isinstance(v, np.bytes_) else v) for k, v in dd.items()}

    def _generate_table_structure(self, table: str) -> list:
        """ Generate a new Yanny par table structure section

        Creates a new struture section description a Yanny table for the
        cache.  The structure is a list of column definitions based on the Yanny
        typedef structure definition.

        Parameters
        ----------
        table : str
            The name of a table in a Yanny par file

        Returns
        -------
        list
            A list of table column definitions
        """
        row = self._generate_row(table)
        out = []
        for c in self._par.columns(table):
            tmp = {
                'name': c,
                'type': self._par.type(table, c),
                'description': 'replace me - with a description of this column',
                'unit': 'replace me - with a unit of this column',
                'is_array': self._par.isarray(table, c),
                'is_enum': self._par.isenum(table, c)
            }
            # optionally include enum values
            if tmp['is_enum']:
                tmp['enum_values'] = self._par._enum_cache.get(tmp['type'], [])

            # add in example
            tmp['example'] = row[c]
            out.append(tmp)
        return out

    def design_content(self, comments: str = None, header: Union[list, dict] = None,
                       name: str = None, description: str = None, columns: list = None) -> None:
        r""" Design a new Yanny par section

        Design a new Yanny par for the given datamodel.  Specify Yanny comments, a header section,
        or a table definition.  Each new table is added to the YAML structure.  Use
        ``name``, and ``description`` to specify the name and description of the new table.
        ``comments`` can be a single string of comments, with newlines indicated by "\\n"

        ``header`` can be a dictionary of key-value pairs, a list of tuples of header keywords,
        conforming to (keyword, value, comment), or list of dictionaries conforming to
        {"key": key, "value": value, "comment": comment}.

        The ``columns`` parameter defines the relevant table columns to add to the file.  It can be
        a list of column names, a list of tuple values conforming to column (name, type, [description]),
        or a list of dictionaries with keys defined from the complete column yaml definition.

        Allowed column types are any valid Yanny par types, input as strings, e.g. "int", "float", "char".
        Array columns can be specified by including the array size in "[]", e.g. "float[6]".  Enum types
        are defined by setting ``is_enum`` to True, and by providing a list of possible values via ``enum_values``.

        Parameters
        ----------
        comments : str, optional
            Any comments to add to the file, by default None
        header : Union[list, dict], optional
            Keywords to add to the header of the Yanny file, by default None
        name : str, optional
            The name of the parameter table
        description: str, optional
            A description of the parameter table
        columns : list, optional
            A set of Yanny table column definitions
        """
        if not self.design or (self.filename and os.path.exists(self.filename)):
            log.warning('Cannot design an new Yanny par when not in the datamodel design phase or '
                        'if a real file already exists.')
            return

        cached_par = self._cache['releases']['WORK'][self.cache_key]

        # add any comments
        comments = comments or '#This is designer Yanny par\n#\n#Add comments here\n'
        cached_par['comments'] = literal(comments)

        # add any header values
        hdr = cached_par.get('header', [])
        if not header and not hdr:
            header = [{'key': 'key1', 'value': 'value1', 'comment': 'description for key1'},
                      {'key': 'key2', 'value': 'value2', 'comment': 'description for key2'}]
        elif header:
            header = self._format_header(header)

        if header:
            hdr.extend(header)
        cached_par['header'] = hdr

        # add any tables
        name = name or 'TABLE'
        tables = cached_par.get('tables', {})
        struct = tables.get(name, {}).get('structure', [])
        description = description or 'description for TABLE'
        # update any columns
        if not columns and not struct:
            cols = [{'name': 'col1', 'type': 'int', 'description': 'description for col1',
                    'unit': '', 'is_array': False, 'is_enum': False,
                    'example': 1}]
        else:
            cols = self._format_columns(columns)
        struct.extend(cols)

        # create the table dictonary and update existing cache
        new_table = {name: {'name': name, 'description': description, 'n_rows': 0,
                            'structure': struct}}
        tables.update(new_table)
        cached_par['tables'] = tables

        # update the cached par
        self._cache['releases']['WORK'][self.cache_key] = cached_par

    @staticmethod
    def _format_header(header: Union[tuple, list, dict]) -> list:
        """ Format an input header into a YAML header """
        if not isinstance(header, list):
            header = [header]

        if isinstance(header[0], (tuple, list)):
            return [dict(zip(("key", "value", "comment"), i)) for i in header]
        elif isinstance(header[0], dict):
            if 'key' in header[0] and 'value' in header[0]:
                return header
            return [{"key": k, "value": v, "comment": f"description for {k}"} for k, v in header[0].items()]

    def _format_columns(self, columns: list) -> list:
        """ Format an input column list into a YAML table column structure """
        if not isinstance(columns, list):
            raise ValueError('input design columns must be a list.')


        if isinstance(columns[0], str):
            return [{'name': c, 'type': 'char', 'description': f'description for {c}',
                    'unit': '', 'is_array': False, 'is_enum': False,
                    'example': ''} for c in columns]
        elif isinstance(columns[0], (list, tuple)):
            n_len = len(columns[0])
            return [{'name': c[0], 'type': c[1] if n_len >= 2 else 'char',
                     'description': c[2] if n_len >= 3 else f'description for {c[0]}',
                     'unit': '', 'is_array': self._is_array(c[1]) if n_len >=2 else False,
                     'is_enum': False, 'example': self._format_example(c[1])} for c in columns]
        elif isinstance(columns[0], dict):
            return columns

    @staticmethod
    def _is_array(type: str) -> bool:
        """ Check if a type is an array """
        match = re.match(r"(?P<type>\w+)(?P<size>\[\d+\])*", type).groupdict()
        count = len(re.findall(r'\[\d+\]', type))
        return (count == 2 and match['type'] == 'char') or (count == 1 and match['type'] != 'char')

    def _format_example(self, type: str) -> str:
        """ Format the column example based on type """
        examples = {'int': 1, 'char': "a", "float": 1.0, "double": 1.0, "real": 1.0, "bool": False,
                    "bit": 0, "long": 1}
        match = re.match(r"(?P<type>\w+)(?P<size>\[\d+\])*", type).groupdict()
        examp = examples.get(match['type'], "")
        if self._is_array(type) and match['size']:
            examp = [examp] * int(match["size"][1])
        return examp

    @staticmethod
    def _get_designed_object(data: dict):
        """ Return a valid Yanny par object

        Parses and validates the par YAML cache into a proper Pydantic model
        and converts the model into an Yanny par object.

        Parameters
        ----------
        data : dict
            The par cache

        Returns
        -------
        yanny
            A valid yanny object
        """
        return ParModel.parse_obj(data).convert_par()

    def write_design(self, file: str, overwrite: bool = True) -> None:
        """ Write out the designed file

        Write out a designed Yanny par object to a file on disk.  Must have run
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
        if not self._designed_object:
            raise AttributeError('Cannot write.  Designed object does not exist.')

        # remove the existing file
        if overwrite and os.path.exists(file):
            os.remove(file)

        par = self._cache['releases']['WORK'][self.cache_key]
        self._designed_object.write(file, comments=par['comments'])

    def _generate_new_cache(self) -> dict:
        """ Generate a new Yanny parameter file cache entry """
        return {'comments': self._generate_comments(),
                    'header': self._generate_header(),
                    'tables': self._generate_tables()}

    def _set_cache(self, force: bool = None):
        """ Custom method to set the Yanny par cache """
        super(ParFile, self)._set_cache(force=force)

        # reset all par comments to a literal block
        self._literalize_comments()

    def _literalize_comments(self):
        """ Convert the Yanny par comments section into a literal block """
        for data in self._cache['releases'].values():
            data[self.cache_key]['comments'] = literal(data[self.cache_key]['comments'])

    def _update_partial_cache(self, cached_par: dict, old_par: dict) -> dict:
        """ Update the partial cache of a Yanny par file

        Parameters
        ----------
        cached_par : dict
            The new cache par section
        old_par : dict
            The old cache par section

        Returns
        -------
        dict
            The updated cache object

        """
        # skip comments section - always generate a new one

        # update the header section
        oldhdr = [c['key'] for c in old_par['header']]
        for hdr in cached_par['header']:
            # TODO - add new hdr entry
            if hdr['key'] not in oldhdr:
                continue
            # update the hdr comment
            hh = [i for i in old_par['header'] if i['key'] == hdr['key']][0]
            hdr['comment'] = hh['comment']

        # update the tables section
        old_tables = old_par['tables']
        for name, table in cached_par['tables'].items():
            # skip the table if it doesn't exist in the old cache
            if name not in old_tables:
                # TODO - need to generate a new table entry
                continue

            # update the description
            table['description'] = old_tables[name]['description']

            # update the structure columns
            oldcols = [c['name'] for c in old_tables[name]['structure']]
            for column in table['structure']:
                # TODO - generate new column entry
                if column['name'] not in oldcols:
                    continue

                # update column parts
                col = [i for i in old_tables[name]['structure'] if i['name'] == column['name']][0]
                column['description'] = col['description']
                column['unit'] = col['unit']

        return cached_par

    def _use_full_cache(self):
        """ Custom method when using the full cache of a prior releaes

        Need to additionally convert comments section into literal blocks
        """
        self._cache['releases'][self.release] = self._cache['releases'].get(self.use_cache_release, {})
        self._literalize_comments()