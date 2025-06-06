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


@pytest.fixture
def testdm(testfits):
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'],
                   path='TEST_REDUX/{ver}/testfile_{id}.fits', access_path_name="test-file")
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    ss.update_cache()
    yield dm, ss


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

def test_datamodel_tcomm(testdm):
    dm, ss = testdm
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
    assert hdu2b['columns']['param']['unit'] == 'm'
    assert hdu2b['columns']['field']['unit'] == ''
    assert hdu2b['columns']['field']['name'] == 'field'
    assert 'mjd' in hdu2b['columns']


def test_datamodel_table_header(validmodel):
    validmodel('fits')
    dm = DataModel.from_yaml('test', release='WORK')
    ss = dm.get_stub('yaml')
    ss.update_cache()
    hdu2 = ss._cache['releases']['WORK']['hdus']['hdu2']
    assert 'header' in hdu2
    assert hdu2['header'][2] == {"key": "TTYPE1", "value": "OBJECT", "comment": "an object name"}


def test_default_work_release_sdss5(caplog):
    dm = DataModel(file_spec='rsCompleteness', keywords=['plan=A', 'observatory=APO'],
                   path='ROBOSTRATEGY_DATA/allocations/{plan}/rsCompleteness-{plan}-{observatory}.fits',
                   verbose=True, release='WORK')
    assert dm.release == 'WORK'
    assert dm.tree_ver == 'sdsswork'

    msg = 'Please add this environment=ROBOSTRATEGY_DATA to the tree product, and try again.'
    assert msg not in caplog.text


def test_work_release_sdsswork(caplog, monkeypatch, mocker):
    monkeypatch.delenv("MANGA_SPECTRO_REDUX")
    assert 'MANGA_SPECTRO_REDUX' not in os.environ

    # patch this to return an empty dict
    mocker.patch('datamodel.generate.datamodel.Tree.get_orig_os_environ', return_value={})

    dm = DataModel(file_spec='mangacube',
                   path='MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}CUBE.fits.gz',
                   keywords=['drpver=v3_1_1','plate=8485','ifu=1901','wave=LOG'],
                   release='WORK', verbose=True)
    assert dm.release == 'WORK'
    assert dm.tree_ver == 'sdsswork'

    msg = 'Please add this environment=MANGA_SPECTRO_REDUX to the tree product, and try again.'
    assert msg in caplog.text

def test_work_treever_sdsswork(caplog):
    dm = DataModel(file_spec='rsCompleteness', keywords=['plan=A', 'observatory=APO'],
                   path='ROBOSTRATEGY_DATA/allocations/{plan}/rsCompleteness-{plan}-{observatory}.fits',
                   verbose=True, release='WORK')
    assert dm.release == 'WORK'
    assert dm.tree_ver == 'sdsswork'

    msg = 'Please add this environment=ROBOSTRATEGY_DATA to the tree product, and try again.'
    assert msg not in caplog.text


def test_rsp_true(testfits):
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'],
                   path='TEST_REDUX/{ver}/testfile_{id}.fits',
                   access_path_name="test-file", science_product=True)
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    ss.update_cache()

    assert dm.recommended_science_product is True
    assert ss._cache['general']['recommended_science_product'] is True


def test_vac_false(testdm):
    dm, ss = testdm
    assert dm.vac is False
    assert ss._cache['general']['vac'] is False

    # also check for rsp is false generically
    assert dm.recommended_science_product is False
    assert ss._cache['general']['recommended_science_product'] is False

def test_vac_true():
    dm = DataModel(file_spec='mangaGEMA',
                   path='MANGA_GEMA/{gemaver}/GEMA-{gemaver}.fits',
                   keywords=['gemaver=1.0.1'],
                   tree_ver='sdsswork', verbose=True)

    assert dm.vac is True
    assert dm.recommended_science_product is True

def test_valid_notes(validmodel):
    validmodel('fits')
    dm = DataModel.from_yaml('test', release='WORK')
    dm.write_stubs()

    ss = dm.get_stub('yaml')
    ss.update_cache()
    assert ss._cache['notes'] == 'here are some notes\nand more notes\n'

    ss = dm.get_stub('json')
    ss.update_cache()
    assert ss._cache['notes'] == 'here are some notes\nand more notes\n'


def test_remove_release(makefile, validmodel):
    validmodel('fits')
    dr15 = makefile(env='dr15')
    dr16 = makefile(env='dr16')

    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits', verbose=True, release='DR15')
    dm.write_stubs(use_cache_release='WORK', full_cache=True)

    ss = dm.get_stub()
    ss.update_cache()
    assert "DR15" in ss._cache['general']['releases']

    ss.remove_release("DR15")
    ss.write()

    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits', verbose=True, release='DR16')
    ss = dm.get_stub()
    ss.update_cache()
    assert "DR15" not in ss._cache['general']['releases']

@pytest.fixture()
def validstub(validmodel):
    validmodel('fits')
    dm = DataModel.from_yaml('test', release='WORK')
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    ss.update_cache()
    yield ss
    dm = None
    ss = None

def test_table_mixcase(validstub):
    """ test we retain the original case of the table column name"""
    hdu = validstub._cache['releases']['WORK']['hdus']['hdu2']

    assert 'param' in hdu['columns']
    assert 'PARAM' not in hdu['columns']
    assert 'UPPER' in hdu['columns']
    assert 'mixCase' in hdu['columns']
    assert 'MIXCASE' not in hdu['columns']
    assert 'mixcase' not in hdu['columns']
    assert hdu['columns']['mixCase']['name'] == 'mixCase'
    assert hdu['columns']['param']['name'] == 'param'
    assert hdu['columns']['UPPER']['name'] == 'UPPER'

def test_par(datamodel):
    """ test the par example is written and read correctly """
    dm = datamodel('par')
    ss = dm.get_stub('yaml')
    ss.update_cache()
    table = ss._cache['releases']["WORK"]['par']['tables']["TABLE"]
    item = table['structure'][-1]
    assert item['type'] == "char[3][2]"
    assert item['example'] == ['11', '##', 'aa']

def test_valid_regrets(validmodel):
    """ test we have some regrets """
    validmodel('fits')
    dm = DataModel.from_yaml('test', release='WORK')
    dm.write_stubs()

    ss = dm.get_stub('yaml')
    ss.update_cache()
    assert ss._cache['regrets'] == 'here are some regrets\nand more regrets\n'

    ss = dm.get_stub('json')
    ss.update_cache()
    assert ss._cache['regrets'] == 'here are some regrets\nand more regrets\n'
