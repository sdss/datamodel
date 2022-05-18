# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pathlib
import pytest
from datamodel.git import Git
from datamodel.git.git import Repo
from datamodel.generate.stub import YamlStub

#cfg = self.repo.config_reader()

class Cfg(dict):
    """ Fake git repo config ini """

    def has_option(self, section, option):
        """ fake ini has_option method """
        return (section in self) and (option in self[section])

    def get(self, key, value=None):
        """ fake ini get method """
        return self[key][value] if value else self[key]

def cfgpatch_nouser(self):
    """ patch a git config with no user info """
    return Cfg({})

def cfgpatch_user(self):
    """ patch a git config with user info """
    return Cfg({"user": {"email": "testuser@test.edu"}})

@pytest.fixture
def mock_cfg_nouser(monkeypatch):
    """ mock the config reader to return a mock config object """
    monkeypatch.setattr(Repo, 'config_reader', cfgpatch_nouser)

@pytest.fixture
def mock_cfg_user(monkeypatch):
    """ mock the config reader to return a mock config object """
    monkeypatch.setattr(Repo, 'config_reader', cfgpatch_user)


@pytest.fixture
def git(monkeypatch, git_repo):
    """ fixture to create a git object and load an empty repo"""
    path = git_repo.workspace
    monkeypatch.setenv("DATAMODEL_DIR", path)
    g = Git(verbose=True)
    g.repo.create_remote('origin', 'git@github.com:havok2063/test.git')
    yield g
    g = None


@pytest.fixture
def main(git):
    """ fixture to set up a main branch from the remote """
    git.origin.fetch()
    # create initial head and set up remote tracking
    git.repo.create_head("main", git.origin.refs.main)
    git.repo.heads.main.set_tracking_branch(git.origin.refs.main)
    git.repo.heads.main.checkout()
    yield git


@pytest.fixture
def remote(main):
    """ fixture to fully set up a remote, create a master branch, and push ht """
    main.repo.git.checkout('HEAD', b='master')
    # push it to the remote
    main.origin.push(main.repo.active_branch, set_upstream=True)
    yield main
    # delete it from the remote
    main.origin.push(main.repo.heads.master, delete=True)
    main.origin.fetch()


@pytest.fixture()
def stub(remote, make_file):
    """ fixture to create a simple fake stub with the mock git repo """
    path = make_file('test')
    yy = YamlStub()
    yy.git = remote
    yy.output = path
    yy.datamodel = type('obj', (object,), {'file_species' : 'test'})
    yield yy
    yy = None


@pytest.fixture
def make_file(git):
    """ fixure factory to make a file in the git repo """
    def _make_file(name):
        p = pathlib.Path(f"{git.directory}") / f'{name}.txt'
        with open(p, 'w') as f:
            f.write('test stuff')
        return str(p)
    return _make_file


@pytest.fixture
def test_file(git, make_file):
    """ fixture to make a test file, add and commit it into the repo """
    path = make_file('test')
    git.add(path)
    git.commit('adding a test file')
    yield path


def test_git(git):
    """ test that the git repo is instantiated correctly """
    assert git.directory == os.getenv("DATAMODEL_DIR")
    assert 'tmp' in git.directory
    assert git.current_branch == 'master'
    assert git.list_remotes(pprint=True) == ['origin']

def test_git_clone(git):
    """ test that a clone is created correctly """
    outpath = f'{git.directory}/tmp_datamodel'
    git.clone(branch=outpath)
    assert os.path.exists(outpath)

def test_git_status(git, test_file):
    output = git.status()
    assert 'On branch master' in output
    assert "nothing to commit, working tree clean" in output

def test_git_checkout(git):
    """ test git checkout of a new branch """
    assert git.current_branch == 'master'
    git.checkout('test')
    assert git.current_branch == 'test'
    assert git.is_main_branch is False

def test_git_create_branch(git):
    """ test git create a new named branch """
    assert git.current_branch == 'master'
    git.create_new_branch("test")
    assert git.current_branch == "test"
    assert git.is_main_branch is False

def test_git_create_branch_cfg_user(mock_cfg_user, git):
    """ test git create a new branch with git config email """
    assert git.current_branch == 'master'
    git.create_new_branch()
    assert git.current_branch == "dmgen_testuser"

