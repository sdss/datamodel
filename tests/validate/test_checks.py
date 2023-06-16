# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pytest

from datamodel.validate import validate_models, revalidate, compare_path, check_invalid

@pytest.mark.parametrize('a, b, exp',
                         [('filename.fits', 'filename.fits', True),
                          ('filename.fits', 'filename.fits.gz', True),
                          ('filename.fits', 'filename.fits.bz2', True),
                          ('otherfile.fits', 'filename.fits', False)],
                         ids=['same', 'gz', 'bz2', 'diff'])
def test_compare(a, b, exp):
    """ test compare two paths """
    assert compare_path(a, b) is exp



gdata = {'in_sdss_access': True,
        'path_name': 'test',
        'path_template': '$TEST_REDUX/{ver}/testfile_{id}.fits',
        'path_kwargs': ['ver', 'id'],
        'access_string': 'test = $TEST_REDUX/{ver}/testfile_{id}.fits'}

@pytest.mark.parametrize('data, exp',
                         [({}, None),
                          ({'in_sdss_access': False}, None),
                          ({'in_sdss_access': True, 'path_name': 'badtest'},
                           ('test', 'path name badtest not found in sdsswork tree.')),
                          ({'in_sdss_access': True, 'path_name': 'test',
                            'path_template': '$TEST_REDUX/{ver}/file_{id}.fits'},
                           ('test', 'product path template $TEST_REDUX/{ver}/file_{id}.fits does not match sdsswork tree path template $TEST_REDUX/{ver}/testfile_{id}.fits')),
                          ({'in_sdss_access': True, 'path_name': 'test',
                            'path_template': '$TEST_REDUX/{ver}/testfile_{id}.fits',
                            'access_string': 'test = $TEST_REDUX/{ver}/file_{id}.fits'},
                           ('test', 'product access key $TEST_REDUX/{ver}/file_{id}.fits does not match sdsswork tree path template $TEST_REDUX/{ver}/testfile_{id}.fits.')),
                          (gdata, None)],
                         ids=['empty', 'no_sdss_access', 'bad_name', 'bad_path', 'bad_access', 'good'])
def test_check_invalid(data, exp):
    """ test check for invalid access info """
    out = check_invalid('test', data, 'WORK')
    assert out == exp


def test_validate_models(validmodel):
    """ test validate models"""
    validmodel('fits')
    validate_models()


def test_validate_models_fail(validyaml):
    """ test validate models fails """
    validyaml('fits')
    with pytest.raises(ValueError, match='The following YAMLs do not yet have validated JSON datamodels'):
        validate_models()

def test_revalidate(validyaml):
    """ test revalidate """
    path = validyaml('fits')
    jpath = path.as_posix().replace('yaml', 'json')
    assert not os.path.exists(jpath)
    revalidate('test', release='WORK')
    assert os.path.exists(jpath)
