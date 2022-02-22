# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import pytest
from astropy.io import fits
from datamodel.generate import DataModel
from pydantic import ValidationError

def test_datamodel_design(yamlfile):
    assert not os.path.exists(yamlfile)
    dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits', design=True)
    dm.write_stubs()    
    assert os.path.exists(yamlfile)

    ss = dm.get_stub('yaml')
    ss.update_cache()
    assert ss.validate_cache() is False
    assert 'replace me' in ss._cache['general']['short']
    assert ss._cache['general']['releases'] == ['WORK']
    assert 'design' in ss._cache['general'] and ss._cache['general']['design'] is True
    
    rel = ss._cache['releases']['WORK']
    assert rel['example'] is None
    assert len(rel['hdus']) == 1
    assert 'hdu0' in rel['hdus']
    assert rel['hdus']['hdu0']['name'] == 'PRIMARY'


def test_design_hdu(validdesign):
    ss = validdesign.get_stub('yaml')
    ss.update_cache()
    rel = ss._cache['releases']['WORK']
    assert len(rel['hdus']) == 1
    
    validdesign.design_hdu(ext='image', name='TEST_IMAGE', 
                           header=[('NAME', '', 'the name of the test image'), 
                                   ('DATA', '', 'the type of data in the test image')], 
                           description='this is a test image extension')    

    validdesign.design_hdu(ext='table', name='TEST_CATALOG', 
                           columns=[('PARAM1','10A'), ('PARAM2','J'), ('PARAM3','B')], 
                           description='this is a test table extension')

    ss.update_cache()
    rel = ss._cache['releases']['WORK']
    assert len(rel['hdus']) == 3
    assert rel['hdus']['hdu1']['name'] == 'TEST_IMAGE'
    assert rel['hdus']['hdu2']['name'] == 'TEST_CATALOG'
    assert rel['hdus']['hdu2']['description'] == 'this is a test table extension'

def test_design_par(validpardesign):
    ss = validpardesign.get_stub('yaml')
    ss.update_cache()
    rel = ss._cache['releases']['WORK']

    assert rel['par']['comments'] == '#This is designer Yanny par\n#\n#Add comments here\n'
    assert len(rel['par']) == 3
    assert len(rel['par']['header']) == 2
    assert rel['par']['header'][0]['key'] == 'key1'
    assert 'TABLE' in rel['par']['tables']
    assert len(rel["par"]["tables"]["TABLE"]["structure"]) == 1
    assert rel['par']['tables']['TABLE']['structure'][0]['name'] == 'col1'

    validpardesign.design_par(header=("a", "b", "c"), name="TABLE", columns=["c1", "c2", "c3"])
    validpardesign.design_par(header={"d": 1, "e": 2, "f": 3}, name="STUFF", 
                              columns=[("d1", "float[6]"), ("d2", "int"), ("d3", "char[2]")])
    validpardesign.design_par(name="TABLE", columns=[("plateid", "int", "the plate id of the obs")])
    ecol = {"name": "ecol", "description": "a new enum col", "type": "ETYPE", "unit": "", "is_array": False,
            "is_enum": True, "enum_values": ["GO", "NO", "FO", "SO"], "example": "GO"}
    validpardesign.design_par(name="TABLE", columns=[ecol])

    ss.update_cache()
    rel = ss._cache['releases']['WORK']

    assert 'STUFF' in rel['par']['tables']
    assert len(rel['par']['header']) == 6
    assert rel['par']['header'][-1]['key'] == 'f'
    newcol = {'name': 'd3', 'type': 'char[2]', 'description': 'description for d3', 
              'unit': '', 'is_array': False, 'is_enum': False, 'example': 'a'}
    assert newcol in rel['par']["tables"]["STUFF"]["structure"]
    
    # assert plateid column is there
    newcol = {"name": "plateid", "type": "int", 
              "description": "the plate id of the obs", 
              "unit": "", "is_array": False, "is_enum": False, "example": 1}
    assert newcol in rel['par']["tables"]["TABLE"]["structure"]

    # assert the enum column is there
    assert ecol in rel['par']["tables"]["TABLE"]["structure"]


def test_design_generates_file(validdesign):
    assert validdesign.file is None
    validdesign.generate_designed_file(ver='v1', id='A')
    assert os.path.exists(validdesign.file)


def test_design_filegen_failure_invalid(yamlfile):
    dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits', design=True)
    with pytest.raises(ValidationError, match='1 validation error for HDU'):
        dm.generate_designed_file(ver='v1', id='A')

           
def test_design_filegen_failure_nokeys(yamlfile):
    dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits', design=True)
    with pytest.raises(KeyError, match='Must specify path keywords to generate a real file'):
        dm.generate_designed_file()
            
@pytest.fixture()
def fulldesign(validdesign):
    validdesign.design_hdu(ext='image', name='TEST_IMAGE', 
                           header=[('NAME', '', 'the name of the test image'), 
                                   ('DATA', '', 'the type of data in the test image')], 
                           description='this is a test image extension')    

    validdesign.design_hdu(ext='table', name='TEST_CATALOG', 
                           columns=[('PARAM1','10A', 'n/a'), ('PARAM2','J', 'm')], 
                           description='this is a test table extension')

    ss = validdesign.get_stub('yaml')
    ss.update_cache()
    ss._cache['releases']['WORK']['hdus']['hdu2']['columns']['PARAM1']['description'] = 'string column'
    ss._cache['releases']['WORK']['hdus']['hdu2']['columns']['PARAM2']['description'] = 'int32 column'
    ss.write()

    yield validdesign
    
def test_updated_genfile(fulldesign):
    fulldesign.generate_designed_file(ver='v1', id='A')
    assert os.path.exists(fulldesign.file)
    
    hdu = fits.open(fulldesign.file)
    assert len(hdu) == 3
    assert hdu[1].name == 'TEST_IMAGE'
    assert hdu[2].name == 'TEST_CATALOG'

