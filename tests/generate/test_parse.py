# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: test_parse.py
# Project: generate
# Author: Brian Cherinka
# Created: Saturday, 1st May 2021 5:09:31 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Saturday, 1st May 2021 5:09:31 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

import pytest
from datamodel.generate.parse import get_abstract_path, get_abstract_key, get_file_spec


@pytest.mark.parametrize('name, exp',
                         [('mangaRss', 'mangaRss'),
                          ('plate6', 'plate6'),
                          ('apogee-rc', 'apogee-rc'),
                          ('bad#$name', None)])
def test_get_file_spec(name, exp):
    filespec = get_file_spec(name)
    assert filespec == exp


@pytest.mark.parametrize('name, exp, brack',
                         [('plate', 'PLATE', False),
                          ('plate', '[PLATE]', True),
                          ('plate:0>5', 'PLATE5', False),
                          (1234, None, False)])
def test_abstract_key(name, exp, brack):
    filespec = get_abstract_key(name, add_brackets=brack)
    assert filespec == exp


@pytest.mark.parametrize('name, exp, brack',
                         [('path/{one}/{two:0>5}/file.fits', 'path/ONE/TWO5/file.fits', False),
                          ('path/{one}/{two:0>5}/file.fits', 'path/[ONE]/[TWO5]/file.fits', True),
                          ('path/@one|/{two:0>5}/file.fits', 'path/ONE/TWO5/file.fits', False),
                          ], ids=['normal', 'brackets', 'special'])
def test_abstract_path(name, exp, brack):
    filespec = get_abstract_path(name, add_brackets=brack)
    assert filespec == exp

