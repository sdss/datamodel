# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: page.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

import os
from typing import Type

from jinja2 import Environment, PackageLoader

from datamodel import log

from ..generate import DataModel
from .remote import Remote


__author__ = "Joel Brownstein <joelbrownstein@sdss.org>"


class Page(object):
    """ Class to store and update wiki pages

    Class to create confluence wiki pages for a given datamodel

    Parameters
    ----------
    datamodel : `.DataModel`, optional
        A datamodel to generate a wiki page for, by default None
    space_ver : str, optional
        Set the version of the datamodel space on the wiki, by default "sdsswork"
    verbose : bool, optional
        If True, turn on verbose logging, by default None
    """

    def __init__(self, datamodel : Type[DataModel] = None, space_ver: str = 'sdsswork', verbose: bool = None,
                 file_species: str = None, env_label: str = None):
        self.space_ver = space_ver
        self.verbose = verbose
        self.datamodel = datamodel
        self.file_species = file_species
        self.env_label = env_label

        if not self.datamodel and not (self.file_species and self.env_label):
            raise ValueError("Must specify either a datamodel or a file_species + env_label!")

        # set the datamodel
        if self.datamodel:
            self.file_species = self.datamodel.file_species
            self.env_label = self.datamodel.env_label

        self.set_data()
        self.set_environment()

    def __repr__(self) -> str:
        if self.file_species:
            return (f'<Page(space="{self.space_ver}", file_species="{self.file_species}", '
                    f'env_label="{self.env_label}")>')
        else:
            return f'<Page(space="{self.space_ver}")>'

    @classmethod
    def from_datamodel(cls, datamodel: Type[DataModel]):
        """ Instantiate a Page object using a datamodel instance """
        return cls(datamodel=datamodel)

    def set_remote(self):
        """ Set the remote command-line connection """
        self.remote = Remote(verbose=self.verbose)
        self.remote.set_login()

    def set_remote_pagelist(self, root: bool = None, parent: bool = None):
        """ Set the remote list of wiki page content """
        self.remote.set_pagelist(parent=self.get_title(root=root, parent=parent))

    def get_title(self, root: bool = None, parent: bool = None) -> str:
        """ Get a title of the wiki page

        Parameters
        ----------
        root : bool, optional
            If True, sets root title to "Datamodel", by default None
        parent : bool, optional
            If True, sets parent title to the environment label, by default None

        Returns
        -------
        str
            the title of the wiki page
        """

        if root:
            title = 'Datamodel'
        elif parent:
            title = self.env_label
        else:
            title = self.file_species

        return title

    def set_data(self):
        """ Sets the relative output paths for the md and access files """
        data = {}

        data['access'] = os.path.join('datamodel', 'products/access', self.env_label, f'{self.file_species}.access')
        data['md'] = os.path.join('datamodel', 'products/md', self.env_label, f'{self.file_species}.md')

        self.data = data

    def get_content(self, parent: bool = None) -> str:
        """ Render the content into the Jinja template

        Parameters
        ----------
        parent : bool, optional
            If True, uses the parent wiki template, by default None

        Returns
        -------
        str
            the template-rendered html content
        """
        self.set_template(parent=parent)
        data = None if parent else self.data
        return self.template.render(data=data) if self.template else None

    def create_parent(self):
        """ Create a parent wiki page based on environment label """
        if self.remote.pagelist:
            if self.verbose:
                log.info(f"PAGE> found {self.env_label} page (version={self.space_ver})")
        else:
            self.set_remote_pagelist(root=True)
            try:
                parent = self.remote.pagelist["parent"]
            except:
                parent = None
            title = self.get_title(parent=True)
            content = self.get_content(parent=True)
            self.create_page(parent=parent, title=title, content=content)

    def create_datamodel(self):
        """ Create a datamodel page """

        if not self.remote.pagelist:
            log.error(f"PAGE> error creating {self.file_species} page without "
                      f"finding parent {self.env_label} page (version={self.space_ver}).")
            return

        title = self.get_title()
        pages = self.remote.pagelist["data"]
        pages = [page for page in pages if page["title"] == title]
        page = pages[0] if len(pages) == 1 else None
        if page:
            if self.verbose:
                log.info(f"PAGE> found {self.file_species} page (version={self.space_ver})")
        else:
            parent = self.get_title(parent=True)
            content = self.get_content()
            self.create_page(parent=parent, title=title, content=content)


    def create_page(self, parent: bool = None, title: str = None, content: str = None, convert: bool = None):
        """ Create a wiki page

        Parameters
        ----------
        parent : bool, optional
            if True, creates a parent page, by default None
        title : str, optional
            the title of the page, by default None
        content : str, optional
            the content to render to the page, by default None
        convert : bool, optional
            if True performs some conversion?, by default None
        """
        if title and content:
            self.remote.add_page(parent=parent, title=title, content=content, convert=convert)

    def set_environment(self):
        """ Set the jina2 environment including filters for content. """
        loader = PackageLoader("datamodel", "templates")
        self.environment = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    def set_template(self, parent: bool = None):
        """ Create the Jinja2 environment and set the template. """

        pagetype = "parent" if parent else "page"
        html = f"wiki-{pagetype}.html"
        self.template = self.environment.get_template(html) if self.environment else None
