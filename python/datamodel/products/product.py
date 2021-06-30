# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: product.py
# Project: products
# Author: Brian Cherinka
# Created: Friday, 25th June 2021 11:14:00 am
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Friday, 25th June 2021 11:14:00 am
# Modified By: Brian Cherinka

import functools
import itertools
import os
import pathlib
from typing import Type, TypeVar, Union

from fuzzy_types import FuzzyList

from datamodel import log
from datamodel.models import phases, releases, surveys
from datamodel.models.yaml import ProductModel, Release


# pylint: disable=maybe-no-member

products_path = pathlib.Path(os.getenv("DATAMODEL_DIR")) / 'datamodel' / 'products' / 'json'

PType = TypeVar('PType', bound='Product')

class Product(object):
    """ Class for an SDSS data product

    Entry point for individual SDSS data products.  This class reads in the content
    from the validated JSON datamodel file, handling deserialization via the pydantic
    `~datamodel.models.yaml.ProductModel`.  By default, products are lazy-loaded, i.e.
    they will not load the underlying JSON content.  Pass ``load=True`` or use ``load()``
    to manually load the product's datamodel.
    
    Parameters
    ----------
    name : str
        The file species name of the datamodel 
    load : bool, optional
        If True, loads the model's JSON content, by default False
    """
    # contains JSON content fields to extract from the model into the main instance
    _extract = ['short', 'description']
    
    def __init__(self, name: str, load: bool = False):
        self.name = name
        self.path = products_path / f"{name}.json"
        self.loaded = False
        
        if load:
            self._load_product_from_model()

    def __repr__(self) -> str:
        short = hasattr(self, 'short')
        return f'<Product ("{self.name}", summary="{self.short if short else ""}")>'
    
    def load(self) -> None:
        """ Loads the DataModel content into the Product """
        if self.loaded:
            return 
        self._load_product_from_model()

    def _load_product_from_model(self) -> None:
        """ Loads the Datamodel content into the Product
        
        Loads the Pydantic Model content from the JSON file into a hidden
        ``_model`` attribute.  Extracts the product's available releases and
        sets to a new attribute.  Also extracts any general fields included in the 
        ``_extract`` list of attributes. 
        """
        self._model = ProductModel.parse_file(self.path)
        self.releases = self._model.general.releases        
        for field in self._extract:
            setattr(self, field, getattr(self._model.general, field))
        self.loaded = True

    def get_release(self, value: str) -> Release:
        """ Get the JSON content for the given product for a given SDSS release

        Returns the Pydantic yaml.Release model for a given SDSS release.  All JSON keys
        are accessible as instance attributes.  The model can be dumped into a dictionary 
        with the ``dict()`` method.    

        Parameters
        ----------
        value : str
            a valid SDSS release

        Returns
        -------
        Release
            The JSON ReleaseModel content for the given SDSS release

        Raises
        ------
        ValueError
            when the input release is an invalid SDSS release
        """
        if value not in self.releases:
            raise ValueError(f"release {value} is not a valid SDSS release")
        
        return self._model.releases[value]
    
    def get_content(self) -> dict:
        """ Returns the entire cached JSON datamodel content

        Returns
        -------
        dict
            The JSON datamodel content
        """
        return self._model.dict()
    
    @classmethod
    def from_file(cls: Type[PType], value: Union[str, pathlib.Path], load: bool = None) -> PType:
        """ Class method to load a data Product from a JSON datamodel filepath

        Parameters
        ----------
        value : Union[str, pathlib.Path]
            The full path to a JSON datamodel file
        load : bool, optional
            If True, loads the model content on instantiation, by default None

        Returns
        -------
        PType
            A new instance of a Product
        """
        path = pathlib.Path(value)
        return cls(name=path.stem, load=load)

