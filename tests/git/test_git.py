# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pathlib
import pytest
from datamodel.git import Git


@pytest.fixture
def git(monkeypatch, git_repo):
    path = git_repo.workspace
    monkeypatch.setenv("DATAMODEL_DIR", path)
    g = Git(verbose=True)
    g.repo.create_remote('origin', 'https://github.com/havok2063/test.git')
    yield g
    g = None

@pytest.fixture
def remote(git):
    git.origin.fetch()
    # create initial head and set up remote tracking
    git.repo.create_head("main", git.origin.refs.main)
    git.repo.heads.main.set_tracking_branch(git.origin.refs.main)
    git.repo.heads.main.checkout()
    git.repo.git.checkout('HEAD', b='master')
    # push it to the remote
    git.origin.push(git.repo.active_branch, set_upstream=True)
    yield git
    # delete it from the remote
    git.origin.push(git.repo.heads.master, delete=True)
    git.origin.fetch()


@pytest.fixture
def make_file(git):
    def _make_file(name):
        p = pathlib.Path(f"{git.directory}") / f'{name}.txt'
        with open(p, 'w') as f:
            f.write('test stuff')
        return str(p)
    return _make_file


@pytest.fixture
def test_file(git, make_file):
    path = make_file('test')
    git.add(path)
    git.commit('adding a test file')
    yield path


def test_git(git):
    assert git.directory == os.getenv("DATAMODEL_DIR")
    assert 'tmp' in git.directory
    assert git.current_branch == 'master'
    assert git.list_remotes(pprint=True) == ['origin']

def test_git_clone(git):
    outpath = f'{git.directory}/tmp_datamodel'
    git.clone(branch=outpath)
    assert os.path.exists(outpath)

def test_git_checkout(git):
    assert git.current_branch == 'master'
    git.checkout('test')
    assert git.current_branch == 'test'
    assert git.is_main_branch is False

def test_get_location(git):
    path = f'{git.directory}/project/test.txt'
    loc = git.get_path_location(path)
    assert loc == 'project/test.txt'

def test_git_add(git, make_file):
    path = make_file('test')
    assert git.check_if_untracked(path) is True
    git.add(path)
    assert git.check_if_untracked(path) is False

def test_git_commit(git, make_file):
    path = make_file('test')
    git.add(path)
    message = 'adding a test file'
    git.commit(message)
    assert message == git.repo.commit("master").message

def test_git_remove(git, test_file):
    assert os.path.exists(test_file)
    assert git.check_if_untracked(test_file) is False
    git.rm(test_file)
    git.commit('removing test file')
    assert git.check_if_untracked(test_file) is True

def test_git_pull_fail_no_remote(remote):
    remote.checkout("test")
    with pytest.raises(RuntimeError, match='Current active branch test does not exist on remote.'):
        remote.pull()

def test_git_pull_fail_dirty(remote, make_file):
    path = make_file('test')
    remote.add(path)
    with pytest.raises(RuntimeError, match='Current repo is dirty.  Please stash or commit your changes before pulling.'):
        remote.pull()

def test_git_pull(remote, test_file, caplog):
    remote.pull()
    assert "Pulling from repo." in caplog.text


def test_git_push_fail_dirty(remote, make_file):
    path = make_file('test')
    remote.add(path)
    with pytest.raises(RuntimeError, match='Current repo is dirty.  Please stash or commit your changes before pushing.'):
        remote.push()

def test_git_push(remote, test_file, caplog):
    remote.push()
    assert "Pushing to repo." in caplog.text

def test_git_push_no_remote(remote, test_file, caplog):
    remote.checkout("test")
    remote.push()
    assert "Current active branch test does not exist on remote. Setting upstream to origin" in caplog.text
    assert "Pushing to repo." in caplog.text
    remote.origin.push(remote.repo.active_branch, delete=True)
