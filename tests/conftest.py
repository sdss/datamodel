# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: conftest.py
# Project: tests
# Author: Brian Cherinka
# Created: Tuesday, 20th April 2021 5:42:59 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Tuesday, 20th April 2021 5:42:59 pm
# Modified By: Brian Cherinka


from __future__ import absolute_import, division, print_function

import os
import pathlib
import shutil

import numpy as np
import pytest
from astropy.io import fits
from sdss_access.path import Path
from tree import Tree


@pytest.fixture(autouse=True)
def setup_datamodel_env(monkeypatch, tmp_path):
    """ fixtures that sets up temp datamodel directory """
    dm_dir = tmp_path / 'base'
    data_dir = dm_dir / 'datamodel'
    products_dir = data_dir / 'products'
    products_dir.mkdir(parents=True)

    monkeypatch.setenv("DATAMODEL_DIR", dm_dir)
    inp = pathlib.Path(__file__).parent.parent / 'datamodel/releases.yaml'
    shutil.copy2(inp, f'{data_dir}/releases.yaml')


@pytest.fixture(autouse=True)
def setup_sas(monkeypatch, tmp_path, mocker):
    """ fixtures that sets up temp SAS and a TEST_REDUX directory """
    sas_dir = tmp_path / 'sas'
    test_dir = sas_dir / 'testwork' / 'test/spectro/redux'
    test_dir.mkdir(parents=True)
    monkeypatch.setenv("SAS_BASE_DIR", sas_dir)
    monkeypatch.setenv("TEST_REDUX", test_dir)

    mocker.patch('datamodel.generate.datamodel.Tree', new=MockTree)
    mocker.patch('datamodel.generate.datamodel.Path', new=MockPath)


def create_test_fits(name: str = None, version: str = None, 
                     env: str = None, extra_cols: bool = None) -> pathlib.Path:
    """ creates a temporary fake test file

    Parameters
    ----------
    name : str, optional
        the name of the file, by default 'testfile_a.fits'
    version : str, optional
        the version of the file, by default 'v1'
    env : str, optional
        the environment, by default 'testwork'
    extra_cols : bool, optional
        If True, add extra columns to the binary table FITS extension, by default False

    Returns
    -------
    pathlib.Path
        The full path to the temporary file on disk
    """
    # set defaults
    name = name or 'testfile_a.fits'
    version = version or 'v1'
    env = env or 'testwork'

    # create the FITS HDUList
    header = fits.Header([('filename','testfile.fits','name of the file'),
                          ('testver', version, 'version of the file')])
    primary = fits.PrimaryHDU(header=header)
    imdata = fits.ImageHDU(name='FLUX', data=np.ones([5,5]))
    cols = [fits.Column(name='object', format='20A', array=['a', 'b', 'c']),
            fits.Column(name='param', format='E', array=np.random.rand(3), unit='m'),
            fits.Column(name='flag', format='I', array=np.arange(3))]
    if extra_cols:
        cols.extend([fits.Column(name='field', format='J', array=np.arange(3)),
                     fits.Column(name='mjd', format='I', array=np.arange(3))])
    bindata = fits.BinTableHDU.from_columns(cols)

    hdu = fits.HDUList([primary, imdata, bindata])

    # write out the file to the designated path
    redux = os.getenv("TEST_REDUX", "")
    redux = redux.replace('testwork', env)

    path = pathlib.Path(redux) / version / name
    if not path.exists():
       path.parent.mkdir(parents=True, exist_ok=True)

    hdu.writeto(path, overwrite=True)

    return path


@pytest.fixture()
def makefile():
    """ fixture to make a test file """
    def _make_file(name=None, version=None, env=None, extra_cols=None):
        return create_test_fits(name=name, version=version, env=env, extra_cols=extra_cols)
    return _make_file


@pytest.fixture()
def testfile(makefile):
    """ fixture to create a default test file """
    testfile = makefile()
    yield testfile
    testfile.unlink()


@pytest.fixture
def yamlfile():
    yield os.getenv("DATAMODEL_DIR") / pathlib.Path('datamodel') / 'products/yaml/test.yaml'

@pytest.fixture
def validyaml(yamlfile):
    """ fixture that makes the test yaml file a valid one """
    yamlfile.parent.mkdir(parents=True, exist_ok=True)
    testpath = pathlib.Path(__file__).parent / 'data/test_valid.yaml'
    shutil.copy2(testpath, yamlfile)
    yield yamlfile


from datamodel.generate import DataModel

@pytest.fixture()
def datamodel(testfile):
    """ fixture to create a default datamodel """
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits')
    dm.write_stubs()
    yield dm


@pytest.fixture
def validmodel(validyaml, datamodel):
    """ fixture to produce a valud datamodel for the test file """
    yield datamodel


@pytest.fixture()
def validdesign(yamlfile):
    """ fixture for creating a valid datamodel design """
    dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits', design=True)
    ss = dm.get_stub('yaml')
    ss.update_cache()
    ss._cache['releases']['WORK']['hdus']['hdu0']['description'] = 'primary hdu extension'
    ss.write()
    yield dm

class MockTree(Tree):
    """ mock out the Tree class to insert test file """

    def _create_environment(self, cfg=None, sections=None):
        environ = super(MockTree, self)._create_environment(cfg=cfg, sections=sections)
        env = 'testwork' if self.config_name in ['sdsswork', 'sdss5'] else self.config_name.lower()
        path = os.getenv("TEST_REDUX").replace('testwork', env)
        environ['general'].update({'TEST_REDUX': path})
        return environ

    def _create_paths(self, cfg=None):
        paths = super(MockTree, self)._create_paths(cfg=cfg)
        paths.update({'test': '$TEST_REDUX/{ver}/testfile_{id}.fits'})
        paths.update({'test-file': '$TEST_REDUX/{ver}/testfile_{id}.fits'})
        return paths

class MockPath(Path):
    """ mock out the Path class to insert test file """

    def __init__(self, *args, **kwargs):
        super(MockPath, self).__init__(*args, **kwargs)
        self.templates.update({'test': '$TEST_REDUX/{ver}/testfile_{id}.fits'})
        self.templates.update({'test-file': '$TEST_REDUX/{ver}/testfile_{id}.fits'})
