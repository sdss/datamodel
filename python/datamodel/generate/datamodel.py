# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: product.py
# Project: generate
# Author: Brian Cherinka
# Created: Wednesday, 10th February 2021 3:14:50 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Wednesday, 10th February 2021 3:14:50 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

import os
import re

from .parse import get_abstract_path, get_abstract_key, get_file_spec
from datamodel import log

from datamodel.generate.stub import stub_iterator
from tree import Tree
from sdss_access.path import Path

from ..git import Git
from .stub import BaseStub


# TODO - add option to specify a real filepath
# TODO - add a user prompt for sdss_access

class DataModel(object):
    """ Class to enable datamodel file generation for a given product

    This class is used to generate valid SDSS datamodel files for a given
    data product.

    Parameters
    ----------
    tree_ver : str, optional
        an SDSS Tree configuration name, by default None
    file_spec : str, optional
        The name of the file species (or sdss_access path name), by default None
    path : str, optional
        A file path template definition, by default None
    keywords : list, optional
        A list of path template keyword-value pairs, by default None
    env_label : str, optional
        The environment variable name of the file's location, by default None
    location : str, optional
        A path location relative to the environment variable, by default None
    verbose : bool, optional
        If True, turn on verbosity logging, by default None
    release : str, optional
        The name of the SDSS release the file is a part of, by default None

    Raises
    ------
    ValueError
        when neither a path nor a (env_label + location) are specified
    ValueError
        when no path template keywords are specified
    """

    def __init__(self, tree_ver: str = None, file_spec: str = None, path: str = None,
                 keywords: list = None, env_label: str = None, location: str = None,
                 verbose: bool = None, release: str = None) -> None:

        # environment options
        self.tree_ver = tree_ver
        self.release = release
        self.tree = None
        self.env = None

        # file options
        self.file_species = get_file_spec(file_spec=file_spec)
        self.path = path
        self.keywords = keywords
        self.env_label = env_label
        self.location = location
        self.template = None
        self.real_location = None
        self.abstract_location = None
        self.file = None

        # setting options
        self.verbose = verbose

        # access options
        self.access = {}
        self.access_string = None
        self.in_sdss_access = None

        # set path, locations, and file_species
        if not self.path and not (self.env_label and self.location):
            raise ValueError('Either a path or an env_label + location must be specified.')
        if not self.keywords:
            raise ValueError('A set of keywords must be provided along with a either a '
                             'path or location.')
        self._construct_path()

        # set the file species from the location
        if not self.file_species:
            self._set_file_spec_from_location()

        # create the tree and file locations
        self._set_tree()
        self._set_real_and_abstract_location()

        # set the fully realized filename and access paths
        self._set_file()
        self._set_access()

        # set a git instance
        self._git = Git(verbose=verbose)

    def __repr__(self) -> str:
        """ Repr for DataModel """
        return f"<DataModel(file_species='{self.file_species}', release='{self.release}')>"

    def _construct_path(self) -> None:
        """ Construct a path, template path, or env_label and location """
        if not self.path:
            self.path = os.path.join(self.env_label, self.location)
        else:
            try:
                self.env_label, self.location = self.path.split(os.sep, 1)
            except ValueError:
                pass

        self.template = f'${get_abstract_path(self.path, add_brackets=True)}'

    def _set_file_spec_from_location(self) -> None:
        """ Extract file species name from file location """

        namesplit = re.split("[-.]", os.path.basename(self.location))
        self.file_species = get_file_spec(namesplit[0]) if len(namesplit) > 1 else None

    def _set_tree(self) -> None:
        """ Setup the SDSS Tree

        Sets a valid Tree from an input tree_ver (config name) or valid release.  If a release is
        specified on input, attempts to convert it to a valid tree configuration.  If no release
        is specified and no input tree_ver is given, defaults to the currently loaded module
        using the TREE_VER environment variable.

        """
        if self.tree_ver and self.release:
            raise AttributeError('Both tree_ver and release cannot be set.  Only specify one or the other.')

        # if not TREE_VER and a release, attempt to get valid tree_ver
        if self.tree_ver is None and self.release:
            releases = Tree.get_available_releases()
            if self.release not in releases:
                raise ValueError(f"release {self.release} is not yet in the SDSS Tree.")
            self.tree_ver = releases[releases.index(self.release)].lower()

        # attempt to get the TREE_VER
        if self.tree_ver is None:
            self.tree_ver = os.getenv('TREE_VER', None)

        # add the tree and config_name
        self.tree = Tree(config=self.tree_ver)
        if self.tree_ver != self.tree.config_name:
            self.tree_ver = self.tree.config_name

        # add the tree release (also as check to ensure proper one gets set)
        self.release = self._get_tree_release()

    def _get_tree_release(self) -> str:
        """ Get a tree release in a backwards compatible way """

        # if the tree has release attribute, use it
        if hasattr(self.tree, 'release'):
            return self.tree.release

        # convert the tree config name into a release name
        release = self.tree.config_name.upper()
        if 'work' in self.tree.config_name or self.tree.config_name == 'sdss5':
            release = 'WORK'
        return release

    def _set_real_and_abstract_location(self) -> None:
        """ Create a real location from path keywords

        Substitute the path keywords into the template location
        to form a real location.  Create an abstract location using
        upper case keyword names.

        """
        real = {}
        abstract = {}
        for keyword in self.keywords:
            try:
                key, value = keyword.split("=")
                real[key] = value
                abstract[key] = get_abstract_key(key=key)
            except:
                log.error(f"GENERATE> {keyword} is an invalid key=value assignment")

        try:
            self.real_location = self.location.format(**real)
            self.abstract_location = self.location.format(**abstract)
        except Exception as e:
            log.error(f"GENERATE {e}> key {key} is missing from location={self.location}")

    def _set_file(self) -> None:
        """ Set the input (real) filepath and check for existence """

        # get the environment
        self._set_env()

        if not self.env and "path" not in self.env:
            log.error('No datamodel environment found!')
            return

        if not os.path.exists(self.env["path"]):
            log.error(f"Nonexistent environ at {self.env}")
            return

        if not self.real_location:
            log.error('Cannot build file path. No real location identified.')
            return

        self.file = os.path.join(self.env["path"], self.real_location)

        if not os.path.exists(self.file):
            log.error(f"Nonexistent file at {self.file}")

        if self.verbose:
            log.info(f'Using real file: {self.file}')

    def _set_env(self) -> None:
        """ Create an environment dictionary

        Create a dictionary containing the env_label and its path definition
        from tree[env_label].
        """
        if not self.env_label:
            log.error("Please specify a valid env label option.")
            return

        tree_dict = self.tree.to_dict()
        if self.env_label in tree_dict:
            self.env = {"label": self.env_label, "path": tree_dict[self.env_label]}

        if not self.env:
            log.error(f"Please add this environment={self.env_label} to the tree "
                      "product, and try again.")
        elif self.verbose:
            log.info(f"Using environment {self.env['label']}={self.env['path']}.")

    def _set_access(self) -> None:
        """ Sets the access path dictionary

        Sets a dictionary containing access parameters for the current
        datamodel release.  Access parameters are path name and
        template definitions used by sdss_access, as well a resolved
        "access string", and a boolean indicating if its already in
        sdss_access.

        """
        # create the original access string
        self.access_string = f"{self.file_species} = ${self.path}"

        # create the dictionary for the current release
        self.access[self.release] = {'release': self.release, 'tree_ver': self.tree_ver,
                                     'access': self.access_string, 'in_sdss_access': None,
                                     'path_name': None, 'path_template': None,
                                     'path_kwargs': None}

        # check if the file species already exists in sdss_access
        path_keys = self.tree.paths.keys()
        self.in_sdss_access = self.file_species in path_keys or \
            self.file_species.lower() in [i.lower() for i in path_keys]
        self.access[self.release]['in_sdss_access'] = self.in_sdss_access

        if self.in_sdss_access:
            path = Path(release=self.tree_ver)
            # find the correct path name
            if self.file_species in path_keys:
                name = self.file_species
            elif self.file_species.lower() in path_keys:
                name = self.file_species.lower()
            elif self.file_species.lower() in [i.lower() for i in path_keys]:
                name = self.file_species.lower()
            else:
                name = None
            # lookup the sdss_access information
            self.access[self.release]['path_name'] = name
            self.access[self.release]['path_template'] = self.tree.paths[name]
            self.access[self.release]['path_kwargs'] = path.lookup_keys(name)

    def get_stub(self, format: str = 'yaml') -> BaseStub:
        """ Get a datamodel Stub

        Return a datamodel Stub for a given format.

        Parameters
        ----------
        format : str, optional
            the stub format to return, by default 'yaml'

        Returns
        -------
        BaseStub
            an instance of a stub class
        """
        stub = list(stub_iterator(format=format))
        return stub[0](self) if stub else None

    def write_stubs(self, format: str = None) -> None:
        """ Write out the stub files

        Write out all stubs or a stub of a given format.

        Parameters
        ----------
        format : str, optional
            A stub format to write out, by default None
        """
        if self.verbose:
            log.info(f'Preparing datamodel: {self}.')

        for stub in stub_iterator(format=format):
            ss = stub(self)
            if self.verbose:
                log.info(f'Creating stub: {ss}')
            ss.write()

    def remove_stubs(self, format: str = None) -> None:
        """ Remove the stub files

        Remove all stubs or a stub of a given format.

        Parameters
        ----------
        format : str, optional
            A stub format to remove, by default None
        """
        for stub in stub_iterator(format=format):
            ss = stub(self)
            if self.verbose:
                log.info(f'Removing stub: {ss}')
            ss.remove_output()

    def commit_stubs(self, format: str = None) -> None:
        """ Commit the stub files into git

        Commit stub files into git.  Performs a git pull, commits all
        stubs into the repo, and attempts a git push.  Optionally specify
        a format to only commit a specific stub.

        Parameters
        ----------
        format : str, optional
            A stub format to commit, by default None
        """
        # attempt a git pull
        self._git.pull()

        # commit the stubs
        for stub in stub_iterator(format=format):
            ss = stub(self)
            if self.verbose:
                log.info(f'Committing stub: {ss}')
            ss.commit_to_git()

        # attempt a push
        self._git.push()

