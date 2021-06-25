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
from datamodel.models.yaml import ProductModel
import os
import pathlib
from typing import Union

# pylint: disable=maybe-no-member

products_path = pathlib.Path(os.getenv("DATAMODEL_DIR")) / 'datamodel' / 'products' / 'json'

class Product(object):
    _extract = ['short', 'description']
    
    def __init__(self, name: str, load: bool = False):

        self.name = name
        self.path = products_path / f"{name}.json"
        self.loaded = False
        
        if load:
            self._load_product_from_model()

    def __repr__(self):
        short = hasattr(self, 'short')
        return f'<Product ("{self.name}", summary="{self.short if short else ""}")>'
    
    def load(self):
        if self.loaded:
            return 
        self._load_product_from_model()

    def _load_product_from_model(self):
        self._model = ProductModel.parse_file(self.path)
        self.releases = self._model.general.releases        
        for field in self._extract:
            setattr(self, field, getattr(self._model.general, field))
        self.loaded = True

    def get_release(self, value: str):

        if value not in self.releases:
            raise ValueError(f"release {value} is not a valid SDSS release")
        
        return self._model.releases[value]
    
    def get_content(self) -> dict:
        return self._model.dict()
    
    @classmethod
    def from_file(cls, value: Union[str, pathlib.Path], load: bool = None):
        path = pathlib.Path(value)
        return cls(name=path.stem, load=load)
    
    
class DataProducts(list):
    
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
    def __init__(self):
        self.releases = releases
        self.surveys = surveys
        self.phases = phases
        self.products = DataProducts()
    
    def __repr__(self):
        return '<SDSS DataModel ()>'
    
    
        