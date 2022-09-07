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
    """ Pydantic model representing an SDSS phase

    Parameters
    ----------
    name : str
        The name of the phase
    id : int
        The id of the phase
    start : int
        The year the phase started
    end : int
        The year the phase ended
    active : bool
        Whether the phase is currently active
    """
    name: str
    id: int
    start: int = None
    end: int = None
    active: bool = False


class Survey(BaseModel, smart_union=True):
    """ Pydantic model representing an SDSS survey

    Parameters
    ----------
    name : str
        The short name of the survey
    long : str
        The full name of the survey
    description : str
        A description of the survey
    phase : `.Phase`
        The main phase the survey was in
    id : str
        An internal reference id for the survey

    Raises
    ------
    ValueError
        when the survey phase is not a valid SDSS Phase
    """
    name: str
    long: str = None
    description: str
    phase: Union[int, Phase] = None
    id : str = None
    aliases: list = []

    @validator('phase')
    def get_phase(cls, v):
        """ check the phase is a valid SDSS phase """
        if isinstance(v, Phase):
            return v

        pid = v if isinstance(v, int) else v['id'] if isinstance(v, dict) else None
        opt = [p for p in phases if p.id==pid]
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
