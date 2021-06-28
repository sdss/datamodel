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

from datamodel.models import releases, surveys, phases
from datamodel.models.yaml import ProductModel, Release
import os
import pathlib
from typing import Union, TypeVar, Type

# pylint: disable=maybe-no-member

products_path = pathlib.Path(os.getenv("DATAMODEL_DIR")) / 'datamodel' / 'products' / 'json'

PType = TypeVar('PType', bound='Product')

class Product(object):
    """[summary]

    [extended_summary]

    Parameters
    ----------
    name : str
        [description]
    load : bool, optional
        [description], by default False
    """
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

class DataProducts(list):
    """ Class of a list of SDSS data products

    Creates a list of all available SDSS data products that have valid JSON datamodel 
    files, i.e. those in the ``datamodel/products/json/`` directory.  All products are 
    lazy-loaded at first for efficiency.  Products are automatically loaded with content when 
    the items in the list are accessed. 
    """
    def __init__(self):
        list.__init__(self, [Product.from_file(i, load=False) for i in products_path.rglob('*.json')])
        
    def __repr__(self):
        return f'<DataProducts (n_products={len(self)})>'

    def __getitem__(self, item):
        if isinstance(item, str) and item in self:
            vals = [i.name for i in self]
            obj =  list.__getitem__(self, vals.index(item))
            obj.load()
            return obj
        obj = list.__getitem__(self, item)
        obj.load()
        return obj

    def __contains__(self, value):
        if isinstance(value, str):
            return value in [i.name for i in self]
        return value in self

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
    
    def __repr__(self):
        return (f'<SDSS DataModel (n_releases={len(self.releases)}, '
                f'n_products={len(self.products)}, n_surveys={len(self.surveys)}, '
                f'n_phases={len(self.phases)})>')
    
    
        