# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import pytest
from pydantic import BaseModel, Field

from datamodel.models.base import CoreModel
from datamodel.models import releases, phases, surveys, tags, vacs, variants
from datamodel.models.releases import Releases, Release
from datamodel.models.surveys import Survey, Phase
from datamodel.models.versions import Tag, Version, Tags
from datamodel.models.vacs import VACS, VAC
from datamodel.models.levels import DataLevel


models = [releases, phases, surveys, tags, vacs]

@pytest.fixture(params=models, ids=["releases", "phases", "surveys", "tags", 'vacs'])
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
                          ('public', 'IPL1')],
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

def test_surveys_list():
    assert 'MaNGA' in surveys
    assert surveys['MaNGA'].name == 'MaNGA'
    assert surveys[3].name == 'MaNGA'
    assert 'manga' in surveys
    assert surveys['MaNGA'] == surveys['MANGA']


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

def test_vac():
    """ test the vac pydantic model """
    assert 'MANGA_GEMA' in vacs
    assert isinstance(vacs, VACS)
    vac = vacs['MANGA_GEMA']
    assert isinstance(vac, VAC)
    assert vac.name == 'MANGA_GEMA'


def test_data_level():
    """ test the data level model """
    d = DataLevel(x=1, y=2, z=3)
    assert d.x.name == 'intermediate'
    assert d.x.value == 1
    assert d.y.name == 'spectra'
    assert d.y.value == 2
    assert (d.z == 3) & isinstance(d.z, int)

    desc = d.describe()
    assert desc == {'product_type': 'intermediate: Intermediate or ancillary pipeline product output during data processing',
                    'product_subtype': 'spectra: A 1d or 2d spectral data product, or a set of spectral data',
                    'product_variant': 'skysub: Post sky subtraction'}


def test_variants():
    """ test the variants model """
    assert 'apo25m' in variants
    vv =  variants['apo25m']
    assert vv.name == 'apo25m'
    assert vv.description == 'Raw data from the APO 2.5m telescope'
    assert vv.x == 0
    assert vv.y == 1
    assert vv.level == 1


def test_repr():
    """ test reduced repr """
    tt = tags['bhm_run2d_v6_0_9']
    assert repr(tt) == "Tag(version='run2d', tag='v6_0_9', release='IPL2')"

    assert "phase=5" in repr(surveys['BHM'])

    tt = tags['mwm_v_astra_0.2.6']
    assert repr(tt) == "Tag(version='v_astra', tag='0.2.6', release='IPL1')"


class C(BaseModel):
    name: str = 'C'
    e: int = 2
    f: str = 'this ia string'

class B(BaseModel):
    name: str = "B"
    c: int = 2
    d: str = 'd'

class A(CoreModel):
    a : int = 1
    b : str = Field('b', repr=False)
    v : B = Field(..., json_schema_extra={'repr_attr':'name'})
    n : C

def test_repr_reduce():
    """ test reduced repr """
    aa = A(v=B(), n=C())
    ra = repr(aa)
    # A(a=1, v='B', n=C(name='C', e=2, f='this ia string'))
    assert "v='B'" in ra
    assert "b='b'" not in ra
    assert "C(name='C', e=2, f='this ia string')" in ra