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
from pydl.pydlutils.yanny import yanny
import h5py
from sdss_access.path import Path
from tree import Tree

from datamodel.generate import DataModel

####
# Fixtures for setting up the test enviroment and paths

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
    mocker.patch('datamodel.validate.check.Tree', new=MockTree)

####
# Fixtures for creating test files and datamodels

def create_fits(name, version, extra_cols):
    """ create a test fits hdulist """
    # create the FITS HDUList
    header = fits.Header([('filename', name,'name of the file'),
                          ('testver', version, 'version of the file')])
    primary = fits.PrimaryHDU(header=header)
    imdata = fits.ImageHDU(name='FLUX', data=np.ones([5,5]))
    cols = [fits.Column(name='object', format='20A', array=['a', 'b', 'c']),
            fits.Column(name='param', format='E', array=np.random.rand(3), unit='m'),
            fits.Column(name='flag', format='I', array=np.arange(3)),
            fits.Column(name='mixCase', format='E', array=np.random.rand(3)),
            fits.Column(name='UPPER', format='E', array=np.random.rand(3))]
    if extra_cols:
        cols.extend([fits.Column(name='field', format='J', array=np.arange(3)),
                     fits.Column(name='mjd', format='I', array=np.arange(3))])
    thead = fits.Header([('TCOMM2', 'A parameter description', '')])
    bindata = fits.BinTableHDU.from_columns(cols, name='PARAMS', header=thead)

    return fits.HDUList([primary, imdata, bindata])

def create_par():
    """ create a test yanny par """
    par = yanny()
    par._symbols['enum'] = []
    par._symbols['struct'] = ["typedef struct {\n\t\tint a; \n\t\tchar b; \n\t\tfloat[5] c;\n} TABLE;"]
    par._symbols["TABLE"] = ["a", "b", "c"]
    par['ma1'] = 1
    par['ma2'] = 2
    par["TABLE"] = {"a": [1], "b": ['ab'], "c": [[1,2,3,4,5]]}
    return par

def create_hdf5(path):
    """ create a test HDF5 file """
    with h5py.File(path, 'a') as f:
        f.attrs.create('NEW', b'STUFF')
        f.create_group('bar')
        f['bar'].attrs.create('HELLO', b'THERE')
        f.create_dataset('bar/ints', shape=(100,), dtype='int32')
        f.create_dataset('default', shape=(2,10), dtype='<f8')
        return f

