# @Author: Brian Cherinka
# @Date: Mar 7, 2016
# @Revised by: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: stub.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

import jinja2
from os.path import basename, join, exists, getsize, splitext
import re
import sys
from astropy.io import fits

__author__ = 'Brian Cherinka, Joel Brownstein'

class Stub(object):
    """Class to create a datamodel stub.

    Parameters
    ----------
    format : str , optional, defaults to md
    verbose : str , optional
        Verbose output
    """
    
    fmap = {'A': 'char', 'I': 'int16', 'J': 'int32', 'K': 'int64',
                     'E': 'float32', 'D': 'float64', 'B': 'bool', 'L': 'bool'}
    #formats = ['md', 'html']
    formats = ['html']

    def __init__(self, format = None, verbose = None):
        self.format = format if format and format in self.formats else self.formats[0]
        self.verbose = verbose
        self.directory = None
        self.template = None
        self.input = self.output = None

    def set_directory(self, path = None):
        """Set the directory's if it exists
        """
        self.directory = path if exists(path) else None
        if not self.directory:
            print("STUB> nonexistent directory at path=%r" % path)
        elif self.verbose:
            print("STUB> directory = %r" % self.directory)

    def set_input(self, path = None):
        """Set the file's properties for it's path.
        """
        self.input = None
        if path and self.directory:
            self.input = {'path': path, 'hdus': None, 'headers': None}
            self.input['basename'] = basename(path)
            self.input['filename'] = self.input['basename'].replace('.', '\.')
            namesplit = re.split('[-.]', self.input['basename'])
            self.input['name'] = namesplit[0] if len(namesplit) > 1 else None
            self.input['stub'] = join(self.directory, self.input['name']) if self.input['name'] else None
            self.input['filesize'] = self.get_filesize()
            self.input['filetype'] = self.get_filetype()set

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

    def set_hdus(self):
        """Read the file and hdus.
        """
        self.input['hdus'] = fits.open(self.input['path']) if self.input else None

    def set_headers(self):
        """Set a list of headers stripped from the hdulist.
        """
        if self.input:
            if self.input['hdus'] is None: self.set_hdus()
            self.input['headers'] = []
            for hdu in self.input['hdus']:
                self.input['headers'].append(hdu.header)

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
        """Set the output for the input by rendering the template.
        """
        self.output = {'path': "%(stub)s.html" % self.input if self.input else None}
        self.output['result'] = self.template.render(self.input) if self.template and self.input else None
        self.hdulist.close()

    def set_template(self):
        """Create the Jinja2 environment and set the template.
        """
        templateLoader = jinja2.PackageLoader('datamodel', 'templates')
        env = jinja2.Environment(loader=templateLoader, trim_blocks=True,
                                 lstrip_blocks=True)
        env.filters['getType'] = self.getType
        env.filters['getHDUSize'] = self.getHDUSize
        env.filters['isKeyAColumn'] = self.isKeyAColumn
        self.template = env.get_template('stub.html')

    def write(self):
        """Write the output result to the output path.
        """
        if self.output:
            with open(self.output['path'], 'w') as file:
                file.write(self.output['result'])

