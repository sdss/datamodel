# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pytest
import pathlib
from datamodel.command.install import Install


@pytest.fixture(autouse=True)
def setup_install_env(monkeypatch, tmp_path):
    """ fixtures that sets up temp install directory """

    home_dir = tmp_path

    def mockhome():
        return pathlib.Path(home_dir)

    monkeypatch.setattr(pathlib.Path, 'home', mockhome)


@pytest.fixture
def ins():
    """ fixture to create a basic install object """
    yield Install()

@pytest.fixture
def dirins(ins):
    """ fixture that sets up directories """
    ins.set_directory()
    yield ins

@pytest.fixture
def cloneins(dirins):
    """ fixture that clones the datamodel repo"""
    dirins.clone()
    yield dirins

@pytest.fixture
def checkins(cloneins):
    """ fixture that checks out the main branch """
    cloneins.checkout_branch()
    yield cloneins

@pytest.fixture
def modins(checkins):
    """ fixture that sets up the modulefile """
    checkins.set_modulefile()
    yield checkins

@pytest.fixture
def doneins(modins):
    """ fixture of final install step"""
    modins.done()
    yield modins


