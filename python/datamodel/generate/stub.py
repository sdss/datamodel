# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: stub_new.py
# Project: generate
# Author: Brian Cherinka
# Created: Tuesday, 23rd February 2021 10:41:09 am
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Tuesday, 23rd February 2021 10:41:09 am
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import abc
import yaml
import os
from jinja2 import Environment, PackageLoader
from typing import Iterator
from pydantic import ValidationError

from ..git import Git
from .changelog import yamldiff_selector
from ..models.releases import releases as sdss_releases
from ..models.yaml import YamlModel
from datamodel.generate.filetypes import file_selector, get_filetype, get_filesize
from datamodel import log


class BaseStub(abc.ABC):
    format = None
    cacheable = False
    has_template = True

    def __init__(self, datamodel = None, use_cache_release: str = None, full_cache: bool = None,
                 verbose: bool = None, force: bool = None):
        self.environment = None
        self.template = None
        self.output = None
        self.datamodel = datamodel
        self.verbose = verbose

        # cache control attrs
        self.use_cache_release = use_cache_release
        self.full_cache = full_cache
        self.force = force

        # content attrs
        self._template_input = None
        self._cache = None
        self.content = None
        self._validated_yaml = None

        # set up the Jinja 2 template + environment, and the output stub file path
        self._set_template()
        if self.datamodel:
            self._set_output()

        # setup a git object
        self.git = Git(verbose=self.verbose)

    def __repr__(self) -> str:
        if self.datamodel:
            return (f'<Stub(format="{self.format}", file_species="{self.datamodel.file_species}", '
                    f'release="{self.datamodel.release}")>')
        else:
            return f'<Stub(format="{self.format}")>'

    @classmethod
    def from_datamodel(cls, datamodel):
        return cls(datamodel=datamodel)

    def add_datamodel(self, datamodel):
        self.datamodel = datamodel
        self._set_output()

    def _set_template(self) -> None:
        """ Set the jina2 environment including filters for content. """

        if not self.has_template:
            return

        loader = PackageLoader("datamodel", "templates")
        self.environment = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        self.template = self.environment.get_template(f'stub.{self.format}')

    def _set_datamodel_dir(self) -> None:
        """ Set the DATAMODEL_DIR from the environment """

        self.datamodel_dir = os.getenv("DATAMODEL_DIR", None)

        if not self.datamodel_dir:
            raise ValueError("No DATAMODEL_DIR found.  Please set a proper environment variable.")
        elif not os.path.exists(self.datamodel_dir):
            raise IOError(f"No datamodel directory found at {self.datamodel_dir}")

    def _set_output(self) -> None:

        if not self.datamodel:
            raise AttributeError('Cannot set an output directory without a valid datamodel')

        # create the output directory
        self._set_datamodel_dir()
        data_dir = os.path.join(self.datamodel_dir, "datamodel")
        products_dir = os.path.join(data_dir, "products")

        directory = os.path.join(products_dir, self.format)

        if not os.path.exists(directory):
            os.makedirs(directory)

        # set the output file path
        self.output = os.path.join(directory, f'{self.datamodel.file_species}.{self.format}')

    def remove_output(self) -> None:
        if self.output and os.path.exists(self.output):
            os.remove(self.output)

    def render_content(self, force: bool = None) -> None:
        if not self._cache or force:
            self._get_cache(force=force)

        if self.format != 'yaml' and not self.validate_cache():
            log.info('yaml cache is not validated!')
            return

        self._get_content()

    @abc.abstractmethod
    def _get_content(self):
        pass

    def write(self, force: bool = None, use_cache_release: str = None, full_cache: bool = None) -> None:

        self.use_cache_release = use_cache_release
        self.full_cache = full_cache
        self.force = force

        if not self.output:
            raise AttributeError('No output filepath set')

        # always re-render the content
        self.render_content(force=force)

        if not self.content:
            log.info('No cache content to write out!')
            return

        with open(self.output, 'w') as f:
            f.write(self.content)

    def update_cache(self, force: bool = None) -> None:
        """ Update the in-memory stub cache from the on-disk file """
        self._get_cache(force=force)

    def _prepare_input(self) -> dict:
        """ prepare the initial template input """

        template_input = {}
        if not self.datamodel:
            raise AttributeError('Cannot prepare template input without a valid datamodel')

        # check if datamodel file is real when not in design phase
        if not self.datamodel.design and not os.path.exists(self.datamodel.file):
            raise IOError(f'File {self.datamodel.file} does not exist.  Cannot prepare input.')

        # create input dictionary for the template
        template_input = {
            "file_species": self.datamodel.file_species,
            'file_template': self.datamodel.template,
            "environments": [self.datamodel.env_label],
            "releases": [self.datamodel.release],
            "example": [self.datamodel.real_location],
            "location": [self.datamodel.location],
            "access": self._get_access_cache(),
            "design": self.datamodel.design
        }
        
        # add additional real info if not in the design phase
        if not self.datamodel.design:
            template_input.update({
                "path": self.datamodel.file,
                "filename": os.path.basename(self.datamodel.file),
                "filesize": get_filesize(self.datamodel.file),
                "filetype": get_filetype(self.datamodel.file)})
            
        return template_input

    def _get_access_cache(self) -> dict:
        return {"in_sdss_access": self.datamodel.in_sdss_access,
                "path_name": self.datamodel.access[self.datamodel.release]['path_name'],
                "path_template": self.datamodel.access[self.datamodel.release]['path_template'],
                "path_kwargs": self.datamodel.access[self.datamodel.release]['path_kwargs'],
                "access_string": self.datamodel.access[self.datamodel.release]['access']}

    def _create_cache(self) -> dict:
        if not self.cacheable or not self.has_template:
            raise ValueError(f'Cannot create a new cache.  The {self.format} stub is not '
                             'cacheable or does not have a valid template to create a cache. '
                             'Please create a cacheable yaml file first.')

        # prepare initial cache input
        input = self._prepare_input()
        return yaml.load(self.template.render(input), Loader=yaml.FullLoader)

    def _get_cache(self, force: bool = None) -> None:
        # only cache-able format is yaml - load that content
        cached_file = self.output.replace(self.format, 'yaml')

        if os.path.exists(cached_file) and not force:
            # read existing cache
            with open(cached_file) as file:
                content = yaml.load(file, Loader=yaml.FullLoader)
                content = self._check_release_in_cache(content)
        else:
            # create a brand new cache
            content = self._create_cache()
        
        # select the correct file object
        suffix = content['general']['datatype'] or get_filetype(self.datamodel.location)
        file_class = file_selector(suffix)

        # raise error if no class found
        if not file_class:
            raise ValueError(f'No supported file class found for {suffix}.')

        # update any design entry
        content['general']['design'] = self.datamodel.design

        # check the content dictionary has a proper release
        if self.datamodel.release not in content['releases']:
            content['releases'][self.datamodel.release] = {"template": None, "example": None, "location": None,
                                                           "environment": None, "access": {}, 
                                                           file_class.cache_key: {}}

        # set the cache content
        self._cache = content
        
        # instantiate the file object
        self.selected_file = file_class(self._cache, datamodel=self.datamodel, stub=self)

        # if release is the same, copy over entire cache
        if self.use_cache_release and self.full_cache:
            self.selected_file._use_full_cache()
            self._update_cache_changelog()
            return

        # set the cache with access info
        self._update_cache_access()

        # check the filetype and generate proper YAML content
        self.selected_file._set_cache(force=force)

        # update the cache changelog
        self._update_cache_changelog()

    def _check_release_in_cache(self, content: dict) -> dict:
        """ updates the yaml.general.releases list with new releases """
        # sort the sdss release list
        sdss_releases.sort('release_date')

        # load and updates the yaml release list
        releases = content['general']['releases']
        if self.datamodel.release not in releases:
            releases.append(self.datamodel.release)
            # sort by the sdss release date; work release always is latest
            releases.sort(key=lambda x: sdss_releases.list_names().index(x))
            content['general']['releases'] = releases
        return content

    def _update_cache_access(self) -> None:
        """ update the cache with access info """
        # always updates the cache with latest datamodel
        # update the access dictionary in the cache
        self._cache['releases'][self.datamodel.release]['access'] = self._get_access_cache()

        # update the template/location, environment keywords in the cache
        self._cache['releases'][self.datamodel.release]['template'] = self.datamodel.template
        self._cache['releases'][self.datamodel.release]['environment'] = self.datamodel.env_label

        # update the general environments sections in cache
        if self.datamodel.env_label not in self._cache['general']['environments']:
            self._cache['general']['environments'].append(self.datamodel.env_label)

        # update the location/example keyword in the cache
        self._cache['releases'][self.datamodel.release]['location'] = self.datamodel.location
        self._cache['releases'][self.datamodel.release]['example'] = self.datamodel.real_location       

    def _update_cache_changelog(self):
        """ Update the changelog in the cache """
        # get the correct yamldiff class
        suffix = self._cache['general']['datatype'] or get_filetype(self.datamodel.location)
        yd_class = yamldiff_selector(suffix)
        # return if no class present
        if not yd_class:
            return

        # instantiate compute the changelog and update the cache
        yaml_diff = yd_class(self._cache)
        release_order = reversed(self._cache['general']['releases'])
        changelog = yaml_diff.generate_changelog(release_order, simple=True)
        self._cache['changelog']['releases'] = changelog

    def validate_cache(self):
        """ Validate the yaml cache """
        if not self._cache:
            log.info("No yaml cache to validate!")
            return False

        # validate the yaml cache
        try:
            self._validated_yaml = YamlModel.parse_obj(self._cache)
        except ValidationError as err:
            log.error(err)
            return False
        else:
            return True     

    def commit_to_git(self) -> None:
        """ Commit the stub to Github """
        # add and commit the file
        self.git.add(path=self.output)
        self.git.commit(path=self.output, message=f"committing {self.datamodel.file_species}.{self.format}")

    def push_to_git(self) -> None:
        """ Push changes to Github """
        # try a git pull
        self.git.pull()

        # try a git push
        self.git.push()

    def remove_from_git(self) -> None:
        """ Remove file from the git repo """
        if os.path.exists(self.output):
            self.git.rm(self.output)

    # def workflow(self):
    #     # create stub with datamodel
    #     # set the output file to write content
    #     # read content from yaml file and create cached content
    #     # for yaml format only, create the cache (has template, creates, uses, replaces cached content)
    #         # render yaml template with prepared template input
    #         # validate the yaml content
    #         # write out the contents into yaml file
    #     # for markdown format only (has template, only used cached content)
    #         # read the markdown template with yaml cache
    #         # validate the yaml content
    #         # write out the contents with cached content
    #     # for json format only (no template, only uses cached content)
    #         # read in yaml cache content
    #         # validate the yaml content
    #         # write out json file with cached content
    #     pass


