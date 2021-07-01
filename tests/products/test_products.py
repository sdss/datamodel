# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: test_products.py
# Project: products
# Author: Brian Cherinka
# Created: Wednesday, 30th June, 2021 4:31 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Wednesday, 30th June, 2021 4:31 pm
# Modified By: Brian Cherinka

import os
import pathlib
import pytest

from datamodel.products import Product, DataProducts, SDSSDataModel
from datamodel.models.releases import Releases
from datamodel.models.surveys import Phases, Surveys

# use the validmodel fixture in all tests
pytestmark = pytest.mark.usefixtures("validmodel")


@pytest.fixture()
def product():
    p = Product('test', load=True)
    yield p


def test_product():
    p = Product('test')
    assert p.name == 'test'
    assert "datamodel/products/json/test.json" in str(p.path)
    assert p.path.exists()


def test_load_product():
    p = Product('test')
    assert p.loaded is False
    assert not hasattr(p, 'releases')
    
    p.load()
    assert p.loaded is True
    assert p.releases == ['WORK']
    assert p.short == 'this is a test file'

    
def test_load_from_file():
    path = pathlib.Path(os.getenv("DATAMODEL_DIR")) / 'datamodel' / 'products' / 'json' / 'test.json'
    p = Product.from_file(path, load=True)

    assert p.name == 'test'
    assert p.loaded is True
    assert p.short == 'this is a test file'


def test_get_release(product):
    release = product.get_release("WORK")
    assert release.template == '$TEST_REDUX/[VER]/testfile_[ID].fits'
    assert release.location == r'{ver}/testfile_{id}.fits'
    assert len(release.hdus) == 3


def test_get_release_fail(product):
    with pytest.raises(ValueError, match='release BAD is not a valid SDSS release'):
        product.get_release('BAD')


def test_get_content(product):
    content = product.get_content()
    assert type(content) == dict
    assert 'general' in content
    assert 'changelog' in content
    assert content['general']['description'] == 'this test file is used for testing'        


def test_data_products():
    dp = DataProducts()
    assert len(dp) == 1
    assert isinstance(dp['test'], Product)
    assert dp['test'].name == 'test'


def test_products_auto_load():
    dp = DataProducts()
    loaded = [i.loaded for i in dp]
    assert loaded == [False]
    assert dp['test'].loaded is True


def test_list_products():
    dp = DataProducts()
    assert dp.list_products() == ['test']

    
@pytest.mark.parametrize('field, key', 
                         [('releases', 'WORK')], 
                         ids=['release'])
def test_products_groupby(field, key):
    dp = DataProducts()
    grp = dp.group_by(field)
    assert key in grp
    assert isinstance(grp[key][0], Product)
    assert grp[key][0].name == 'test'


def test_sdss_datamodel():
    dm = SDSSDataModel()
    assert dm.products is not None
    assert len(dm.products) == 1
    assert dm.products[0].name == 'test'
    
    assert isinstance(dm.releases, Releases)
    assert isinstance(dm.surveys, Surveys)
    assert isinstance(dm.phases, Phases)
    
    assert 'WORK' in dm.releases
    assert 'MaNGA' in dm.surveys
    assert 'Phase-II' in dm.phases