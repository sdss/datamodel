# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import print_function, division, absolute_import

from collections import defaultdict
from typing import List, Union, Optional
from pydantic import BaseModel, validator

from ..io.loaders import read_yaml, get_yaml_files
from .base import BaseList
from .releases import Release, releases
from .surveys import Survey, surveys



class Version(BaseModel):
    """ Pydantic model representing an SDSS version

    Parameters
    ----------
    name : str
        The name of the software version key
    description : str
        A description of the software key
    """
    name: str
    description: str


class Tag(BaseModel, smart_union=True):
    """ Pydantic model representing an SDSS software tag

    Parameters
    ----------
    version : Version
        The version key
    tag : str
        The version tag number or name
    release : `~datamodel.models.releases.Release`
        The SDSS release the tag is associated with
    survey : `~datamodel.models.surveys.Survey`
        The SDSS survey the tag is associated with

    Raises
    ------
    ValueError
        when the tag release is not a valid SDSS Release
    ValueError
        when the tag survey is not a valid SDSS Survey
    """
    version: Version
    tag: Union[str, list] = None
    release: Union[str, Release, List[Release]]
    survey: Union[str, Survey]

    @validator('release')
    def get_release(cls, v):
        """ check the release is a valid SDSS release """
        if isinstance(v, Release):
            return v

        # return all public releases
        if v == 'all':
            return [i for i in releases if i.public]

        # check release
        if isinstance(v, str):
            # check string release name
            opt = [p for p in releases if p.name==v]
        elif isinstance(v, list):
            # check list of release names
            vv = [i.name for i in v]
            opt = [p for p in releases if p.name in vv]
        if not opt:
            raise ValueError(f'Tag release {v} is not a valid SDSS Release.')
        return opt[0]

    @validator('survey')
    def get_survey(cls, v):
        """ check the survey is a valid SDSS survey """
        if isinstance(v, Survey):
            return v

        opt = [p for p in surveys if p.id==v]
        if not opt:
            raise ValueError(f'Tag survey {v} is not a valid SDSS Survey.')
        return opt[0]

    @property
    def name(self):
        """ A name for the tag """
        return f"{self.survey.id}_{self.version.name}_{self.tag}"


class Tags(BaseList):
    """ Pydantic model representing a list of Tags """
    __root__: List[Tag]

    def group_by(self, order_by: str = 'release') -> dict:
        """ Group tags by SDSS release or survey

        Convert the list of tags to a series of dictionaries,
        ordered by the SDSS release or survey, with key:value pairs
        of version_name:tag. Default is to group by release, then survey.
        With `order_by` set to `survey`, grouped by survey, then release.
        For example, "{'DR17': {'manga': {'drpver': 'v3_1_1', 'dapver': '3.1.0'}}".

        Parameters
        ----------
        order_by : str, optional
            _description_, by default 'release'

        Returns
        -------
        dict
            nested dictionary of tags
        """
        dd = defaultdict(dict)
        for i in self:
            rel = i.release if isinstance(i.release, list) else [i.release]
            if order_by == 'release':
                self._by_release(i, dd, rel)
            elif order_by == 'survey':
                self._by_survey(i, dd, rel)
        return dd

    @staticmethod
    def _by_release(i: Tag, dd: dict, rel: list):
        """ Group tags by SDSS release """
        for r in rel:
            if i.survey.id in dd[r.name]:
                dd[r.name][i.survey.id][i.version.name] = i.tag
            else:
                dd[r.name][i.survey.id] = {i.version.name: i.tag}

    @staticmethod
    def _by_survey(i: Tag, dd: dict, rel: list):
        """ Group tags by SDSS survey """
        for r in rel:
            if r.name in dd[i.survey.id]:
                dd[i.survey.id][r.name][i.version.name] = i.tag
            else:
                dd[i.survey.id][r.name] = {i.version.name: i.tag}


# construct the SDSS tags
tags = Tags.parse_obj(read_yaml(get_yaml_files('versions'))['tags'])
