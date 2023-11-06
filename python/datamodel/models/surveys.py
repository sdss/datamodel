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

from typing import List, Union, Optional
from pydantic import field_validator, Field, RootModel

from ..io.loaders import read_yaml, get_yaml_files
from .base import BaseList, CoreModel


class Phase(CoreModel):
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
    start: Optional[int] = Field(None, repr=False)
    end: Optional[int] = Field(None, repr=False)
    active: bool = False


class Survey(CoreModel):
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
    long: str = Field(None, repr=False)
    description: str = Field(..., repr=False)
    phase: Union[int, Phase] = Field(None, json_schema_extra={'repr_attr':'id'})
    id: str = None
    aliases: list = Field([], repr=False)

    @field_validator('phase')
    @classmethod
    def get_phase(cls, v):
        """ check the phase is a valid SDSS phase """
        if isinstance(v, Phase):
            return v

        pid = v if isinstance(v, int) else v['id'] if isinstance(v, dict) else None
        opt = [p for p in phases if p.id == pid]
        if not opt:
            raise ValueError(f'Survey phase {v} is not a valid SDSS Phase!')
        return opt[0]


class Surveys(BaseList, RootModel[List[Survey]]):
    """ Pydantic model representing a list of Surveys """
    #__root__: List[Survey]


class Phases(BaseList, RootModel[List[Phase]]):
    """ Pydantic model representing a list of Phases """
    #__root__: List[Phase]


# construct the SDSS releases
phases = Phases.model_validate(read_yaml(get_yaml_files('phases'))['phases'])
surveys = Surveys.model_validate(read_yaml(get_yaml_files('surveys'))['surveys'])
