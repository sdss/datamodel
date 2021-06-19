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
from click.testing import CliRunner
from datamodel.cli import cli
import pytest


def test_datamodel_cli():
    """ test the main datamodel click program """
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Command-line tool for handling SDSS datamodels" in result.output

@pytest.mark.parametrize('command, msg',
                         [('generate', 'Generate a datamodel file for a SDSS data product'),
                          ('wiki', 'Upload a datamodel to the wiki'),
                          ('install', 'Install the datamodel product at Utah'),
                          ('design', 'Design a datamodel for a new file')],
                         ids=['generate', 'wiki', 'install', 'design'])
def test_datamodel_help(command, msg):
    """ test the help of each datamodel click subcommand """
    runner = CliRunner()
    result = runner.invoke(cli, [command, '--help'])
    assert result.exit_code == 0
    assert msg in result.output
