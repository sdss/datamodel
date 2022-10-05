# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import print_function, division, absolute_import

from typing import List
from pydantic import BaseModel

from ..io.loaders import read_yaml, get_yaml_files
from .base import BaseList


class VAC(BaseModel):
    """ Pydantic model presenting an SDSS VAC

    Parameters
    ----------
    name : str
        The environment variable label name of the VAC

    Raises
    ------
    ValueError
        when the release name does not start with a valid SDSS release code
    """
    name: str


class VACS(BaseList):
    """ Pydantic model representing a list of VACs """
    __root__: List[VAC]


# construct the SDSS releases
vacs = VACS.parse_obj(read_yaml(get_yaml_files('vacs'))['vacs'])