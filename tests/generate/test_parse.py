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
from datamodel.generate.parse import get_abstract_path, get_abstract_key, get_file_spec, find_kwargs


@pytest.mark.parametrize('name, exp',
                         [('mangaRss', 'mangaRss'),
                          ('plate6', 'plate6'),
                          ('apogee-rc', 'apogee-rc'),
                          ('bad#$name', None)])
def test_get_file_spec(name, exp):
    """ test the get_file_spec function """
    filespec = get_file_spec(name)
    assert filespec == exp


@pytest.mark.parametrize('name, exp, brack',
                         [('plate', 'PLATE', False),
                          ('plate', '[PLATE]', True),
                          ('plate:0>5', 'PLATE5', False),
                          (1234, None, False)])
def test_abstract_key(name, exp, brack):
    """ test the get_abstract_key function """
    filespec = get_abstract_key(name, add_brackets=brack)
    assert filespec == exp


@pytest.mark.parametrize('name, exp, brack',
                         [('path/{one}/{two:0>5}/file.fits', 'path/ONE/TWO5/file.fits', False),
                          ('path/{one}/{two:0>5}/file.fits', 'path/[ONE]/[TWO5]/file.fits', True),
                          ('path/@one|/{two:0>5}/file.fits', 'path/ONE/TWO5/file.fits', False),
                          ], ids=['normal', 'brackets', 'special'])
def test_abstract_path(name, exp, brack):
    """ test the get_abstract_path function """
    filespec = get_abstract_path(name, add_brackets=brack)
    assert filespec == exp


@pytest.mark.parametrize('loc, examp, keys',
                         [('{mjd}/sdR-{br}{id}-{frame}.fits.gz', '55049/sdR-b1-00100006.fits.gz',
                           {'mjd': '55049', 'br': 'b', 'id': '1', 'frame': '00100006'}),
                          ('{rerun}/{run}/objcs/{camcol}/fpBIN-{run:0>6}-{filter}{camcol}-{field:0>4}.fit',
                           '1/45/objcs/3/fpBIN-000045-g3-0123.fit',
                           {'rerun': '1', 'run': '45', 'camcol': '3', 'filter': 'g', 'field': '0123'}),
                          ('galaxy_{dr}{version}_{sample}_{ns}.fits.gz', 'galaxy_DR12v1.0_1_n.fits.gz',
                           {'dr': 'DR12', 'version': 'v1.0', 'sample': '1', 'ns': 'n'}),
                          ('{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz',
                           'v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz',
                           {'drpver': 'v2_4_3', 'plate': '8485', 'ifu': '1901', 'wave': 'LOG'})],
                         ids=['sdR', 'fpBIN', 'galaxy', 'mangarss'])
def test_find_kwargs(loc, examp, keys):
    out = find_kwargs(loc, examp)
    assert out == keys
