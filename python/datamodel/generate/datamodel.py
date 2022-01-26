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
import pathlib

from typing import TypeVar, Type, Union, List

from .parse import get_abstract_path, get_abstract_key, get_file_spec
from datamodel import log

from astropy.io import fits
from datamodel.generate.stub import stub_iterator
from tree import Tree
from sdss_access.path import Path
from pydantic import ValidationError

from ..git import Git
from .stub import BaseStub

# Create a generic variable that can be 'DataModel', or any subclass.
D = TypeVar('D', bound='DataModel')


def prompt_for_access(filename: str, path_name: str = None, config: str = None) -> tuple:
    """ Prompt the user to verify or define information

    Takes the user through a variety of input prompts in order to verify any existing
    entry in sdss_access, or to define a new file species, symbolic path location, and
    example variable=value key mappings for the input file.

    Parameters
    ----------
    filename : str
        The full path to the file
    path_name : str, optional
        Any existing sdss_access path_name / file_species, by default None
    config : str, optional
        What tree config version, or release the file corresponds to, by default None

    Returns
    -------
    tuple
        a tuple of path_name, path_template, path_keys
    """

    # prompt for sdss_access entry
    if not path_name:
        in_sdss = input('Does this file have an existing sdss_access definition? (y/n): ')
    else:
        in_sdss = 'y'

    # resolve path_name, path_template, and path_keys
    if in_sdss in ['y', "Y"]:
        # look up path name and template in sdss_access
        path = Path(release=config)
        if not path_name:
            path_name = input('What is the sdss_access path_name?: ')
        path_template = path.templates.get(path_name, path.templates.get(path_name.lower(), None))
        if not path_template:
            log.warning(f'No path_template could be found for path_name {path_name}.  Check syntax.')
            return

        # strip template of $envvar
        path_template = path_template[1:] if path_template.startswith('$') else path_template

        # attempt to extract the proper name=value mappings from the filename and path_name
        keys = path.lookup_keys(path_name)
        keymaps = path.extract(path_name, filename)
        if not keymaps:
            path_keys = input(f'Could not extract a value mapping for keys: {keys}\n'
                              'Please define a list of name=value key mappings for variable substitution. \n'
                              'e.g. drpver=v2_4_3, plate=8485, ifu=1901, wave=LOG\n:')
            path_keys = path_keys.replace(' ','').split(',')
        else:
            path_keys = [f'{k}={v}' for k,v in keymaps.items()]
    elif in_sdss in ['n', 'N']:
        # prompt for new path definitions
        path_name = input('Define a new path_name / file_species, e.g. mangaRss: ')
        path_template = input('Define a new path template, starting with an environment '
                              'variable label.\nUse jinja {} templating to define variable name used for substitution.\n'
                              'e.g. "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"\n: ')
        path_keys = input('Define a list of name=value key mappings for variable substitution. \n'
                          'e.g. drpver=v2_4_3, plate=8485, ifu=1901, wave=LOG\n: ')
        path_keys = path_keys.replace(' ','').split(',')

    # confirm the choices
    msg = (f"\nConfirm the following: (y/n): \n file = {filename} \n path_name = {path_name}\n "
           f"path_template = {path_template}\n path_keys = {path_keys}\n ")
    confirm = input(msg)
    if confirm not in ['y', 'Y']:
        return None, None, None

    return path_name, path_template, path_keys

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
    filename : str, optional
        A full filepath to a real file on disk to create the datamodel for
    access_path_name : str, optional
        A name of the path name in sdss_access, if different than the file species name, by default None
    design : bool, optional
        If True, indicates the datamodel is in a design phase, by default None

    Raises
    ------
    ValueError
        when neither a path nor a (env_label + location) are specified
    ValueError
        when no path template keywords are specified
    """
    supported_filetypes = ['.fits', '.par']

    def __init__(self, tree_ver: str = None, file_spec: str = None, path: str = None,
                 keywords: list = [], env_label: str = None, location: str = None,
                 verbose: bool = None, release: str = None, filename: str = None, 
                 access_path_name: str = None, design: bool = False) -> None:

        # environment options
        self.tree_ver = tree_ver
        self.release = release
        self.tree = None
        self.env = None

        # file options
        self.filename = filename
        self.file_species = get_file_spec(file_spec=file_spec)
        self.path = path
        self.keywords = keywords
        self.kwargs = None
        self.env_label = env_label
        self.location = location
        self.template = None
        self.real_location = None
        self.abstract_location = None
        self.file = None
        self.design = design

        # setting options
        self.verbose = verbose

        # access options
        self.access = {}
        self.access_string = None
        self.in_sdss_access = None
        self._access_path_name = access_path_name 

        # check for a real filename
        if self.filename:
            self.file_species, self.path, self.keywords = prompt_for_access(self.filename,
                                                                            self.file_species,
                                                                            self.tree_ver or self.release)

        # set path, locations, and file_species
        if not self.path and not (self.env_label and self.location):
            raise ValueError('Either a path or an env_label + location must be specified.')
        
        # check if keywords are expected
        if re.search(r'{(.*?)}', self.path) and not self.keywords and not self.design:
            raise ValueError('A set of keywords must be provided along with a either a '
                             'path or location.')
        self._construct_path()

        # set the file species from the location
        if not self.file_species:
            self._set_file_spec_from_location()

        # create the tree and file locations
        self._set_tree()
        if self.design:
            self._set_design_location()
        else:
            self._set_real_and_abstract_location()

        # check for valid file support
        self.suffixes = pathlib.Path(self.location).suffixes
        if set(self.suffixes).isdisjoint(set(self.supported_filetypes)):
            raise ValueError(f'File type {self.suffixes[0]} is not currently supported by sdss-datamodel.')    

        # set the fully realized filename and access paths
        self._set_file()
        self._set_access()

        # set a git instance
        self._git = Git(verbose=verbose)

    def __repr__(self) -> str:
        """ Repr for DataModel """
        return f"<DataModel(file_species='{self.file_species}', release='{self.release}')>"

    @classmethod
    def from_file(cls: Type[D], filename: str, path_name: str = None, tree_ver: str = None,
                  verbose: bool = None) -> D:
        """ class method to create a datamodel from an absolute filepath

        Creates a DataModel for a given full path to a file.  Prompts the user to
        verify any existing entry in sdss_access for the input file, or to define
        a new file_species / path_name, symbolic path location, and example
        variable_name=value key mappings.

        Parameters
        ----------
        filename : str
            The full path to the file
        path_name : str, optional
            The existing sdss_access path name if any, by default None
        tree_ver : str, optional
            The SDSS tree version or release associated with the file, by default None
        verbose : bool, optional
            If True, creates the DataModel with verbosity, by default None

        Returns
        -------
        DataModel
            a SDSS DataModel instance
        """
        file_species, path, keys = prompt_for_access(filename, path_name, tree_ver)
        if not file_species:
            return None
        return DataModel(file_spec=file_species, path=path, keywords=keys, verbose=verbose, tree_ver=tree_ver)

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
    
    def _set_design_location(self) -> None:
        """ Sets the abstract file location for the design """
        design_keys = re.findall(r'{(.*?)}', self.location)
        abstract = {key: get_abstract_key(key=key) for key in design_keys}
        self.abstract_location = self.location.format(**abstract)
        if self.verbose:
            log.info(f'Designing abstract location {self.abstract_location}')
        
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

        self.kwargs = real.copy()
        try:
            self.real_location = self.location.format(**real)
            self.abstract_location = self.location.format(**abstract)
        except Exception as e:
            log.error(f"GENERATE {e}> key {key} is missing from location={self.location}")

    def _set_file(self) -> None:
        """ Set the input (real) filepath and check for existence """

        # get the environment
        self._set_env()

        if not self.env or "path" not in self.env:
            log.error('No datamodel environment found!')
            return

        if not os.path.exists(self.env["path"]):
            log.error(f"Nonexistent environ at {self.env}")
            return
        
        # exit if in design phase
        if self.design:
            return

        if not self.real_location:
            log.error('Cannot build file path. No real location identified.')
            return

        self.file = os.path.join(self.env["path"], self.real_location)

        if not os.path.exists(self.file):
            log.error(f"Nonexistent file at {self.file}")

        if self.verbose:
            log.info(f'Using real file: {self.file}')

    @property
    def file_exists(self):
        """ Checks for file existence on disk """
        return os.path.isfile(self.file) if self.file else False

    def _set_env(self) -> None:
        """ Create an environment dictionary

        Create a dictionary containing the env_label and its path definition
        from tree[env_label].
        """
        if not self.env_label:
            log.error("Please specify a valid env label option.")
            return

        orig_env = self.tree.get_orig_os_environ()
        tree_dict = self.tree.to_dict()
        if self.env_label in tree_dict:
            path = tree_dict[self.env_label]

            # check if path is a PRODUCT_ROOT
            if path.startswith("$PRODUCT_ROOT"):

                if self.verbose:
                    log.info(f'{self.env_label} path is a PRODUCT_ROOT') 
                              
                # check for existing label in enironemnt
                if self.env_label in orig_env:
                    path = orig_env.get(self.env_label)
                else:
                    # try to resolve your product_root path
                    path = os.path.expandvars(path) 
                    
                    if path.startswith("$PRODUCT_ROOT"):                    
                        # look for a valid product root
                        product_root = self.tree.get_product_root()
                        # fail if PRODUCT_ROOT is not set
                        if not product_root:
                            msg = 'No PRODUCT_ROOT found in your environment!  Please set your root directory for all git or svn products.'
                            log.error(msg)
                            raise ValueError(msg)
           
                        # replace product_root with one found from tree
                        path = path.replace("$PRODUCT_ROOT", product_root)
                
            # assign environment label and path
            self.env = {"label": self.env_label, "path": path}

        # issue error or info log messages
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
        # set the access path name 
        aname = self._access_path_name or self.file_species

        # create the original access string
        self.access_string = f"{aname} = ${self.path}"

        # create the dictionary for the current release
        self.access[self.release] = {'release': self.release, 'tree_ver': self.tree_ver,
                                     'access': self.access_string, 'in_sdss_access': None,
                                     'path_name': None, 'path_template': None,
                                     'path_kwargs': None}

        # check if the file species already exists in sdss_access
        path_keys = self.tree.paths.keys()
        self.in_sdss_access = aname in path_keys or \
            aname.lower() in [i.lower() for i in path_keys]
        self.access[self.release]['in_sdss_access'] = self.in_sdss_access

        if self.in_sdss_access:
            path = Path(release=self.tree_ver)
            # find the correct path name
            if aname in path_keys:
                name = aname
            elif aname.lower() in path_keys:
                name = aname.lower()
            elif aname.lower() in [i.lower() for i in path_keys]:
                name = aname.lower()
            else:
                name = None
            # lookup the sdss_access information
            self.access[self.release]['path_name'] = name
            self.access[self.release]['path_template'] = self.tree.paths[name]
            self.access[self.release]['path_kwargs'] = list(set(path.lookup_keys(name)))

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

    def write_stubs(self, format: str = None, force: bool = None, use_cache_release: str = None,
                    full_cache: bool = None) -> None:
        """ Write out the stub files

        Write out all stubs or a stub of a given format.

        Parameters
        ----------
        format : str, optional
            A stub format to write out, by default None
        force : bool, optional
            If True, forces a rewrite of the cached stub content
        use_cache_release: str, optional
            Specify a cached release to use to copy over custom user content
        full_cache: bool, optional, by default None
            If True, use the entire cached YAML release, rather than only the HDUs
        """
        if self.verbose:
            log.info(f'Preparing datamodel: {self}.')

        for stub in stub_iterator(format=format):
            ss = stub(self)
            if self.verbose:
                log.info(f'Creating stub: {ss}')
            ss.write(force=force, use_cache_release=use_cache_release, full_cache=full_cache)

    def remove_stubs(self, format: str = None, git: bool = None) -> None:
        """ Remove the stub files

        Remove all stubs or a stub of a given format.

        Parameters
        ----------
        format : str, optional
            A stub format to remove, by default None
        git : bool, optional
            If True, removes from the git repo
        """
        for stub in stub_iterator(format=format):
            ss = stub(self)
            if self.verbose:
                log.info(f'Removing stub: {ss}')

            # either remove locally or from git
            if git:
                try:
                    ss.remove_from_git()
                except RuntimeError:
                    log.info("Could not perform git remove.  Falling back to local remove.")
                    ss.remove_output()
            else:
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
        
    def design_hdu(self, ext: str = 'primary', extno: int = None, name: str = 'EXAMPLE', 
                   description: str = None, header: Union[list, dict, fits.Header] = None, 
                   columns: List[Union[list, dict, fits.Column]] = None, **kwargs):
        """ Design a new HDU

        Design a new astropy HDU for the given datamodel.  Specify the extension type ``ext`` 
        to indicate a PRIMARY, IMAGE, or BINTABLE HDU extension.  Each new HDU is added to the
        YAML structure using next hdu extension id found, or the one provided with ``extno``.  Use
        ``name`` to specify the name of the HDU extension.  Each call to this method will write out 
        the new HDU to the YAML design file.     

        ``header`` can be a `~astropy.io.fits.Header` instance, a list of tuples of header keywords, 
        conforming to (keyword, value, comment), or list of dictionaries conforming to 
        {"keyword": keyword, "value": value, "comment": comment}.

        ``columns`` can be a list of `~astropy.io.fits.Column` objects, a list of tuples 
        minimally conforming to (name, format, unit), or list of dictionaries minimally conforming
        to {"name": name, "format": format, "unit": unit}.  See Astropy's Binary Table 
        `Column Format <https://docs.astropy.org/en/stable/io/fits/usage/table.html#column-creation>`_
        for the allowed format values.  When supplying a list of tuples or dictionaries, can include
        any number of valid arguments into `~astropy.io.fits.Column`.
        
        Parameters
        ----------
        ext : str, optional
            the type of HDU to create, by default 'primary'
        extno : int, optional
            the extension number, by default None
        name : str, optional
            the name of the HDU extension, by default 'EXAMPLE'
        description: str, optional
            a description for the HDU, by default None
        header : Union[list, dict, fits.Header], optional
            valid input to create a Header, by default None
        columns : List[Union[list, dict, fits.Column]], optional
            a list of binary table columns, by default None
        force : bool
            If True, forces a new design even if the HDU already exists, by default None
        **kwargs, optional
            additional keyword arguments to pass to the HDU constructor

        Raises
        ------
        ValueError
            when the ext type is not supported
        ValueError
            when the table columns input is not a list
        """
        
        if not self.design:
            log.warning('Cannot design an HDU when not in the datamodel design phase.')
            return

        # get the stub and update from disk
        ss = self.get_stub(format='yaml')
        ss.update_cache()
        
        # design the new HDU
        ss.design_hdu(ext=ext, extno=extno, name=name, description=description, 
                      header=header, columns=columns, **kwargs)

        # write it out to the yaml stub        
        ss.write()
        
        
    def generate_designed_file(self, redesign: bool = None, **kwargs):
        """ Generate a file from a designed datamodel

        Generates a real file on disk from a designed datamodel. If there are any
        path template keywords, they must be specified here as input keyword arguments
        to convert the symbolic path / abstract location to a real example location on 
        disk.  After generating the file, the datamodel sets ``design`` to False and exits
        design mode.   
        
        Parameters
        ----------
        redesign : bool
            If True, re-enters design mode to create a new file
        kwargs
            Any path keyword arguments to be filled in
        
        Raises
        ------
        KeyError
            when there are missing path keywords
        AttributeError
            when the release is not WORK when in the datamodel design phase
        """
        if redesign:
            log.info("Re-entering datamodel design mode. Setting to True.")
            self.design = True

        if not self.design:
            log.warning('Cannot generate a file when not in the datamodel design phase.')
            return
        
        if self.design and self.release != 'WORK':
            raise AttributeError(f'The release {self.release} must be "WORK" when in '
                                 'the datamodel design phase.')

        # create a real location and filepath
        try:
            self.real_location = self.location.format(**kwargs)
        except KeyError as e:
            raise KeyError(f'Must specify path keywords to generate a real file: {e}') from e
        else:    
            self.file = os.path.join(self.env["path"], self.real_location)
            
        # generate the designed HDUList
        ss = self.get_stub(format='yaml')
        ss.update_cache()
        try:
            hdulist = ss.create_hdulist_from_cache(release='WORK')
        except ValidationError as e:
            log.error(f'Failed to create a valid HDUList')
            raise
        
        # exit if for any reason hdulist doesn't exist
        if not hdulist:
            log.error('No HDUList to write out.')
            return
        
        # create directories if needed
        path = pathlib.Path(self.file)
        if not path.parent.exists():
            log.info(f'Creating directory: {path.parent}')
            path.parent.mkdir(parents=True)
        
        # write out the designed file
        hdulist.writeto(self.file, overwrite=True, checksum=True)
        
        if self.verbose:
            log.info(f'Writing designed filepath: {self.file}')
            log.info("Setting datamodel design mode to False")

        # set design to False
        # updates the YAML cache with the file and real locations
        self.design = False if not redesign else self.design
        ss = self.get_stub(format='yaml')
        ss.write()
        
        

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