class YamlStub(BaseStub):
    format: str = 'yaml'
    cacheable: bool = True

    def _get_content(self) -> None:
        self.content = yaml.dump(self._cache, sort_keys=False)

class MdStub(BaseStub):
    format: str = 'md'

    def _get_content(self, release: str = None, group: str = 'WORK') -> None:
        selected_release = self.get_selected_release(release=release, group=group)
        #hdus = self._cache['hdus'][selected_release]
        hdus = self._cache['releases'][selected_release].get('hdus', {})
        pars = self._cache['releases'][selected_release].get('par', {})
        self.content = self.template.render(content=self._cache, hdus=hdus, par=pars, 
                                            selected_release=selected_release)

    def get_selected_release(self, release: str = None, group: str = 'WORK') -> str:
        """ get the hdu content for a given release """
        cached_releases = list(self._cache['releases'].keys())
        if len(cached_releases) == 0:
            return release or self.datamodel.release
        elif len(cached_releases) == 1:
            return cached_releases[0]
        elif release in cached_releases:
            return release
        else:
            if release and release not in cached_releases:
                log.debug(f'Input release {release} unavailable in cache. '
                          f'Selecting latest release in group {group}')

            # TODO - move to separate function
            # groups releases and sorts them
            import itertools
            g = itertools.groupby(sorted(cached_releases, key=lambda x: x[0]), lambda x: x[0])
            key = {'D': 'DR', 'I': 'IPL', 'M': 'MPL', 'W': 'WORK'}
            rs = {}
            for i, gg in g:
                rs[key[i]] = sorted(gg, key=lambda x: int(x[2:]) if 'DR' in x else int(x[3:]) if 'PL' in x else x)

            # get latest release
            # set a fallback group; fallback either to WORK or DR group
            altgroup = 'WORK' if group != 'WORK' else 'DR'
            if group not in key.values():
                raise KeyError(f'group {group} is not a valid release group')
            elif group not in rs.keys():
                if altgroup not in rs.keys():
                    raise KeyError(f'group(s) {group}/{altgroup} not yet a cached release')
                else:
                    group = altgroup
            return rs[group][-1]

    def render_content(self, force: bool = None, release: str = None, group: str = 'WORK') -> None:
        if not self._cache or force:
            self._get_cache(force=force)

        if self.format != 'yaml' and not self.validate_cache():
            log.info('yaml cache is not validated!')
            return

        self._get_content(release=release, group=group)

    def write(self, force: bool = None, release: str = None, group: str = 'WORK',
              html: bool = None, use_cache_release: str = None, full_cache: bool = None) -> None:

        if not self.output:
            raise AttributeError('No output filepath set')

        # always re-render the content
        self.render_content(force=force, release=release, group=group)

        if not self.content:
            log.info('No cache content to write out!')
            return

        with open(self.output, 'w') as f:
            f.write(self.content)

class JsonStub(BaseStub):
    format: str = 'json'
    has_template: bool = False

    def _get_content(self) -> None:
        # uses orjson to dump; see orjson_dumps method in models/yaml.py
        # orjson options; indent=2, sort_keys = False (default)
        self.content = self._validated_yaml.json(by_alias=True) if self._validated_yaml else {}

class AccessStub(BaseStub):
    format: str = 'access'
    has_template: bool = False
    cacheable: bool = False

    def _get_content(self) -> None:
        releases = {k: v.get('access', {}) for k,v in self._cache['releases'].items()}
        self.content = yaml.dump(releases, sort_keys=False)


def stub_iterator(format: str = None) -> Iterator[BaseStub]:
    """ Iterator for all stub formats """
    for stub in [YamlStub, AccessStub, MdStub, JsonStub]:
        if format and format != stub.format:
            continue
        yield stub

