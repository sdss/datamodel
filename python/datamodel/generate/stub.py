# @Author: Brian Cherinka
# @Date: Mar 7, 2016
# @Revised by: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: stub.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

import jinja2
import os
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
        self.dict = {}
        self.hdulist = None
        self.file = None
        self.directory = None
        self.template = None
        self.output = None
        self.path = None

    def set_directory(self, path = None):
        """Set the directory's if it exists
        """
        self.directory = path if exists(path) else None
        if not self.directory:
            print("STUB> nonexistent directory at path=%r" % path)
        elif self.verbose:
            print("STUB> directory = %r" % self.directory)

    def set_file(self, path = None):
        """Set the file's properties for it's path.
        """
        self.file = {'basename': None, 'name':None, 'path':None}
        if path and self.directory:
            self.file['basename'] = os.path.basename(self.filename)
            namesplit = re.split('[-.]', self.file['basename'])
            self.file['name'] = namesplit[0] if len(namesplit) > 1 else None
            self.file['path'] = os.path.join(self.directory, self.file['name']) if self.file['name'] else None

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

    def getFileSize(self):
        """Get the size of the input file.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """
        return self.formatBytes(os.path.getsize(self.filename))

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

    def getFileExtension(self):
        """Get the extension of the input file.

        Returns
        -------
        str
            File type in upper case.
        """
        filename, file_extension = os.path.splitext(self.filename)
        if 'gz' in file_extension:
            filename, file_extension = os.path.splitext(filename)
        return file_extension[1:].upper()

    def readFile(self):
        """Read the file and hdus.
        """
        self.hdulist = fits.open(self.filename)

    def getHeaders(self):
        """Return a list of headers.

        Returns
        -------
        list
            The headers stripped from the file.
        """
        if self.hdulist is None:
            self.readFile()
        headers = []
        for hdu in self.hdulist:
            headers.append(hdu.header)
        return headers

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
        """Build the stub for a single file.
        """
        self.readFile()
        self.set_dict()
        self.output = self.template.render(self.dict) if self.template and self.dict else None
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

    def set_dict(self):
        """Set up input dictionary to the template files.
        """
        self.dict['name'] = self.file['name'] if self.file else None
        self.dict['filesize'] = self.getFileSize()
        self.dict['filetype'] = self.getFileExtension()
        self.dict['filename'] = self.file['basename'].replace('.', '\.')
        self.dict['hdus'] = self.hdulist

    def set_path(self):
        """Set the path for the stub
        """
        self.path = '{path}.html'.format(self.file) if self.file else None

    def write(self):
        """Write the template to path.
        """
        if self.template and self.path:
            with open(self.path, 'w') as file: file.write(self.template)

