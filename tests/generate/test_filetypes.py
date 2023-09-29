# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pytest
from datamodel.generate.filetypes.base import get_filetype, get_filesize, format_bytes



@pytest.mark.parametrize('file, exp',
                         [('test.fits', 'FITS'),
                          ('test.fits.gz', 'FITS'),
                          ('test.fits.bz2', 'FITS'),
                          ('test.fits.fz', 'FITS'),
                          ('test.hdf5', 'HDF5'),
                          ('test.par', 'PAR'),
                          ],
                         ids=['fits', 'gz', 'bz2', 'fz', 'hdf5', 'par'])
def test_get_filetypes(file, exp):
    ftype = get_filetype(file)
    assert ftype == exp


@pytest.mark.parametrize('num, exp',
                         [(1, '1 KB'),
                          (2, '1 MB'),
                          (3, '1 GB'),
                          (4, '1.0 TB'),
                          (5, '1024.0 TB')],
                         ids=['kb', 'mb', 'gb', 'tb', 'tb2'])
def test_format_bytes(num, exp):
    ftype = format_bytes(1024**num)
    assert ftype == exp


@pytest.mark.parametrize('num, exp',
                         [(1, '1 KB'),
                          (2, '1 MB'),
                          (3, '1 GB'),
                          (4, '1.0 TB'),
                          (5, '1024.0 TB')],
                         ids=['kb', 'mb', 'gb', 'tb', 'tb2'])
def test_get_filesize(mocker, num, exp):
    mocker.patch('os.path.getsize', return_value=1024**num)
    ftype = get_filesize('test.txt')
    assert ftype == exp
