# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import pytest

from datamodel.models import releases, phases, surveys, tags
from datamodel.models.releases import Releases, Release
from datamodel.models.surveys import Survey, Phase
from datamodel.models.versions import Tag, Version, Tags

models = [releases, phases, surveys, tags]

@pytest.fixture(params=models, ids=["releases", "phases", "surveys", "tags"])
def model(request):
    return request.param


def test_release():
    """ test release model """
    assert isinstance(releases, Releases)
    assert isinstance(releases[0], Release)
    assert 'DR15' in releases
    rel = releases["MPL10"]
    assert rel.name == "MPL10"


def test_list_names(model):
    """ test we can list names """
    tmp = model.list_names()
    assert isinstance(tmp, list)
    assert isinstance(tmp[0], str)

@pytest.mark.parametrize('name, exp',
                         [('release_date', 'EDR'),
                          ('name', 'DR1'),
                          ('public', 'MPL1')],
                         ids=['date', 'name', 'public'])
def test_sort(name, exp):
    """ test we can sort model lists """
    releases.sort(name)
    rel = releases[0]
    assert rel.name == exp


def test_survey():
    """ test the survey model """
    s = surveys["MWM"]
    assert s.name == "MWM"
    assert s.long == "Milky Way Mapper"
    assert isinstance(s, Survey)
    assert isinstance(s.phase, Phase)
    assert s.phase.id == 5
    assert s.phase.name == 'Phase-V'


def test_tags():
    """ test the tag model """
    assert isinstance(tags, Tags)
    tag = tags["manga_drpver_v3_1_1"]
    assert isinstance(tag, Tag)
    assert isinstance(tag.version, Version)
    assert isinstance(tag.release, Release)
    assert isinstance(tag.survey, Survey)
    assert tag.name == "manga_drpver_v3_1_1"
    assert tag.tag == "v3_1_1"
    assert tag.survey.id == "manga"
    assert tag.version.name == "drpver"

def test_tag_groupby_release():
    """ test tag groupby release """
    tmp = tags.group_by()
    assert isinstance(tmp, dict)
    assert 'DR17' in tmp
    assert 'manga' in tmp['DR17']
    assert tmp['DR17']['manga'] == {'drpver': 'v3_1_1', 'dapver': '3.1.0'}

def test_tag_groupby_survey():
    """ test tag groupby survey """
    tmp = tags.group_by('survey')
    assert isinstance(tmp, dict)
    assert 'DR17' not in tmp
    assert 'manga' in tmp
    assert 'DR17' in tmp['manga']
    assert tmp['manga']['DR17'] == {'drpver': 'v3_1_1', 'dapver': '3.1.0'}


