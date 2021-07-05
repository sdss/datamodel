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

import deepdiff
from datamodel.generate import DataModel



def test_default_create_file(testfile):
    assert testfile.exists()

@pytest.mark.parametrize('ver, env', [('v1', 'dr15'), ('v2', 'dr16')])
def test_create_file(makefile, ver, env):
    testfile = makefile(version=ver, env=env)
    assert testfile.exists()
    assert ver in str(testfile)
    assert env in str(testfile)
    assert 'testfile_a.fits' in str(testfile)


def test_datamodel_generate(testfile):
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits')
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    assert os.path.exists(ss.output)
    assert ss.validate_cache() is False


def test_datamodel_nokeys_ok():
    path = 'BOSS_PHOTOBJ/astromqa/astromQAFields.fits'
    dm = DataModel(file_spec='astromQAFields', path=path, release="DR10")
    assert isinstance(dm, DataModel)
    assert dm.location == 'astromqa/astromQAFields.fits'

def test_datamodel_nokeys(testfile):
    with pytest.raises(ValueError, match='A set of keywords must be provided along with a either a path or location'):
        DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits')

def test_valid_datamodel(datamodel, validyaml):
    ss = datamodel.get_stub('yaml')
    datamodel.write_stubs()
    ss.update_cache()
    # assert valid yaml content
    assert os.path.exists(ss.output)
    assert ss.validate_cache() is True

    # assert other stubs exist
    for stub in ['md', 'json', 'access']:
        ss = datamodel.get_stub(stub)
        assert os.path.exists(ss.output)


def test_release_same_cache(makefile, validyaml):
    dr15 = makefile(env='dr15')
    dr16 = makefile(env='dr16')

    # dr15
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