def test_git_create_branch_cfg_nouser(mock_cfg_nouser, git):
    """ test git create new branch with uuid """
    assert git.current_branch == 'master'
    git.create_new_branch()
    assert git.current_branch.startswith("dmgen_")

def test_get_location(git):
    """ test that we can extract a relative location from a path """
    path = f'{git.directory}/project/test.txt'
    loc = git.get_path_location(path)
    assert loc == 'project/test.txt'

def test_git_add(git, make_file):
    """ test we can git add a file to the repo"""
    path = make_file('test')
    assert git.check_if_untracked(path) is True
    git.add(path)
    assert git.check_if_untracked(path) is False

def test_git_add_fail_on_main(main, make_file):
    """ test git add fails if on main branch """
    assert main.current_branch == 'main'
    path = make_file('test')
    with pytest.raises(AttributeError, match="Cannot add files to the main branch. Please make your changes in a new branch."):
        main.add(path)

def test_git_commit(git, make_file):
    """ test we can git commit a file to the repo """
    path = make_file('test')
    git.add(path)
    message = 'adding a test file'
    git.commit(message)
    assert message == git.repo.commit("master").message

def test_git_remove(git, test_file):
    """ test we can git remove a file from the repo """
    assert os.path.exists(test_file)
    assert git.check_if_untracked(test_file) is False
    git.rm(test_file)
    git.commit('removing test file')
    assert git.check_if_untracked(test_file) is True

def test_git_rm_fail_on_main(main, make_file):
    """ test git rm fails if on main branch """
    assert main.current_branch == 'main'
    path = make_file('test')
    with pytest.raises(AttributeError, match="Cannot remove files from the main branch. Please make your changes in a new branch."):
        main.rm(path)

@pytest.mark.gitremote
def test_git_pull_fail_no_remote(remote):
    """ test git pull fails if the branch does not exist on remote """
    remote.checkout("test")
    with pytest.raises(RuntimeError, match='Current active branch test does not exist on remote.'):
        remote.pull()

@pytest.mark.gitremote
def test_git_pull_fail_dirty(remote, make_file):
    """ test git pull fails if the repo is dirty, i.e. has uncommited changes """
    path = make_file('test')
    remote.add(path)
    with pytest.raises(RuntimeError, match='Current repo is dirty.  Please stash or commit your changes before pulling.'):
        remote.pull()

@pytest.mark.gitremote
def test_git_pull(remote, test_file, caplog):
    """ test git pull works correctly """
    remote.pull()
    assert "Pulling from repo." in caplog.text

@pytest.mark.gitremote
def test_git_push_fail_dirty(remote, make_file):
    """ test git push fails if the repo is dirty """
    path = make_file('test')
    remote.add(path)
    with pytest.raises(RuntimeError, match='Current repo is dirty.  Please stash or commit your changes before pushing.'):
        remote.push()

@pytest.mark.gitremote
def test_git_push(remote, test_file, caplog):
    """ test git push works correctly """
    remote.push()
    assert "Pushing to repo." in caplog.text

@pytest.mark.gitremote
def test_git_push_no_remote(remote, test_file, caplog):
    """ test git push pushes a new branch upstream to remote """
    remote.checkout("test")
    remote.push()
    assert "Current active branch test does not exist on remote. Setting upstream to origin" in caplog.text
    assert "Pushing to repo." in caplog.text
    remote.origin.push(remote.repo.active_branch, delete=True)


@pytest.mark.gitremote
def test_dm_git_commit(stub):
    """ test the stub git add/commit """
    stub.git.checkout('main')
    assert stub.git.current_branch == 'main'
    stub.commit_to_git()
    assert stub.git.current_branch != 'main'
    assert stub.git.current_branch == 'dmgen-fs-test'


@pytest.mark.gitremote
def test_dm_git_pushpull(stub):
    """ test the stub git push/pull """
    stub.git.checkout('dmgen-fs-test')
    assert stub.git.current_branch == 'dmgen-fs-test'
    assert stub.git.branch_exists_on_remote is False
    stub.push_to_git()
    assert stub.git.current_branch != 'main'
    assert stub.git.branch_exists_on_remote is True


@pytest.mark.gitremote
def test_dm_git_remove(stub):
    """ test the stub git remove """
    stub.git.checkout('main')
    assert stub.git.current_branch == 'main'
    stub.commit_to_git()
    stub.remove_from_git()
    assert stub.git.current_branch != 'main'
    assert stub.git.current_branch == 'dmgen-fs-test'