def create_test_file(name: str = None, version: str = None,
                     env: str = None, extra_cols: bool = None,
                     id: str = 'a', suffix: str = 'fits') -> pathlib.Path:
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
    suffix : str
        The type of file to create, by default "fits"
    id : str
        The id of the file, by default "a"

    Returns
    -------
    pathlib.Path
        The full path to the temporary file on disk
    """
    # set defaults
    name = name or f'testfile_{id}.{suffix.lower()}'
    version = version or 'v1'
    env = env or 'testwork'

    if suffix == 'fits':
        hdu = create_fits(name, version, extra_cols)
    elif suffix == 'par':
        par = create_par()

    # write out the file to the designated path
    redux = os.getenv("TEST_REDUX", "")
    redux = redux.replace('testwork', env)

    path = pathlib.Path(redux) / version / name
    if not path.exists():
       path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == 'fits':
        hdu.writeto(path, overwrite=True)
    elif suffix == 'par':
        par.write(path, comments=f'# version\n# {version}\n')
    elif suffix == 'h5':
        create_hdf5(path)

    return path


@pytest.fixture()
def makefile():
    """ fixture to make a test file """
    def _make_file(name=None, version=None, env=None, extra_cols=None, id='a', suffix='fits'):
        return create_test_file(name=name, version=version, env=env, extra_cols=extra_cols,
                                id=id, suffix=suffix)
    return _make_file

@pytest.fixture()
def testfile(makefile):
    """ fixture factory to create a new test file for a given file type suffix """
    def _testfile(suffix='fits'):
        return makefile(suffix=suffix)
    return _testfile

@pytest.fixture()
def testfits(testfile):
    """ Fixture to create a default test FITS file """
    yield testfile('fits')


@pytest.fixture
def yamlfile():
    yield os.getenv("DATAMODEL_DIR") / pathlib.Path('datamodel') / 'products/yaml/test.yaml'


@pytest.fixture
def validyaml(yamlfile):
    """ fixture factory that creates a valid test yaml file for a given file type suffix"""
    def _validyaml(suffix='fits'):
        yamlfile.parent.mkdir(parents=True, exist_ok=True)
        testpath = pathlib.Path(__file__).parent / f'data/test_valid_{suffix}.yaml'
        shutil.copy2(testpath, yamlfile)
        return yamlfile
    return _validyaml

@pytest.fixture()
def dmonly(testfile):
    """ fixture factory to create a datamodel (but not write out stubs) for a given file type suffix"""
    def _datamodel(suffix='fits'):
        testfile(suffix=suffix)
        return DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.' + f'{suffix}')
    return _datamodel

@pytest.fixture()
def datamodel(testfile):
    """ fixture factory to create a datamodel for a given file type suffix"""
    def _datamodel(suffix='fits'):
        testfile(suffix=suffix)
        dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.' + f'{suffix}')
        dm.write_stubs()
        return dm
    return _datamodel


@pytest.fixture
def validmodel(validyaml, datamodel):
    """ fixture factory to produce a valid datamodel for a given file type suffix """
    def _validmodel(suffix='fits'):
        validyaml(suffix=suffix)
        return datamodel(suffix=suffix)
    return _validmodel


@pytest.fixture()
def validdesign(yamlfile):
    """ fixture factory for creating a valid datamodel design for a given file type suffix """
    def _validdesign(suffix='fits'):
        dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.' + f'{suffix}', design=True)
        ss = dm.get_stub('yaml')
        ss.update_cache()
        if suffix == 'fits':
            ss._cache['releases']['WORK']['hdus']['hdu0']['description'] = 'primary hdu extension'
        ss.write()
        return dm
    return _validdesign

@pytest.fixture()
def designedfits(validdesign):
    """ Fixture to create a default designed fits file """
    yield validdesign('fits')


#####
# Fixtures for iterating over each file type of the given suffix

# a list of filetypes suffixes to test against
suffixes = ['fits', 'par', 'h5']

@pytest.fixture(params=suffixes)
def suffix(request):
    """ fixture to return a suffix """
    yield request.param

@pytest.fixture
def testfiles(suffix, makefile):
    """ a fixture to iterate over multiple file types, creating a test file """
    testfile = makefile(suffix=suffix)
    yield testfile
    testfile.unlink()

@pytest.fixture
def validyamls(suffix, yamlfile):
    """ a fixture to iterate over multiple file types, creating a valid yaml file """
    yamlfile.parent.mkdir(parents=True, exist_ok=True)
    testpath = pathlib.Path(__file__).parent / f'data/test_valid_{suffix}.yaml'
    shutil.copy2(testpath, yamlfile)
    yield yamlfile

@pytest.fixture()
def datamodels(suffix, testfiles):
    """ a fixture to iterate over multiple file types, creating a datamodel """
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.' + f'{suffix}')
    dm.write_stubs()
    yield dm

@pytest.fixture
def validmodels(validyamls, datamodels):
    """ a fixture to iterate over multiple file types, creating a valididated datamodel """
    yield datamodels

@pytest.fixture()
def validdesigns(suffix, validyamls):
    """ a fixture to iterate over multiple file types, creating datamodel designs """
    dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.' + f'{suffix}', design=True)
    ss = dm.get_stub('yaml')
    ss.update_cache()
    if suffix == 'fits':
        ss._cache['releases']['WORK']['hdus']['hdu0']['description'] = 'primary hdu extension'
    ss.write()
    yield dm

#####
# Mocks for Tree and sdss_access Path classes to add in TEST_REDUX and test file paths
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

class MockTreeEnv(Tree):
    """ mock out the Tree class to only TEST_REDUX enviroment """

    def _create_environment(self, cfg=None, sections=None):
        environ = super(MockTreeEnv, self)._create_environment(cfg=cfg, sections=sections)
        env = 'testwork' if self.config_name in ['sdsswork', 'sdss5'] else self.config_name.lower()
        path = os.getenv("TEST_REDUX").replace('testwork', env)
        environ['general'].update({'TEST_REDUX': path})
        return environ

class MockPath(Path):
    """ mock out the Path class to insert test file """

    def __init__(self, *args, **kwargs):
        super(MockPath, self).__init__(*args, **kwargs)
        self.templates.update({'test': '$TEST_REDUX/{ver}/testfile_{id}.fits'})
        self.templates.update({'test-file': '$TEST_REDUX/{ver}/testfile_{id}.fits'})
