# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: generate.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

import os
import re
from os.path import basename, dirname, exists, join, sep

from tree import Tree

from .parse import get_abstract_key, get_file_spec
from .stub import Stub


__author__ = "Joel Brownstein <joelbrownstein@sdss.org>"


class Generate(object):
    """Class to generate a datamodel.

    Parameters
    ----------
    options : object, optional
        argparse command-line options
    tree_ver : str, optional
        Override the tree version default set by modules
    file_spec : str, optional
        Name of file species
    path : str, optional
        Symbolic path to fits file (can be combined from the env_label/location if omitted).
        (required w/out env_label + location)
    keywords : list of str, optional
        keywords needed to format the symbolic path to form a real path to the fits file.
    env_label : str, optional
        the tree environmental variable (can be parsed from the symbolic path if omitted)
        (required w/out path)
    location: str, optional
        the partial symbolic path (can be parsed from the symbolic path if omitted)
        (required w/out path)
    html : bool
        if True, generate html format. Default is False.
    replace : bool
        set True to (git) move the output files if the path has changed for the given spec file, and
        to avoid abort due to the conflict of having multiple paths for a single spec file name.
    force : bool
        set True to over-write the human edited yaml and restore it to the original
        template / fits file. Default is False.
    """

    formats = ["md", "html"]

    def __init__(self, options=None, tree_ver=None, file_spec=None, path=None, keywords=None,
                 env_label=None, location=None, html=None, replace=None, force=None, verbose=None,
                 debug=None
                 ):
        # TODO - add git booleans
        # TODO - split out product code into Product class
        # TODO - refactor Generate to be only about the file generation process

        # setting options
        self.tree_ver = options.tree_ver if options else tree_ver
        file_spec = options.file_spec if options else file_spec
        self.file_spec = get_file_spec(file_spec=file_spec)
        self.path = options.path if options else path
        self.keywords = options.keywords if options else keywords

        if self.path is None:
            self.env_label = options.env_label if options else env_label
            self.location = options.location if options else location
            self.path = join(self.env_label, self.location)
        else:
            try:
                self.env_label, self.location = self.path.split(sep, 1)
            except:
                self.env_label = options.env_label if options else env_label
                self.location = options.location if options else location

        # set the file species from the location
        if not self.file_spec and not file_spec:
            self.set_file_spec_from_location()

        self.html = options.html if options else html
        self.force = options.force if options else force
        self.replace = options.replace if options else replace
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

    def __repr__(self):
        return f"<Generate(file_spec='{self.file_spec}', release='{self.release}')>"

    def set_format(self):
        """ Set the output format """
        self.format = "html" if self.html else None
        if self.format not in self.formats:
            self.format = self.formats[0]

    def set_tree(self) -> None:
        """ Set the SDSS Tree

        Sets the Tree from input options, or default to the current loaded module
        """
        if self.tree_ver is None:
            self.tree_ver = os.getenv('TREE_VER', None)

        # add the tree and config_name
        self.tree = Tree(config=self.tree_ver)
        if self.tree_ver != self.tree.config_name:
            self.tree_ver = self.tree.config_name

        # add the tree release
        self.release = self._get_tree_release()

    def _get_tree_release(self):
        """ Get a tree release in a backwards compatible way """
        if hasattr(self.tree, 'release'):
            return self.tree.release

        release = self.tree.config_name.upper()
        if 'work' in self.tree.config_name or self.tree.config_name == 'sdss5':
            release = 'WORK'
        return release

    def set_env(self):
        """Get the env_path from tree[env_label]"""
        self.env = None
        if self.env_label:
            if self.tree:
                for section, env in self.tree.environ.items():
                    if self.env_label in env:
                        self.env = {"label": self.env_label, "path": env[self.env_label]}
                        break
        else:
            print("GENERATE> Please specify a valid env label option.")

        if not self.env:
            print(f"GENERATE> Please add this environment={self.env_label} to the tree "
                  "product, and try again.")
        elif self.verbose:
            print(f"GENERATE> using {self.env['label']}={self.env['path']}.")

    def set_real_and_abstract_location(self):
        """ Substitute path keywords

        Substitute the keywords into the location
        to form a real location, and replace with
        upper case for the abstract location

        """
        self.real_location = self.abstract_location = None
        real = {}
        abstract = {}
        for keyword in self.keywords:
            try:
                key, value = keyword.split("=")
                real[key] = value
                abstract[key] = get_abstract_key(key=key)
            except:
                print("GENERATE> %r is an invalid key=value assignment")
        try:
            self.real_location = self.location.format(**real)
            self.abstract_location = self.location.format(**abstract)
        except Exception as e:
            print(f"GENERATE {e}> key {key} is missing from location={self.location}")

    def set_datamodel_dir(self):
        """Set the DATAMODEL_DIR from the environment"""

        self.datamodel_dir = os.getenv("DATAMODEL_DIR", None)

        if not self.datamodel_dir:
            print("GENERATE> Please set DATAMODEL_DIR")
        elif not exists(self.datamodel_dir):
            print(f"GENERATE> Nonexistent DATAMODEL_DIR at {self.datamodel_dir}")
            self.datamodel_dir = None
        elif self.verbose:
            print(f"GENERATE> DATAMODEL_DIR = {self.datamodel_dir}")

    def set_sas_base_dir(self):
        """Set the SAS_BASE_DIR from the environment"""

        self.sas_base_dir = os.getenv("SAS_BASE_DIR", None)

        if not self.sas_base_dir:
            print("GENERATE> Please set SAS_BASE_DIR")
        elif not exists(self.sas_base_dir):
            print(f"GENERATE> Nonexistent SAS_BASE_DIR at {self.sas_base_dir}")
            self.sas_base_dir = None
        elif self.verbose:
            print(f"GENERATE> SAS_BASE_DIR = {self.sas_base_dir}")

    def set_directory(self):
        """ Set the output directory

        Set the output directory from the tree_ver, env_label and location
        and confirm it exists (try making it if it doesn't)

        """
        self.directory = None
        if not self.format:
            print("GENERATE> Please set a valid format option")
        elif not self.path:
            print("GENERATE> Please set path option, or set env_label and location options")
        elif self.datamodel_dir and self.abstract_location:
            formats = [self.format, "access", "yaml", "json"]
            self.directory = {}
            data_dir = join(self.datamodel_dir, "data")
            for format in formats:
                directory = join(data_dir, format, self.env_label)
                if format != "access":
                    directory = join(directory, dirname(self.abstract_location))
                if not exists(directory):
                    try:
                        os.makedirs(directory)
                        if self.verbose:
                            print(f"GENERATE> creating directory at {directory}")
                    except Exception as e:
                        print(f"GENERATE> cannot create directory at {directory}")
                        print(f"--> EXCEPTION={e}")
                        directory = None
                if directory:
                    self.directory[format] = directory

    def set_file(self):
        """ Set the input file

        Set the input file from the tree_ver and location
        and confirm it exists
        """
        self.set_env()
        if self.env and "path" in self.env:
            if not exists(self.env["path"]):
                print(f"GENERATE> Nonexistent environ at {self.env}")
                self.file = None
            else:
                self.file = (
                    join(self.env["path"], self.real_location) if self.real_location else None
                )
                if not self.file:
                    print("GENERATE> Please set location option")
                elif not exists(self.file):
                    print(f"GENERATE> Nonexistent file at {self.file}")
                    self.file = None
        else:
            self.file = None

    def set_file_spec_from_location(self):
        """ Set file species from file location """
        namesplit = re.split("[-.]", basename(self.location))
        self.file_spec = get_file_spec(namesplit[0]) if len(namesplit) > 1 else None

    def set_stub(self, skip_git=False):
        """ Set the Stub Class

        Set the stub class and use it to write output
        from the template

        """
        self.stub = Stub(file_spec=self.file_spec, directory=self.directory,
                         verbose=self.verbose, force=self.force)
        # updates the local datamodel git repo
        if not skip_git:
            self.stub.git.pull()
            self.stub.git.status()
        # creates the access path file
        self.stub.set_access(path=self.path, replace=self.replace)
        # creates the dictionary of inputs into the various stubs
        self.stub.set_input(path=self.file, format=self.format)
        self.stub.set_input_hdus()
        # creates the Jinja2 environment
        self.stub.set_environment()
        # creates the yaml cache
        self.stub.set_cache()
        # creates the Jinja2 template
        self.stub.set_template()
        # creates the output filepaths for various formats, i.e. yaml, md, json, etc
        self.stub.set_output()
        # creates the output results, as a rendered string
        self.stub.set_result()
        # writes out the rendered strings into each file ; also performs git add + commit on files
        for format in [self.format, "yaml", "json"]:
            self.stub.write(format=format, skip_git=skip_git)
        # closes any open file HDUs
        self.stub.close_input_hdus()
        # git pushes the results
        if not skip_git:
            self.stub.git.push()
