# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: test_commands.py
# Project: cli
# Author: Brian Cherinka
# Created: Thursday, 17th June 2021 1:33:09 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Thursday, 17th June 2021 1:33:09 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

import os
import pytest
from click.testing import CliRunner
from datamodel.cli import cli


def test_datamodel_cli():
    """ test the main datamodel click program """
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Command-line tool for handling SDSS datamodels" in result.output

@pytest.mark.parametrize('command, msg',
                         [('generate', 'Generate a datamodel file for a SDSS data product'),
                          ('install', 'Install the datamodel product at Utah'),
                          ('design', 'Design a datamodel for a new file'),
                          ('update', 'Update existing datamodels with any new content added into the template'),
                          ('tree', 'Interact with the SDSS tree product')],
                         ids=['generate', 'install', 'design', 'update', 'tree'])
def test_datamodel_help(command, msg):
    """ test the help of each datamodel click subcommand """
    runner = CliRunner()
    result = runner.invoke(cli, [command, '--help'])
    assert result.exit_code == 0
    assert msg in result.output

@pytest.mark.parametrize('command, msg',
                         [('add', 'Add new access paths into the tree git product'),
                          ('check', 'Check the product path definitions are correct in tree'),
                          ('update', 'Update datamodel stubs with new access paths')],
                         ids=['add', 'check', 'update'])
def test_datamodel_tree_help(command, msg):
    """ test the help of each datamodel tree click subcommand """
    runner = CliRunner()
    result = runner.invoke(cli, ['tree', command, '--help'])
    assert result.exit_code == 0
    assert msg in result.output

def test_cli_datamodel_generate(testfits):
    """ test that cli generates a file """
    runner = CliRunner()
    result = runner.invoke(cli, ['generate', '-f', 'test', '-p', 'TEST_REDUX/{ver}/testfile_{id}.fits', '-k', 'ver=v1', '-k', 'id=a', '-v'])
    path = os.path.join(os.getenv("DATAMODEL_DIR"), 'datamodel/products/yaml/test.yaml')
    assert os.path.exists(path)

def test_cli_dm_generate_keywords(testfits):
    """ test that no keywords are allowed in cli """
    runner = CliRunner()
    result = runner.invoke(cli, ['generate', '-f', 'test', '-p', 'TEST_REDUX/testfile.fits', '-v'])
    assert ('Error: when --file_species is set, exactly 1 of the following '
            'parameters must be set:') not in result.output
    assert result.exit_code == 1


def test_cli_dm_design(yamlfile):
    """ test that cli designs a file """
    runner = CliRunner()
    result = runner.invoke(cli, ['design', '-f', 'test', '-p', 'TEST_REDUX/{ver}/testfile_{id}.fits'])
    assert os.path.exists(yamlfile)


def test_cli_dm_tree_check():
    """ test that cli can run a tree check """
    runner = CliRunner()
    result = runner.invoke(cli, ['tree', 'check', '-r', 'DR17'])
    assert result.exit_code == 0

def test_cli_dm_validate_check():
    """ test that cli can run a validate check """
    runner = CliRunner()
    result = runner.invoke(cli, ['validate', 'check'])
    assert result.exit_code == 0

def test_cli_dm_validate_redo(validmodel):
    """ test that cli can run a validate redo """
    validmodel('fits')
    runner = CliRunner()
    result = runner.invoke(cli, ['validate', 'redo', '-f', 'test', '-v'])
    assert result.exit_code == 0

def test_cli_dm_update(validmodel):
    """ test that cli can run an datamodel update """
    validmodel('fits')
    runner = CliRunner()
    result = runner.invoke(cli, ['update', '-f', 'test', '-v'])
    assert result.exit_code == 0

