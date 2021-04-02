# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: loaders.py
# Project: io
# Author: Brian Cherinka
# Created: Friday, 2nd April 2021 3:22:28 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Friday, 2nd April 2021 3:22:28 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import pathlib
import os
import yaml
from typing import Union

from datamodel import log


def get_yaml_files(get: str = None) -> Union[str, list]:
    """ Get a list of yaml files

    Return a list of YAML files in the datamodel directory.

    Parameters
    ----------
    get : str, optional
        type of yaml file to get, can be "releases" or "products", by default None

    Returns
    -------
    Union[str, list]
        The yaml file path or list of yaml file paths
    """
    envvar = os.environ.get('DATAMODEL_DIR', None)
    if not envvar:
        log.error('Cannot get yaml files.  No DATAMODEL_DIR envvar set.  Check your installation.')
        return None

    datamodel_dir = envvar / pathlib.Path('datamodel')

    files = datamodel_dir.rglob(f'*.yaml')
    if not get:
        return list(files)
    elif get == 'releases':
        file = [i for i in files if 'releases' in str(i)]
        return file[0] if file else None
    elif get == 'products':
        return [i for i in files if 'products' in str(i)]


def read_yaml(ymlfile: Union[str, pathlib.Path]) -> dict:
    """ Opens and reads a YAML file

    Parameters
    ----------
    ymlfile : Union[str, pathlib.Path]
        a file or pathlib.Path object

    Returns
    -------
    dict
        the YAML content
    """

    if isinstance(ymlfile, str):
        ymlfile = pathlib.Path(ymlfile)

    with open(ymlfile, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data
