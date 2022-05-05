# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pytest
from datamodel.command.install import Install


def test_install_directory(tmp_path, ins):
    """ test setting up the directories for install """
    ins.set_directory()
    assert ins.directory['home'] == str(tmp_path)
    assert ins.directory['root'] == str(tmp_path / 'software')
    assert ins.directory['software'].startswith(str(tmp_path))
    assert ins.directory['etc'] == str(tmp_path / 'base' / 'etc')

def test_install_clone(dirins):
    """ test cloning the datamodel repo """
    assert not os.path.exists(dirins.directory['branch'])
    dirins.clone()
    assert os.path.exists(dirins.directory['branch'])
    assert dirins.git.repo.working_dir == dirins.directory['branch']

@pytest.mark.parametrize('branch', ['main', 'test'])
def test_install_checkout(branch):
    """ test checking out a branch """
    ins = Install(branch=branch)
    ins.set_directory()
    ins.clone()

    assert ins.directory['branch'] == f"{ins.directory['software']}/{branch}"

    assert ins.git.current_branch == 'main'
    ins.checkout_branch()
    assert ins.git.current_branch == branch

def test_install_modules(checkins):
    """ test creating a new datamodel modulefile """
    assert not hasattr(checkins, 'modulefile')
    checkins.set_modulefile()
    assert hasattr(checkins, 'modulefile')
    assert os.path.exists(checkins.modulefile['path'])
    assert "set version main\n" in checkins.modulefile["content"]

def test_install_done(modins, capsys):
    """ test output install done messaging """
    modins.done()
    captured = capsys.readouterr()
    assert "INSTALL> main branch installed at path=" in captured.out
    assert "please do the following in a new terminal:" in captured.out
    assert "module load datamodel/main." in captured.out

