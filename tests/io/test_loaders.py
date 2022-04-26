# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: test_loaders.py
# Project: io
# Author: Brian Cherinka
# Created: Sunday, 2nd May 2021 3:27:15 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Sunday, 2nd May 2021 3:27:15 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

from datamodel.io.loaders import get_yaml_files, read_yaml
import pathlib
import os
import pytest


@pytest.fixture()
def defaultdm(datamodel):
    yield datamodel('fits')

def test_get_yaml(defaultdm):
    """ test we can get a YAML file """
    files = get_yaml_files('products')
    exp = os.getenv("DATAMODEL_DIR") / pathlib.Path('datamodel') / 'products/yaml/test.yaml'
    assert len(files) == 1
    assert exp in files


def test_read_yaml(defaultdm):
    """ test we can read a YAML file """
    files = get_yaml_files('products')
    data = read_yaml(files[0])
    assert isinstance(data, dict)
    assert data['general']['name'] == 'test'