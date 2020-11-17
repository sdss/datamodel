# @Author: Brian Cherinka
# @Date: Mar 7, 2016
# @Revised by: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: stub.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from astropy.io import fits
from os.path import basename, join, exists, getsize, splitext
from json import dumps
import jinja2
import re

__author__ = 'Brian Cherinka, Joel Brownstein'

class Stub(object):
    """Class to create a datamodel stub.

    Parameters
    ----------
    directory : dictionary of paths to output stub
    verbose : str , optional
        Verbose output
    """
    
    fmap = {'A': 'char', 'I': 'int16', 'J': 'int32', 'K': 'int64',
                     'E': 'float32', 'D': 'float64', 'B': 'bool', 'L': 'bool'}

    def __init__(self, directory = None, verbose = None):
        self.directory = directory
        self.verbose = verbose
        self.template = None
        self.input = self.output = None

    def set_input(self, path = None, format = None):
        """Set the file's properties for it's path.
        """
        self.input = None
        if path:
            self.input = {'path': path, 'hdus': None}
            self.input['format'] = format
            self.input['basename'] = basename(path)
            self.input['filename'] = self.input['basename'].replace('.', '\.')
            namesplit = re.split('[-.]', self.input['basename'])
            self.input['name'] = namesplit[0] if len(namesplit) > 1 else None
            self.input['filesize'] = self.get_filesize()
            self.input['filetype'] = self.get_filetype()

    def formatBytes(self, value):
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
        return self.formatBytes(getsize(self.input['path'])) if self.input else None

    def getHDUSize(self, value):
        """Jinja2 filter - Get the size of an HDU.

        Parameters
        ----------
        value : int
            An integer representing number of bytes.

        Returns
        -------
        str
            Size of the HDU in human-readable format.
        """
        return self.formatBytes(value)

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

    def open_hdus(self):
        """Read the file and hdus.
        """
        self.input['hdus'] = fits.open(self.input['path']) if self.input else None

    def getString(self, value):
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

    def getType(self, value):
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

    def isKeyAColumn(self, value):
        """Jinja2 Filter to filter out a header keyword
        that specifies a column in a binary table hdu.

        Parameters
        ----------
        value : str
            Not sure what the type of value is supposed to be.

        Returns
        -------
        bool
            ``True`` if `value` does *not* contain 'TFORM' or 'TTYPE'.
        """
        return tuple([value.find(f) for f in ('TFORM', 'TTYPE')]) == (-1, -1)

    def set_output(self):
        if self.input and self.template:
            name = self.input['name']
            self.output = {format: join(dir, name + "." + format) for format, dir in self.directory.items()}
        else: self.output = None

    def get_yaml(self):
        return "yaml"

    def get_json(self):
        return dumps({}) if self.input else None

    def set_result(self):
        """Set the result for the input by rendering the template,
           and set a json or yaml version of the input dictionary.
        """
        self.result = None
        format = self.input['format'] if self.input and 'format' in self.input else None
        if format and self.template:
            self.result = {format: self.template.render(self.input)}
            self.result['json'] = self.get_json()
            self.result['yaml'] = self.get_yaml()

    def set_template(self):
        """Create the Jinja2 environment and set the template.
        """
        templateLoader = jinja2.PackageLoader('datamodel', 'templates')
        env = jinja2.Environment(loader=templateLoader, trim_blocks=True,
                                 lstrip_blocks=True)
        env.filters['getType'] = self.getType
        env.filters['getHDUSize'] = self.getHDUSize
        env.filters['isKeyAColumn'] = self.isKeyAColumn
        env.filters['getString'] = self.getString
        self.template = env.get_template("stub.%(format)s" % self.input) if self.input else None

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

    def close_hdus(self):
        """Close input hdus
        """
        if self.input and 'hdus' in self.input:
            self.input['hdus'].close()
