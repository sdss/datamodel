# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: generate.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from tree import Tree
from datamodel.generate import Stub
from os import environ, makedirs
from os.path import join, exists, dirname, sep
from re import split
from yaml import load, FullLoader


__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Generate(object):
    """Class to generate a datamodel.

    Parameters
    ----------
    options : command-line options, optional
    tree_ver : str, optional
        Override the tree version default set by modules
    file_spec : str, required
        Name of file species
    path : str, optional (required w/out env_label + location)
        Symbolic path to fits file (can be combined from
        the env_label/location if omitted)
    keywords : list of str, optional
        keywords needed to format the symbolic path to form
        a real path to the fits file.
    env_label : str, optional (required w/out path)
        the tree environmental variable (can be parsed from
        the symbolic path if omitted)
    location: str, optional (required w/out path)
        the partial symbolic path (can be parsed from the
        symbolic path if omitted)
    html : generate html format
    force : bool (default false)
        set True to over-write the human edited yaml and
        restore it to the original template / fits file.
    """
    
    formats = ['md', 'html']

    def __init__(self, options = None, tree_ver = None, file_spec = None, path = None, keywords = None, env_label = None, location = None, html = None, force = None, verbose = None, debug = None):
        self.tree_ver = options.tree_ver if options else tree_ver
        self.file_spec = options.file_spec if options else file_spec
        self.path = options.path if options else path
        self.keywords = options.keywords if options else keywords
        if self.path is None:
            self.env_label = options.env_label if options else env_label
            self.location = options.location if options else location
            self.path = join(self.env_label, self.location)
        else:
            try: self.env_label, self.location = self.path.split(sep, 1)
            except:
                self.env_label = options.env_label if options else env_label
                self.location = options.location if options else location
        if not self.file_spec: self.set_spec_from_location()
        self.html = options.html if options else html
        self.force = options.force if options else force
        self.verbose = options.verbose if options else verbose
        self.debug = options.debug if options else debug
        self.tree = None
        self.env_path = None
        self.stub = None
        self.directory = None
        self.file = None
        self.set_format()
        self.set_tree()
        self.set_real_and_abstract_location()
        self.set_datamodel_dir()
        self.set_sas_base_dir()
    
    def set_format(self):
        self.format = 'html' if self.html else None
        if self.format not in self.formats: self.format = self.formats[0]
        
    def set_tree(self):
        """Set the Tree from input options, or default to the current loaded module
        """
        if self.tree_ver is None:
            try:  self.tree_ver = environ['TREE_VER']
            except: pass
        self.tree = Tree(config = self.tree_ver)
        if self.tree_ver != self.tree.config_name: self.tree_ver = self.tree.config_name
    
    def set_env(self):
        """Get the env_path from tree[env_label]
        """
        self.env = None
        if self.env_label:
            if self.tree:
                for section, env in self.tree.environ.items():
                    if self.env_label in env:
                        self.env = {'label': self.env_label, 'path': env[self.env_label]}
                        break
        else:
            print("GENERATE> Please specify a valid env label option.")
        if not self.env:
            print("GENERATE> Please add this environment=%r to the tree product, and try again." % self.env_label)
        elif self.verbose:
            print("GENERATE> using %(label)s=%(path)r" % self.env)
    
    def set_real_and_abstract_location(self):
        """Substitute the keywords into the location
        """
        self.real_location = self.abstract_location = None
        real = {}
        abstract = {}
        for keyword in self.keywords:
            try:
                key, value = keyword.split('=')
                real[key] = value
                abstract[key] = key.upper()
            except: print("GENERATE> %r is an invalid key=value assignment")
        try:
            self.real_location = self.location.format(**real)
            self.abstract_location = self.location.format(**abstract)
        except Exception as e: print("GENERATE %r> key %s is missing from location=%r" % (e, key, self.location))
    
    def set_abstract_location(self):
        """Replace the keyword format with upper case
        """
        self.abstract_location = self.location
        keywords = {}
        for keyword in self.keywords:
            try: key, value = keyword.split('=')
            except: print("GENERATE> %r is an invalid key=value assignment")
            try: self.real_location.format(key=value)
            except: print("GENERATE> key %s is missing from location=%r" % (key, self.location))
    

    def set_datamodel_dir(self):
        """Set the DATAMODEL_DIR from the environment
        """
        try: self.datamodel_dir = environ['DATAMODEL_DIR']
        except: self.datamodel_dir = None
        if not self.datamodel_dir:
            print("GENERATE> Please set DATAMODEL_DIR")
        elif not exists(self.datamodel_dir):
            print("GENERATE> Nonexistent DATAMODEL_DIR at %s" % self.datamodel_dir)
            self.datamodel_dir = None
        elif self.verbose:
            print("GENERATE> DATAMODEL_DIR = %r" % self.datamodel_dir)

    def set_sas_base_dir(self):
        """Set the SAS_BASE_DIR from the environment
        """
        try: self.sas_base_dir = environ['SAS_BASE_DIR']
        except: sas_base_dir = None
        if not self.sas_base_dir:
            print("GENERATE> Please set SAS_BASE_DIR")
        elif not exists(self.sas_base_dir):
            print("GENERATE> Nonexistent SAS_BASE_DIR at %s" % self.sas_base_dir)
            self.sas_base_dir = None
        elif self.verbose:
            print("GENERATE> SAS_BASE_DIR = %r" % self.sas_base_dir)

    def set_directory(self):
        """Set the output directory from the tree_ver, env_label and location
           and confirm it exists (try making it if it doesn't)
        """
        self.directory = None
        if not self.format:
            print("GENERATE> Please set a valid format option")
        elif not self.path:
            print("GENERATE> Please set path option, or set env_label and location options")
        elif self.datamodel_dir and self.abstract_location:
            formats = [self.format, 'access', 'yaml', 'json']
            self.directory = {}
            data_dir = join(self.datamodel_dir, 'data')
            for format in formats:
                directory = join(data_dir, format, self.env_label)
                if format != 'access': directory = join(directory, dirname(self.abstract_location))
                if not exists(directory):
                    try:
                        makedirs(directory)
                        if self.verbose:
                            print("GENERATE> creating directory at %s" % directory)
                    except Exception as e:
                        print("GENERATE> cannot create directory at %s" % directory)
                        print("--> EXCEPTION=%r" % e)
                        directory = None
                if directory: self.directory[format] = directory

    def set_file(self):
        """Set the input file from the tree_ver and location
           and confirm it exists
        """
        self.set_env()
        if self.env and 'path' in self.env:
            if not exists(self.env['path']):
                print("GENERATE> Nonexistent environ at %s" % self.env)
                self.file = None
            else:
                self.file = join(self.env['path'], self.real_location) if self.real_location else None
                if not self.file:
                    print("GENERATE> Please set location option")
                elif not exists(self.file):
                    print("GENERATE> Nonexistent file at %s" % self.file)
                    self.file = None
        else: self.file = None

    def set_spec_from_location(self):
        namesplit = split('[-.]', basename(self.location))
        self.file_spec = namesplit[0] if len(namesplit) > 1 else None
    
    def set_stub(self):
        """Set the stub class and use it to write output
           from the template"
        """
        self.stub = Stub(file_spec = self.file_spec, directory = self.directory, verbose = self.verbose, force = self.force)
        self.stub.set_access(path = self.path)
        self.stub.set_input(path = self.file, format = self.format)
        self.stub.set_input_hdus()
        self.stub.set_environment()
        self.stub.set_cache()
        self.stub.set_template()
        self.stub.set_output()
        self.stub.set_result()
        for format in [self.format, 'yaml', 'json']:
            self.stub.write(format = format)
        self.stub.close_input_hdus()


