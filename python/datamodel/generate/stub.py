# @Author: Brian Cherinka
# @Date: Mar 7, 2016
# @Revised by: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: stub.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from astropy.io import fits
from os.path import basename, join, exists, getsize, splitext
from jinja2 import Environment, PackageLoader
from json import dumps
from yaml import load, FullLoader, dump

__author__ = 'Brian Cherinka, Joel Brownstein'

class Stub(object):
    """Class to create a datamodel stub.

    Parameters
    ----------
    file_spec : (unique) file file_spec name
    directory : dictionary of paths to output stub
    verbose : str , optional
        Verbose output
    """
    
    fmap = {'A': 'char', 'I': 'int16', 'J': 'int32', 'K': 'int64',
                     'E': 'float32', 'D': 'float64', 'B': 'bool', 'L': 'bool'}
    cache_formats = ['yaml']

    def __init__(self, file_spec = None, directory = None, verbose = None, force = None):
        self.file_spec = file_spec
        self.directory = directory
        self.verbose = verbose
        self.force = force
        self.template = self.input = self.output = self.cache = self.environment = None

    def set_access(self, path = None):
        if self.directory and 'access' in self.directory:
            directory = self.directory['access']
            if not exists(directory):
                print("STUB> nonexistent directory at %s" % directory)
                directory = None
            access_path = join(directory, "%s.access" % self.file_spec) if directory and self.file_spec else None
            if access_path:
                if exists(access_path):
                    with open(access_path) as file:
                        print("STUB> access %s" % access_path)
                        self.access = load(file, Loader=FullLoader)
                        if self.access.split(" = $")[-1] != path:
                            print("STUB> Aborting due to conflict in existing spec: %s" % self.access)
                            self.access = None
                elif access_path:
                    self.access = "%s = $%s" % (self.file_spec, path)
                    try:
                        with open(access_path, 'w') as file:
                            file.write(self.access)
                        if self.verbose: print("STUB> Output to %s" % access_path)
                    except Exception as e:
                        print("STUB> Output exception %r" % e)
                else: self.access = None
            else: self.access = None
        else: self.access = None

    def set_input(self, path = None, format = None):
        """Set the file's properties for it's path.
        """
        self.input = None
        if path and self.access:
            self.input = {'path': path, 'file_spec': self.file_spec, 'hdus': None}
            self.input['format'] = format
            self.input['basename'] = basename(path)
            self.input['filename'] = self.input['basename'].replace('.', '\.')
            self.input['filesize'] = self.get_filesize()
            self.input['filetype'] = self.get_filetype()
    
    def set_environment(self):
        """Set the jina2 environment including filters for content.
        """
        loader = PackageLoader('datamodel', 'templates')
        self.environment = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    def set_cache(self, format='yaml'):
        """Set the cached content from yaml (by default).
        """
        if self.input and format in self.cache_formats:
            file_spec = self.input['file_spec'] if self.input and 'file_spec' in self.input else None
            dir = self.directory[format] if self.directory and format in self.directory else None
            self.cache = {'format':format, 'path': join(dir, file_spec + "." + format)} if dir and file_spec else None
            self.cache['content'] = self.get_content_from_cache()
            self.set_cache_hdus()
        else: self.cache = None

    def update_cache_hdu_row(self, row = None, field = None):
        """Set the name, etc. fields in the cached hdu
        """
        if field and hasattr(self.hdu, field):
            if field in self.hdu_row and not self.force:
                self.cached = True
            elif field=='header':
                header = self.hdu.header
                self.hdu_row[field] = []
                for key, value in header.items():
                    if self.is_header_keyword(key = key):
                        column = {'key': key, 'value': value, 'comment': header.comments[key]}
                        self.hdu_row['header'].append(column)
            elif field=='size':
                self.hdu_row[field] = self.format_bytes(getattr(self.hdu, field))
            else:
                self.hdu_row[field] = getattr(self.hdu, field)
                self.cached = False

    def update_cache_hdu_column(self, row = None, index = None, column = None):
        """Set the cached content for a colum in a hdu table
        """
        columns = self.hdu_row['columns'] if 'columns' in self.hdu_row else {}
        if column.name in columns and not self.force:
            pass
        else:
            columns[column.name] = {'name':column.name.upper(), 'type': self.format_type(column.format), 'unit': self.nonempty_string(column.unit), 'description': self.nonempty_string()}

    def set_cache_hdus(self):
        """Set the cached content for each hdu
        """
        content = self.cache['content'] if self.cache and 'content' in self.cache else None
        hdus = content['hdus'] if content and 'hdus' in content else None
        if hdus is not None:
            for hdu_number, self.hdu in enumerate(self.input['hdus']):
                row = 'hdu%r' % hdu_number
                self.hdu_row = hdus[row] if hdus and row in hdus else {} if self.hdu.is_image else {'columns': {}}
                for field in ['name', 'is_image', 'size']:
                    self.update_cache_hdu_row(row = row, field = field)
                if self.hdu.is_image:
                    if self.verbose: print("HDU %r >" % hdu_number + "IMAGE: %(name)s" % self.hdu_row)
                    self.update_cache_hdu_row(row = row, field = 'header')
                else:
                    if self.verbose: print("HDU %r >" % hdu_number + "TABLE: %(name)s"  % self.hdu_row + " --> %r columns" % len(self.hdu.columns))
                    for index, column in enumerate(self.hdu.columns):
                        self.update_cache_hdu_column(row = row, index = index, column = column)
                hdus[row] = self.hdu_row

    def get_content_from_cache(self):
        """Get the cached content from yaml file (by default).
        """
        format = self.cache['format'] if self.cache and 'format' in self.cache else None
        path = self.cache['path'] if self.cache and 'path' in self.cache else None
        if path and format == 'yaml':
            if exists(path):
                with open(path) as file:
                    content = load(file, Loader=FullLoader)
            else:
                template = self.environment.get_template("stub.%s" % format)
                content = load(template.render(self.input), Loader=FullLoader)
            if content and 'hdus' not in content: content['hdus'] = {}
        else: content = None
        return content

    def format_bytes(self, value = None):
        """Convert an integer to human-readable format.

        Parameters
        ----------
        value : int
            An integer representing number of bytes.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """
        
        try: value = int(value)
        except: value = 0
        
        for unit in ('bytes', 'KB', 'MB', 'GB'):
            if value < 1024:
                return "{0:d} {1}".format(int(value), unit)
            else:
                value /= 1024.0

        return "{0:3.1f} {1}".format(value, 'TB')

    def get_filesize(self):
        """Get the size of the input file.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """
        return self.format_bytes(getsize(self.input['path'])) if self.input else None

    def get_filetype(self):
        """Get the extension of the input file.

        Returns
        -------
        str
            File type in upper case.
        """
        filename, file_extension = splitext(self.input['path']) if self.input else None
        if 'gz' in file_extension:
            filename, file_extension = splitext(filename)
        return file_extension[1:].upper()

    def set_input_hdus(self):
        """Read the file and hdus.
        """
        if self.input:
            self.input['hdus'] = fits.open(self.input['path'])

    def nonempty_string(self, value = None):
        """Jinja2 Filter to map the format value to a string.

        Parameters
        ----------
        value : str?
            Not sure what type this is supposed to have.

        Returns
        -------
        string: str
            The string.
        """
        string = value if type(value) == str else "%r" % value if value else "**"
        return string

    def format_type(self, value = None):
        """Jinja2 Filter to map the format type to a data type.

        Parameters
        ----------
        value : str?
            Not sure what type this is supposed to have.

        Returns
        -------
        str
            The data type.
        """
        out = [val if value.isalpha() else '{0}[{1}]'.format(val, value[:-1])
               for key, val in self.fmap.items() if key in value]
        return out[0]

    def is_header_keyword(self, key = None):
        """Test for hdu header keyword

        Returns
        -------
        bool
            ``True`` if `key` does *not* contain 'TFORM' or 'TTYPE'.
        """
        return tuple([key.find(f) for f in ('TFORM', 'TTYPE')]) == (-1, -1)

    def set_output(self):
        if self.input and self.template:
            self.output = {format: join(dir, self.file_spec + "." + format) for format, dir in self.directory.items()}
        else: self.output = None

    def get_yaml(self):
        return dump(self.cache['content']) if self.cache and 'content' in self.cache else None

    def get_json(self):
        return dumps({}) if self.input else None

    def set_result(self):
        """Set the result for the input by rendering the template,
           and set a json or yaml version of the input dictionary.
        """
        self.result = None
        format = self.input['format'] if self.input and 'format' in self.input else None
        if format and self.template:
            self.result = {format: self.template.render(input = self.input, content = self.cache['content'])}
            self.result['json'] = self.get_json()
            self.result['yaml'] = self.get_yaml()

    def set_template(self):
        """Create the Jinja2 environment and set the template.
        """
        self.template = self.environment.get_template("stub.%(format)s" % self.input) if self.environment and self.input else None

    def write(self, format = None):
        """Write the output result to the output path.
        """
        if self.output and self.result:
            if format and format in self.output and format in self.result:
                try:
                    with open(self.output[format], 'w') as file:
                        file.write(self.result[format])
                    if self.verbose: print("STUB> Output to %s" % self.output[format])
                except Exception as e:
                    print("STUB> Output exception %r" % e)
            else:
                print("STUB> Invalid format=%r for write" % format)

    def close_input_hdus(self):
        """Close input hdus
        """
        if self.input and 'hdus' in self.input:
            self.input['hdus'].close()
