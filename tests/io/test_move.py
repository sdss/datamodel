# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pytest
import pathlib
from datamodel.io.move import dm_move, find_files_from_species, construct_new_path, dm_move_species


@pytest.fixture()
def make_files(testfits, makefile):
    fileb = makefile(id='b', suffix='fits')
    yield testfits, fileb


def test_move_single_file(testfits):
    """ test that we can move a single file """

    new_path = pathlib.Path(str(testfits).replace('testwork', 'dr17'))

    assert testfits.is_file()
    assert not new_path.exists()

    dm_move(testfits, new_path)

    assert testfits.exists()
    assert new_path.exists()


def test_move_single_file_nosymlink(testfits):
    """ test that we can move a single file with no symlink """

    new_path = pathlib.Path(str(testfits).replace('testwork', 'dr17'))

    assert testfits.is_file()
    assert not new_path.exists()

    dm_move(testfits, new_path, symlink=False)

    assert not testfits.exists()
    assert new_path.exists()


def test_move_directory(make_files):
    """ test that we can move a single file with no symlink """

    filea, fileb = make_files
    assert fileb.exists()

    new_filea = pathlib.Path(str(filea).replace('testwork', 'dr17'))
    new_path = pathlib.Path(str(fileb).replace('testwork', 'dr17'))

    assert fileb.is_file()
    assert not new_path.exists()
    assert not new_path.parent.exists()

    dm_move(fileb, new_path, parent=True)

    assert fileb.is_file()
    assert fileb.parent.exists()
    assert new_path.parent.exists()
    assert new_path.exists()
    assert new_filea.exists()
    assert new_filea.exists()

def test_find_file_species(make_files):
    filea, fileb = make_files

    files = list(find_files_from_species('$TEST_REDUX/{ver}/testfile_{id}.fits'))
    assert len(files) == 2
    assert filea in files
    assert fileb in files


def test_move_multiple_files(make_files, makefile):
    """ test that we can move a multiple files of a species """

    filea, fileb = make_files
    newfile = makefile(name='newfile-1234.fits', suffix='fits')
    sumfile = makefile(name='summaryFile.fits', suffix='fits')
    assert newfile.exists()
    assert sumfile.exists()

    files = find_files_from_species('$TEST_REDUX/{ver}/testfile_{id}.fits')

    for file in files:

        new_path = pathlib.Path(str(file).replace('testwork', 'dr17'))
        assert file.is_file()
        assert not new_path.exists()

        dm_move(file, new_path)

        assert file.parent.exists()
        assert new_path.exists()

    new_sumpath = pathlib.Path(str(sumfile).replace('testwork', 'dr17'))
    assert not new_sumpath.exists()


def test_construct_new_path():
    old_path = 'MANGA_SANDBOX/galaxyzoo3d/{ver}/gz3d_metadata.fits'
    new_path = 'MANGA_MORPHOLOGY/galaxyzoo3d/{ver}/gz3d_metadata.fits'

    before = os.path.expandvars(f'${old_path}')
    assert 'mangawork/manga/sandbox' in before
    exp = construct_new_path(old_path=old_path, new_path=new_path,
                             release='DR17', kwargs={'ver':'v4_0_0'})
    assert 'dr17/manga/morphology' in str(exp)


def test_construct_new_path_by_file(make_files):
    filea, fileb = make_files
    old_path = 'TEST_REDUX/{ver}/testfile_{id}.fits'

    before = os.path.expandvars(f'${old_path}')
    assert 'testwork' in before
    exp = construct_new_path(file=fileb, old_path=old_path, new_path=old_path,
                             release='DR17')
    assert 'dr17' in str(exp)


def test_move_species(make_files, makefile):
    filea, fileb = make_files
    newfile = makefile(name='newfile-1234.fits', suffix='fits')
    sumfile = makefile(name='summaryFile.fits', suffix='fits')
    assert newfile.exists()
    assert sumfile.exists()
    new_fullpath = pathlib.Path(str(fileb).replace('testwork', 'dr17'))
    assert not new_fullpath.exists()

    old_path = 'TEST_REDUX/{ver}/testfile_{id}.fits'
    new_path = 'TEST_REDUX/{ver}/testfile_{id}.fits'
    dm_move_species(old_path, new_path, 'DR17')

    new_sumpath = pathlib.Path(str(sumfile).replace('testwork', 'dr17'))
    assert not new_sumpath.exists()
    assert new_fullpath.exists()
