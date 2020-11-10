# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: generate.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from datamodel.generate import Stub
from os import environ, makedirs
from os.path import join, exists, dirname

__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Generate(object):
    """Class to generate a datamodel.

    Parameters
    ----------
    options : command-line options, optional
        Operate on these files.
    tree_ver : str, optional
        Override the tree version default set by modules
    """
    
    

    def __init__(self, options = None, tree_ver = None, env_label = None, location = None, format = None, force = None, verbose = None, debug = None):
        self.tree_ver = options.tree_ver if options else tree_ver
        self.env_label = options.env_label if options else env_label
        self.location = options.location if options else location
        self.format = options.format if options else format
        self.force = options.verbose if options else force
        self.verbose = options.verbose if options else verbose
        self.debug = options.debug if options else debug
        self.stub = None
        self.directory = None
        self.file = None
        self.set_datamodel_dir()
        self.set_sas_base_dir()
    
    def set_datamodel_dir(self):
        """Set the DATAMODEL_DIR from the environment
        """
        self.datamodel_dir = environ('DATAMODEL_DIR')
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
        self.sas_base_dir = environ('SAS_BASE_DIR')
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
        if self.datamodel_dir and self.format:
            self.directory = join(self.datamodel_dir, 'data', self.format, self.env_label) if self.env_label else None
            if not self.directory:
                print("GENERATE> Please set env_label option")
            else:
                folder = dirname(self.location) if self.location else None
                self.directory = join(self.directory, folder) if folder else None
                if not self.directory:
                    print("GENERATE> Please set location option")
                elif not exists(self.directory):
                    try:
                        makedirs(self.directory)
                        if self.verbose:
                            print("GENERATE> creating directory at %s" % self.directory)
                    except Exception as e:
                        print("GENERATE> cannot create directory at %s" % self.directory)
                        print("--> EXCEPTION=%r" % e)
                        self.directory = None
        else:
            if not self.format:
                print("GENERATE> Please set format to html or md")
            self.directory = None

    def set_file(self):
        """Set the input file from the tree_ver and location
           and confirm it exists
        """
        if self.sas_base_dir:
            self.file = join(self.sas_base_dir, self.tree_ver) if self.tree_ver else None
            if not self.file:
                print("GENERATE> Please set tree_ver option")
            elif not exists(self.file):
                print("GENERATE> Nonexistent tree at %s" % self.file)
                self.file = None
            else:
                self.file = join(self.file, self.location) if self.location else None
                if not self.file:
                    print("GENERATE> Please set location option")
                elif not exists(self.file):
                    print("GENERATE> Nonexistent file at %s" % self.file)
                    self.file = None
        else: self.file = None

    def set_stub(self):
        """Set the stub class and use it to write output
           from the template"
        """
        self.stub = Stub(format = self.format, verbose = self.verbose)
        self.stub.set_directory(path = self.directory)
        self.stub.set_file(path = self.file)
        self.stub.set_template()
        self.stub.set_output()
        self.stub.set_path()
        self.stub.write()