class DataProducts(FuzzyList):
    """ Class of a fuzzy list of SDSS data products

    Creates a list of all available SDSS data products that have valid JSON datamodel 
    files, i.e. those in the ``datamodel/products/json/`` directory.  All products are 
    lazy-loaded at first for efficiency.  Products are automatically loaded with content when 
    the items in the list are accessed. 
    """
    def __init__(self):
        super(DataProducts, self).__init__([Product.from_file(i, load=False) for i in products_path.rglob('*.json')], dottable=False)

    def __repr__(self):
        return f'<DataProducts (n_products={len(self)})>'
    
    @staticmethod
    def mapper(item) -> str:
        """ Override the fuzzy mapper to match on product's name """
        return str(item.name)

    def __getitem__(self, item: Union[int, str]) -> PType:
        """ Override fuzzy getter to also load the product on access """
        val = super(DataProducts, self).__getitem__(item)
        val.load()
        return val
    
    def list_products(self) -> list:
        """ List all data products """
        return [item.name for item in self]
    
    def load_all(self):
        """ Load all data products """
        for item in self:
            item.load()
            
    def group_by(self, field: str) -> dict:
        """ Group the products by an attribute 
        
        Group all products by either a product attribute, e.g. "releases", 
        or a field in the underlying JSON model, e.g. "_model.general.environments".
        A dotted attribute string is resolved as a set of nested attribute. Returns 
        a dictionary of products grouped by the field, or fields, if the requested 
        field is a list.

        Parameters
        ----------
        field : str
            The name of the attribute or field

        Returns
        -------
        dict
            A dictionary of products grouped by desired field
            
        Example
        -------
        >>> from datamodel.products import DataProducts
        >>> dp = DataProducts()
        >>> gg = dp.group_by('releases')
        >>> gg
            {"DR15": ..., 
             "DR16": ....}
        """
        return grouper(field, self)

class DataModel(object):
    """ Class for the SDSS DataModel

    High-level entry point into the SDSS DataModel.  Contains accounting of
    all relevant SDSS phases, surveys, data releases, and available data products.
    """
    def __init__(self):
        self.releases = releases
        self.surveys = surveys
        self.phases = phases
        self.products = DataProducts()
    
    def __repr__(self) -> str:
        return (f'<SDSS DataModel (n_releases={len(self.releases)}, '
                f'n_products={len(self.products)}, n_surveys={len(self.surveys)}, '
                f'n_phases={len(self.phases)})>')


def rgetattr(obj: object, attr: str, *args):
    """ recursive getattr for nested attributes
    
    Recursively get attributes from nested classes.  See
    https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def grouper(field: str, products: list) -> dict:
    """ Group the products by an attribute 

    Group all products by either a product attribute, e.g. "releases", 
    or a field in the underlying JSON model, e.g. "_model.general.environments".
    A dotted attribute string is resolved as a set of nested attribute. Returns 
    a dictionary of products grouped by the field, or fields, if the requested 
    field is a list.

    Parameters
    ----------
    field : str
        The name of the attribute or field
    products : list
        A list of Products to group by

    Returns
    -------
    dict
        A dictionary of products grouped by desired field
    
    """
    # check if the products are loaded
    if not all(i.loaded for i in products):
        log.warning('Input list of products are not loaded.  Loading all!')
        products.load_all()

    # check if the field is a list    
    value = rgetattr(products[0], field)
    if type(value) != list:
        zipper = lambda x: list(zip(itertools.repeat(x), [rgetattr(x, field)]))
    else:
        zipper = lambda x: list(zip(itertools.repeat(x), rgetattr(x, field)))

    # create a master zipped list of [(product, field)] to easily sort by
    e = list(map(zipper, products))
    r = sum(e, [])

    # sort the data ahead of groupby, using the field as key
    data = sorted(r, key=lambda x:x[1])

    # group items by field, drop into dict, and return
    gg = itertools.groupby(data, key=lambda x: x[1])

    groups = {}
    for i, g in gg:
        prods, ff = zip(*g)  # pylint: disable=unused-variable
        groups[i] = list(prods)
    return groups
