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
import json
from astropy.io import fits
from jinja2 import Environment, PackageLoader
import pathlib
from typing import Iterator, Type
from pydantic import ValidationError

try:
    import markdown
except ImportError:
    markdown = None

from ..git import Git
from .changelog import YamlDiff
from ..models.yaml import YamlModel
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

        directory = os.path.join(products_dir, self.format, self.datamodel.env_label)

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

        if not os.path.exists(self.datamodel.file):
            raise IOError(f'File {self.datamodel.file} does not exist.  Cannot prepare input.')

        # create input dictionary for the template
        template_input = {
            "path": self.datamodel.file,
            "file_species": self.datamodel.file_species,
            'file_template': self.datamodel.template,
            "filename": os.path.basename(self.datamodel.file),
            "filesize": self._get_filesize(),
            "filetype": self._get_filetype(),
            "environment": self.datamodel.env_label,
            "releases": [self.datamodel.release],
            "example": [self.datamodel.real_location],
            "location": [self.datamodel.location],
            "access": self._get_access_cache()
        }
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

        # check the content dictionary has a proper release
        if self.datamodel.release not in content['releases']:
            content['releases'][self.datamodel.release] = {"template": None, "example": None,
                                                           "location": None, "access": {}, "hdus": {}
                                                           }

        # set the cache content
        self._cache = content

        # if release is the same, copy over entire cache
        if self.use_cache_release and self.full_cache:
            self._cache['releases'][self.datamodel.release] = self._cache['releases'].get(self.use_cache_release, {})
            return

        # set the cache with access info
        self._update_cache_access()

        # set the cache for hdus
        self._set_cache_hdus(force=force)

        # update the cache changelog
        self._update_cache_changelog()

    def _check_release_in_cache(self, content: dict) -> dict:
        releases = content['general']['releases']
        if self.datamodel.release not in releases:
            releases.append(self.datamodel.release)
            releases.sort()
            content['general']['releases'] = releases
        return content

    def _update_cache_access(self) -> None:
        """ update the cache with access info """
        # always updates the cache with latest datamodel
        # update the access dictionary in the cache
        self._cache['releases'][self.datamodel.release]['access'] = self._get_access_cache()

        # update the template/location keyword in the cache
        self._cache['releases'][self.datamodel.release]['template'] = self.datamodel.template

        # update the location/example keyword in the cache
        self._cache['releases'][self.datamodel.release]['location'] = self.datamodel.location
        self._cache['releases'][self.datamodel.release]['example'] = self.datamodel.real_location

    def _set_cache_hdus(self, force: bool = None) -> None:
        """[summary]

        [extended_summary]

        Parameters
        ----------
        force : bool, optional
            If True, rewrites hdu cache from scratch, by default None
        """
        cached_hdus = self._cache['releases'][self.datamodel.release].get('hdus', {})

        # if no cache exists or forced update, generate a new cache from file
        if not cached_hdus or force:
            cached_hdus = self._generate_new_hdu_cache()

        if self.use_cache_release and not force:
            old_hdus = self._cache['releases'][self.use_cache_release].get('hdus', {})
            if not self.full_cache:
                # partial copy of the cache
                cached_hdus = self._update_partial_cache(cached_hdus, old_hdus)
            else:
                # full copy of the cache
                cached_hdus = old_hdus

        # set the HDU cache to the given release
        self._cache['releases'][self.datamodel.release]['hdus'] = cached_hdus

    @staticmethod
    def _update_partial_cache(cached_hdus, old_hdus):
        old_names = [v['name'] for v in old_hdus.values()]

        for k, v in cached_hdus.items():
            # skip extensions that aren't in the old HDU
            if v['name'] not in old_names:
                continue

            # get the matching old hdu index
            idx = old_names.index(v['name'])
            oldkey = f'hdu{idx}'

            # update the HDU description
            v['description'] = old_hdus[oldkey]['description']

            # skip processing of image extensions
            if v['is_image'] is True:
                continue

            for kk,vv in v['columns'].items():
                vv['unit'] = old_hdus[oldkey]['columns'][kk]['unit']
                vv['description'] = old_hdus[oldkey]['columns'][kk]['description']

        return cached_hdus

    def _generate_new_hdu_cache(self) -> dict:
        """[summary]

        [extended_summary]

        Returns
        -------
        dict
            [description]
        """
        hdus = {}

        with fits.open(self.datamodel.file) as hdulist:
            for hdu_number, hdu in enumerate(hdulist):
                header = hdu.header
                extno = f'hdu{hdu_number}'

                # create a new one
                row = {
                    'name': hdu.name,
                    'description': 'replace me description',
                    'is_image': hdu.is_image,
                    'size': self._format_bytes(hdu.size),
                }

                if hdu.is_image:
                    row['header'] = []
                    for key, value in header.items():
                        if self._is_header_keyword(key=key):
                            column = {"key": key, "value": value, "comment": header.comments[key]}
                            row['header'].append(column)
                else:
                    row['columns'] = {}
                    for column in hdu.columns:
                        row['columns'][column.name] = {
                            'name': column.name.upper(),
                            'type': self._format_type(column.format),
                            'unit': self._nonempty_string(column.unit),
                            'description': self._nonempty_string()
                        }

                hdus[extno] = row
        return hdus

    def _update_cache_changelog(self):
        yaml_diff = YamlDiff(self._cache)
        release_order = reversed(self._cache['general']['releases'])
        changelog = yaml_diff.generate_changelog(release_order, simple=True)
        self._cache['changelog']['releases'] = changelog

    def validate_cache(self):
        if not self._cache:
            log.info("No yaml cache to validate!")
            return False

        # validate the yaml cache
        try:
            YamlModel.parse_obj(self._cache)
        except ValidationError as err:
            log.error(err)
            return False
        else:
            return True

    @staticmethod
    def _format_bytes(value: int = None) -> str:
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

        try:
            value = int(value)
        except:
            value = 0

        for unit in ("bytes", "KB", "MB", "GB"):
            if value < 1024:
                return "{0:d} {1}".format(int(value), unit)
            else:
                value /= 1024.0

        return "{0:3.1f} {1}".format(value, "TB")

    def _get_filesize(self) -> str:
        """Get the size of the input file.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """
        return self._format_bytes(os.path.getsize(self.datamodel.file))

    def _get_filetype(self) -> str:
        """Get the extension of the input file.

        Returns
        -------
        str
            File type in upper case.
        """
        filename, file_extension = os.path.splitext(self.datamodel.file)
        if "gz" in file_extension:
            filename, file_extension = os.path.splitext(filename)
        return file_extension[1:].upper()

    @staticmethod
    def _is_header_keyword(key: str = None) -> bool:
        """Test for hdu header keyword

        Returns
        -------
        bool
            ``True`` if `key` does *not* contain 'TFORM' or 'TTYPE'.
        """
        return tuple(key.find(f) for f in ("TFORM", "TTYPE")) == (-1, -1)

    @staticmethod
    def _nonempty_string(value: str = None) -> str:
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
        return f"{value}" if value else 'replace me - with content'

    @staticmethod
    def _format_type(value: str = None) -> str:
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
        fmap = {"A": "char", "I": "int16", "J": "int32", "K": "int64", "E": "float32",
                "D": "float64", "B": "bool", "L": "bool"}
        out = [
            val if value.isalpha() else "{0}[{1}]".format(val, value[:-1])
            for key, val in fmap.items()
            if key in value
        ]
        return out[0]

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
        hdus = self._cache['releases'][selected_release]['hdus']
        self.content = self.template.render(content=self._cache, hdus=hdus, selected_release=selected_release)

    # def convert_to_html(self):
    #     htmlpath = self.output.replace('md', 'html')
    #     outpath = pathlib.Path(self.output)
    #     if not outpath.exists():
    #         raise ValueError(f'Cannot convert md to html. md file {self.output} does not exist.')

    #     if not markdown:
    #         raise ImportError('Cannot convert md to html.  markdown package is not installed.')

    #     pathlib.Path(htmlpath).parent.mkdir(parents=True, exist_ok=True)
    #     markdown.markdownFromFile(input=self.output, output=htmlpath, extensions=['markdown.extensions.tables', 'toc'])

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
            if group not in key.values():
                raise KeyError(f'group {group} is not a valid release group')
            elif group not in rs.keys():
                raise KeyError(f'group {group} is not yet a cached release')
            return rs[group][-1]

    def render_content(self, force: bool = None, release: str = None, group: str = 'WORK') -> None:
        if not self._cache or force:
            self._get_cache(force=force)

        if self.format != 'yaml' and not self.validate_cache():
            log.info('yaml cache is not validated!')
            return

        self._get_content(release=release, group=group)

    def write(self, force: bool = None, release: str = None, group: str = 'WORK', html: bool = None) -> None:

        if not self.output:
            raise AttributeError('No output filepath set')

        # always re-render the content
        self.render_content(force=force, release=release, group=group)

        if not self.content:
            log.info('No cache content to write out!')
            return

        with open(self.output, 'w') as f:
            f.write(self.content)

        # if html:
        #     self.convert_to_html()


class JsonStub(BaseStub):
    format: str = 'json'
    has_template: bool = False

    def _get_content(self) -> None:
        self.content = json.dumps({}, sort_keys=False, indent=4)


class AccessStub(BaseStub):
    format: str = 'access'
    has_template: bool = False
    cacheable: bool = False

    def _get_content(self) -> None:
        releases = {k: v.get('access', {}) for k,v in self._cache['releases'].items()}
        self.content = yaml.dump(releases, sort_keys=False)

class HtmlStub(MdStub):
    format: str = 'html'



def stub_iterator(format: str = None) -> Iterator[BaseStub]:
    """ Iterator for all stub formats """
    for stub in [YamlStub, AccessStub, MdStub, JsonStub]:
        if format and format != stub.format:
            continue
        yield stub

