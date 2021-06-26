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

from typing import List
from pydantic import BaseModel, validator

from ..io.loaders import read_yaml, get_yaml_files


class Release(BaseModel):
    """ Pydantic model presenting an SDSS release """
    name: str
    description: str
    public: bool = False

    @validator('name')
    def name_check(cls, value): # pylint: disable=no-self-argument
        if not value.startswith(('WORK', 'DR', 'MPL', 'IPL')):
            raise ValueError('release name must start with WORK, DR, MPL, or IPL.')
        return value


class BaseList(BaseModel):
    """ Base pydantic class for lists of models """

    def __iter__(self):
        return iter(self.__root__)

    def __contains__(self, value):
        if isinstance(value, str):
            return value in [i.name for i in self]
        return value in self

    def __getitem__(self, item):
        if isinstance(item, str) and item in self:
            vals = [i.name for i in self.__root__]
            return self.__root__[vals.index(item)]
        return self.__root__[item]

    def __repr__(self):
        val = '\n '.join(repr(i) for i in self)
        return f"[{val}]"

    def __str__(self):
        return f"[{', '.join([i.name for i in self])}]"
    
    def __len__(self):
        return len(self.__root__)


class Releases(BaseList):
    """ Pydantic model representing a list of Releases """
    __root__: List[Release]


# construct the SDSS releases
releases = Releases.parse_obj(read_yaml(get_yaml_files('releases'))['releases'])