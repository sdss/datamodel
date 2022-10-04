# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: test_datamodel.py
# Project: generate
# Author: Brian Cherinka
# Created: Saturday, 1st May 2021 6:37:03 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Saturday, 1st May 2021 6:37:03 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

import pytest
import os
import re

import deepdiff
from datamodel.generate import DataModel
from datamodel.generate.filetypes import ParFile, FitsFile, HdfFile


suffix_map = {'fits': FitsFile, 'par': ParFile, 'h5': HdfFile}


def test_default_create_file(testfile):
    """ test we can create a test file """
    assert testfile().exists()

@pytest.mark.parametrize('ver, env', [('v1', 'dr15'), ('v2', 'dr16')])
def test_create_file(makefile, ver, env):
    """ test we can make different versions of a file """
    testfile = makefile(version=ver, env=env)
    assert testfile.exists()
    assert ver in str(testfile)
    assert env in str(testfile)
    assert 'testfile_a.fits' in str(testfile)


def test_datamodel_generate(testfiles, suffix):
    """ test we can run datamodel generate for different file types """

    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.' + f'{suffix}')
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    assert dm.survey == 'SDSS'
    assert os.path.exists(ss.output)
    assert ss.validate_cache() is False


def test_diff_file_species_path_name(testfits):
    """ test datamodel generate works when the file species and path template name are different """

    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'],
                   path='TEST_REDUX/{ver}/testfile_{id}.fits', access_path_name="test-file")
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    ss.update_cache()
    assert dm.file_species == 'test'
    assert dm._access_path_name == 'test-file'
    assert ss._cache['releases']['WORK']['access']['path_name'] == dm._access_path_name

def test_datamodel_nokeys_ok():
    """ test we can generate a datamodel without path keyword args """
    path = 'BOSS_PHOTOBJ/astromqa/astromQAFields.fits'
    dm = DataModel(file_spec='astromQAFields', path=path, release="DR10")
    assert isinstance(dm, DataModel)
    assert dm.location == 'astromqa/astromQAFields.fits'

def test_datamodel_nokeys(testfits):
    """ test if fails as expected when keys are expected but not provided """
    with pytest.raises(ValueError, match='A set of keywords must be provided along with a either a path or location'):
        DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits')

def test_datamodel_tcomm(testfits):
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'],
                   path='TEST_REDUX/{ver}/testfile_{id}.fits', access_path_name="test-file")
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    ss.update_cache()
    cols = ss._cache['releases']['WORK']['hdus']['hdu2']['columns']
    assert cols['object']['description'] == 'replace me - with content'
    assert cols['param']['description'] == 'A parameter description'

def test_datamodel_duplicate_keys():
    """ test that datamodel generate correctly handles duplicate keys """
    path = 'ROBOSTRATEGY_DATA/allocations/{plan}/rsCompleteness-{plan}-{observatory}.fits'
    keys = ['plan=alpha-3', 'observatory=apo']
    dm = DataModel(file_spec='rsCompleteness', path=path, tree_ver='sdss5', keywords=keys)
    assert sorted(dm.access['WORK']['path_kwargs']) == sorted(['plan', 'observatory'])
    real_keys = re.findall(r'{(.*?)}', dm.path)
    assert real_keys == ['plan', 'plan', 'observatory']

def test_datamodel_from_yaml(validmodel):
    validmodel('fits')
    dm = DataModel.from_yaml('test', release='WORK')
    assert isinstance(dm, DataModel)

def test_dm_survey(validyaml, dmonly):
    validyaml('noaccess')
    dm = dmonly(suffix='fits')
    assert dm.survey == 'SDSS'
    ss = dm.get_stub()
    data = ss._read_cache(ss.output)
    assert 'surveys' not in data['general']

    ss.update_cache()
    assert 'surveys' in ss._cache['general']
    dm.write_stubs()
    data = ss._read_cache(ss.output)
    assert 'surveys' in data['general']

def test_valid_datamodel(validmodels, suffix):
    """ test we can produce valid datamodels for different file types """
    ss = validmodels.get_stub('yaml')
    validmodels.write_stubs()
    ss.update_cache()
    # assert valid yaml content
    assert os.path.exists(ss.output)
    assert ss.validate_cache() is True
    assert isinstance(ss.selected_file, suffix_map[suffix])
    assert ss._cache["general"]["datatype"] == suffix.upper()

    # assert other stubs exist
    for stub in ['md', 'json', 'access']:
        ss = validmodels.get_stub(stub)
        assert os.path.exists(ss.output)

def test_release_same_cache(makefile, validyaml):
    """ test that the full cache works for new releases """
    validyaml('fits')
    dr15 = makefile(env='dr15')
    dr16 = makefile(env='dr16')

    # dr15 - copy valid cache from WORK
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits', verbose=True, release='DR15')
    dm.write_stubs(use_cache_release='WORK', full_cache=True)

    # dr16
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits', verbose=True, release='DR16')
    dm.write_stubs(use_cache_release='DR15', full_cache=True)

    ss = dm.get_stub('yaml')
    ss.update_cache()
    assert set(ss._cache['general']['releases']) == set(['WORK', 'DR15', 'DR16'])
    assert ss._cache['releases']['DR15'] == ss._cache['releases']['DR16']
    assert deepdiff.DeepDiff(ss._cache['releases']['DR15'], ss._cache['releases']['DR16']) == {}

def test_release_partial_cache(makefile, validyaml):
    """ test that the partial cache works for new releases """
    validyaml('fits')
    dr16 = makefile(env='dr16')
    dr17 = makefile(env='dr17', extra_cols=True)

    # dr16 - copy valid cache from WORK
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits', verbose=True, release='DR16')
    dm.write_stubs(use_cache_release='WORK', full_cache=True)

    # dr17
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits', verbose=True, release='DR17')
    dm.write_stubs(use_cache_release='DR16')

    ss = dm.get_stub('yaml')
    ss.update_cache()
    assert set(ss._cache['general']['releases']) == {'WORK', 'DR16', 'DR17'}
    hdu2a = ss._cache['releases']['DR16']['hdus']['hdu2']
    hdu2b = ss._cache['releases']['DR17']['hdus']['hdu2']
    assert 'field' not in hdu2a['columns']
    assert 'field' in hdu2b['columns']
    assert 'replace me - with content' in hdu2b['columns']['field']['unit']
    assert hdu2b['columns']['field']['name'] == 'FIELD'
    assert 'mjd' in hdu2b['columns']


