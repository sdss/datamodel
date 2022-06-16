# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pytest

from datamodel.validate import update_datamodel_access, update_tree, clone_tree
from ..conftest import MockTreeEnv, MockTree, MockPath
from sdss_access.path import Path


@pytest.fixture()
def validmodel(monkeypatch, mocker, validyaml, datamodel):
    """ fixture to product a valid datamodel with no access info """
    mocker.patch('datamodel.generate.datamodel.Tree', new=MockTreeEnv)
    mocker.patch('datamodel.generate.datamodel.Path', new=Path)
    mocker.patch('datamodel.validate.check.Tree', new=MockTreeEnv)
    mocker.patch('datamodel.validate.add.Tree', new=MockTreeEnv)

    validyaml(suffix='noaccess')
    yield datamodel(suffix='fits')


@pytest.fixture
def clonetree(monkeypatch, tmpdir):
    """ fixture to clone the tree product """
    path = tmpdir.mkdir('clone').mkdir('tree')
    clone_tree(path=path)
    monkeypatch.setenv("TREE_DIR", str(path))
    yield path


def check_json(dm, exp=False):
    """ asserts for json stub """
    json = dm.get_stub('json')
    json.update_cache()
    assert json._cache['releases']['WORK']['access']['in_sdss_access'] is exp


def test_update_dmacces(monkeypatch, mocker, validmodel):
    """ test that we can update the access info of a datamodel """
    # assert no access
    assert validmodel.access['WORK']['in_sdss_access'] is False
    check_json(validmodel, False)

    # reapply the mock
    mocker.patch('datamodel.generate.datamodel.Tree', new=MockTree)
    mocker.patch('datamodel.generate.datamodel.Path', new=MockPath)
    mocker.patch('datamodel.validate.check.Tree', new=MockTree)
    mocker.patch('datamodel.validate.add.Tree', new=MockTree)

    # test that we can add access
    update_datamodel_access(test=True, commit_to_git=False)
    dm = validmodel.__class__.from_yaml(validmodel.file_species)
    dm.write_stubs()
    assert dm.access['WORK']['in_sdss_access'] is True
    assert dm.access['WORK']['path_name'] == 'test'
    check_json(dm, True)


def test_update_tree(clonetree, validmodel):
    """ test that we can update the tree ini configs """
    m = MockTreeEnv('sdsswork')
    assert 'test' not in m.paths

    update_tree(local=True, skip_push=True, work_ver='sdsswork')

    m = MockTreeEnv('sdsswork')
    assert 'test' in m.paths
