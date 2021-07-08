# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: releases.py
# Project: models
# Author: Brian Cherinka
# Created: Friday, 2nd April 2021 2:33:07 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Friday, 2nd April 2021 2:33:07 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

from datetime import date
from typing import List, Union
from pydantic import BaseModel, validator

from ..io.loaders import read_yaml, get_yaml_files
from .base import BaseList

class Release(BaseModel):
    """ Pydantic model presenting an SDSS release

    Parameters
    ----------
    name : str
        The name of the release
    description : str
        A description of the release
    public : bool
        Whether the release is public or not
    release_date : `datetime.date`
        The date of the release

    Raises
    ------
    ValueError
        when the release name does not start with a valid SDSS release code
    """
    name: str
    description: str
    public: bool = False
    release_date: Union[str, date] = 'unreleased'

    @validator('name')
    def name_check(cls, value): # pylint: disable=no-self-argument
        if not value.startswith(('WORK', 'DR', 'MPL', 'IPL', 'EDR')):
            raise ValueError('release name must start with WORK, DR, MPL, or IPL.')
        return value
    
class Releases(BaseList):
    """ Pydantic model representing a list of Releases """
    __root__: List[Release]


# construct the SDSS releases
releases = Releases.parse_obj(read_yaml(get_yaml_files('releases'))['releases'])