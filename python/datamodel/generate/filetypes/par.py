# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import numpy as np
import yaml
import os

from pydl.pydlutils.yanny import yanny

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
                'is_enum': self._par.isenum(table, c),
                'example': row[c]
            }
            out.append(tmp)
        return out
    
    def design_content(self) -> None:
        if not self.design or (self.filename and os.path.exists(self.filename)):
            log.warning('Cannot design an new Yanny par when not in the datamodel design phase or '
                        'if a real file already exists.')
            return
        
        cached_par = self._cache['releases']['WORK'][self.cache_key]

        cached_par['comments'] = '#This is designer Yanny par\n#\n#Add comments here\n'
        cached_par['header'] = [{'key': 'key1', 'value': 'value1', 'comment': 'description for key1'}, 
                                {'key': 'key2', 'value': 'value2', 'comment': 'description for key2'}]
        cached_par['tables'] = {'NEWPAR': {'name': 'NEWPAR', 'description': 'description for NEWPAR', 
                                           'n_rows': 0, 
                                           'structure': []}}
        cols = [{'name': 'col1', 'type': 'int', 'description': 'description for col1', 
                 'unit': '', 'is_array': False, 'is_enum': False, 
                 'example': 1}] 
        cached_par['tables']['NEWPAR']['structure'] = cols
        self._cache['releases']['WORK'][self.cache_key] = cached_par
        
    def create_from_cache(self, release: str = 'WORK') -> yanny:
        """ Create a Yanny par file from the yaml cache

        Converts the par dictionary entry in the YAML cache into
        a Yanny par object.

        Parameters
        ----------
        release : str, optional
            the name of the data release, by default 'WORK'

        Returns
        -------
        yanny
            a valid yanny par object

        Raises
        ------
        ValueError
            when the release is not in the cache
        ValueError
            when the release is not WORK when in the datamodel design phase
        """
        if release not in self._cache['releases']:
            raise ValueError(f'Release {release} not found in list of cached releases.')
        
        if self.design and release != 'WORK':
            raise ValueError(f'Release {release} can only be "WORK" when in the datamodel design phase.')
        
        par = self._cache['releases'][release][self.cache_key]
        self._designed_object = ParModel.parse_obj(par).convert_par()
        return self._designed_object 

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