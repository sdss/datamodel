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
from datamodel.models.versions import Tags
from datamodel.models.vacs import VACS


@pytest.fixture()
def defaultmodel(validmodel):
    """ fixture to create a default valid FITS datamodel """
    yield validmodel('fits')

# use the default validmodel fixture in all tests
pytestmark = pytest.mark.usefixtures("defaultmodel")


@pytest.fixture()
def product():
    """ fixture to create a new test Product """
    p = Product('test', load=True)
    yield p


def test_product():
    """ test the creation of a new Product """
    p = Product('test')
    assert p.name == 'test'
    assert "datamodel/products/json/test.json" in str(p.path)
    assert p.path.exists()


def test_load_product():
    """ test we can load a product """
    p = Product('test')
    assert p.loaded is False
    assert not hasattr(p, 'releases')

    p.load()
    assert p.loaded is True
    assert 'WORK' in p.releases
    assert p.short == 'this is a test file'
    assert str(p.data_level) == "1.2.3"


def test_load_from_file():
    """ test we can load a product from a valid JSON file """
    path = pathlib.Path(os.getenv("DATAMODEL_DIR")) / 'datamodel' / 'products' / 'json' / 'test.json'
    p = Product.from_file(path, load=True)

    assert p.name == 'test'
    assert p.loaded is True
    assert p.short == 'this is a test file'
    assert str(p.data_level) == "1.2.3"

def test_load_context():
    """ test contextmanager product loader """
    p = Product('test')
    assert p.loaded is False
    with p.loader() as pp:
        assert pp.loaded is True
    assert p.loaded is False


def test_get_release(product):
    """ test we can get a release from a product """
    release = product.get_release("WORK")
    assert release.template == '$TEST_REDUX/[VER]/testfile_[ID].fits'
    assert release.location == r'{ver}/testfile_{id}.fits'
    assert len(release.hdus) == 3


def test_get_release_fail(product):
    """ test if fails for invalid releases """
    with pytest.raises(ValueError, match='release BAD is not a valid SDSS release'):
        product.get_release('BAD')


def test_get_content(product):
    """ test we can get the model content of a product """
    content = product.get_content()
    assert type(content) == dict
    assert 'general' in content
    assert 'changelog' in content
    assert content['general']['description'] == 'this test file is used for testing'

@pytest.mark.parametrize('expand, exp',
                         [(True, 'v1/testfile_a.fits'),
                          (False, '$TEST_REDUX/v1/testfile_a.fits')],
                         ids=['expand', 'noexpand'])
def test_get_example(product, expand, exp):
    """ test we can get an example file from the product model data """
    path = product.get_example(expand=expand)
    assert exp in path

@pytest.mark.parametrize('symbolic, exp',
                         [(True, '$TEST_REDUX/{ver}/testfile_{id}.fits'),
                          (False, 'v2/testfile_b.fits')],
                         ids=['symbolic', 'nosymbolic'])
def test_get_location(product, symbolic, exp):
    """ test we can get the location of a product """
    path = product.get_location(symbolic=symbolic, ver='v2', id='b')
    assert exp in path

def test_get_acces(product):
    """ test we can get the product acces info"""
    # naming this test acces so the stub does not replace test name during "access"->"yaml" cache file check
    data = product.get_access("WORK")
    assert data['in_sdss_access'] is True
    assert data['path_name'] == 'test'
    assert data['path_template'] == '$TEST_REDUX/{ver}/testfile_{id}.fits'
    assert data['access_string'] == 'test = $TEST_REDUX/{ver}/testfile_{id}.fits'

def test_data_products():
    """ test all data products """
    dp = DataProducts()
    assert len(dp) == 1
    assert isinstance(dp['test'], Product)
    assert dp['test'].name == 'test'


def test_products_auto_load():
    """ test load all data products """
    dp = DataProducts()
    loaded = [i.loaded for i in dp]
    assert loaded == [False]
    assert dp['test'].loaded is True


def test_list_products():
    """ test list all products """
    dp = DataProducts()
    assert dp.list_products() == ['test']


@pytest.mark.parametrize('field, key',
                         [('releases', 'WORK'),
                          ('_model.general.environments', 'TEST_REDUX'),
                          ('data_level', '1.2.3')],
                         ids=['release', 'environment', 'data_level'])
def test_products_groupby(field, key):
    """ test we can group products by a field """
    dp = DataProducts()
    grp = dp.group_by(field)
    assert key in grp
    assert isinstance(grp[key][0], Product)
    assert grp[key][0].name == 'test'


def test_products_getlevel():
    """ test we can get the data level of a product """
    dp = DataProducts()
    exp = {'1.2.3': [dp['test']]}
    assert dp.get_level('1') == exp
    assert dp.get_level(1) == exp
    assert dp.get_level(2) == {}
    assert dp.get_level('1.2') == exp
    assert dp.get_level('1.3') == {}
    assert dp.get_level('1.2.3') == exp
    assert dp.get_level('1.2.4') == {}


def test_sdss_datamodel():
    """ test the general SDSS datamodel object"""
    dm = SDSSDataModel()
    assert dm.products is not None
    assert len(dm.products) == 1
    assert dm.products[0].name == 'test'

    assert isinstance(dm.releases, Releases)
    assert isinstance(dm.surveys, Surveys)
    assert isinstance(dm.phases, Phases)
    assert isinstance(dm.tags, Tags)
    assert isinstance(dm.vacs, VACS)

    assert 'WORK' in dm.releases
    assert 'MaNGA' in dm.surveys
    assert 'Phase-II' in dm.phases


def test_product_mixcase(product):
    """ test the product retains the original case of the table column name """
    cols = product.get_release('WORK').hdus['hdu2'].columns
    assert 'param' in cols
    assert 'PARAM' not in cols
    assert 'UPPER' in cols
    assert 'mixCase' in cols
    assert 'MIXCASE' not in cols
    assert 'mixcase' not in cols
    assert cols['mixCase'].name == 'mixCase'
    assert cols['param'].name == 'param'
    assert cols['UPPER'].name == 'UPPER'
