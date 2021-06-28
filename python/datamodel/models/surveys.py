# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: surveys.py
# Project: models
# Author: Brian Cherinka
# Created: Friday, 7th May 2021 5:01:55 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Friday, 7th May 2021 5:01:55 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import

from typing import List, Union
from pydantic import BaseModel, validator

from ..io.loaders import read_yaml, get_yaml_files
from .base import BaseList


class Phase(BaseModel):
    """ Pydantic model representing an SDSS phase """
    name: str
    id: int
    start: int = None
    end: int = None
    active: bool = False


class Survey(BaseModel):
    """ Pydantic model representing an SDSS survey """
    name: str
    long: str = None
    description: str
    phase: Union[int, Phase] = None

    @validator('phase')
    def get_phase(cls, v):
        if type(v) == Phase:
            return v

        opt = [p for p in phases if p.id==v]
        if not opt:
            raise ValueError(f'Survey phase {v} is not a valid SDSS Phase!')
        return opt[0]

class Surveys(BaseList):
    """ Pydantic model representing a list of Surveys """
    __root__: List[Survey]


class Phases(BaseList):
    """ Pydantic model representing a list of Phases """
    __root__: List[Phase]


# construct the SDSS releases
phases = Phases.parse_obj(read_yaml(get_yaml_files('phases'))['phases'])
surveys = Surveys.parse_obj(read_yaml(get_yaml_files('surveys'))['surveys'])