#
# code to create a markdown table

# def test(hdus):
#      results = ['No.    Name      Ver    Type      Cards   Dimensions   Format']
#      format = '{:3d}  {:10}  {:3} {:11}  {:5d}   {}   {}   {}'
#      default = ('', '', '', 0, (), '', '')
#      for idx, hdu in enumerate(hdus):
#          summary = hdu._summary()
#          if len(summary) < len(default):
#              summary += default[len(summary):]
#          summary = (idx,) + summary
#          #if output:
#          #    results.append(format.format(*summary))
#          #else:
#          results.append(summary)
#      return results

# def table(ll):
#      #ll=test(hdu)
#      #ll=hdu
#      ll.insert(1,'|:---|:---|:---|:---|:---|:---|:---|')
#      tab = ['|'.join([str(k) for k in i]) if type(i)==tuple else i for i in ll]
#      return tab

# def _create_basic_table(self, hdus):
#      from io import StringIO
#      import re
#      s = StringIO()
#      hdus.info(output=s)
#      s.seek(0)
#      ee = ''.join(s.readlines()).split('\n')
#      ee.insert(2, '|:---|:---|:---|:---|:---|:---|:---|')
#      tmp = [re.sub(r'\|+', '|', '|'.join(i.split('  '))) for i in ee if not i.startswith('File') and i != '']
#      return tmp
