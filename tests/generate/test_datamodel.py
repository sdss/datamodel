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
    dm = DataModel(file_spec='test', keywords=['ver=v1', 'id=a'], path='TEST_REDUX/{ver}/testfile_{id}.fits', verbose=True)
    dm.write_stubs()
    ss = dm.get_stub('yaml')
    assert os.path.exists(ss.output)