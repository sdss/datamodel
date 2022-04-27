# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import pytest
from astropy.io import fits
from datamodel.generate import DataModel
from pydantic import ValidationError

def test_datamodel_design(yamlfile):
    """ test we can design a new fits file """
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


def test_design_hdu(designedfits):
    """ test we can design an HDU in python """
    ss = designedfits.get_stub('yaml')
    ss.update_cache()
    rel = ss._cache['releases']['WORK']
    assert len(rel['hdus']) == 1

    designedfits.design_hdu(ext='image', name='TEST_IMAGE',
                           header=[('NAME', '', 'the name of the test image'),
                                   ('DATA', '', 'the type of data in the test image')],
                           description='this is a test image extension')

    designedfits.design_hdu(ext='table', name='TEST_CATALOG',
                           columns=[('PARAM1','10A'), ('PARAM2','J'), ('PARAM3','B')],
                           description='this is a test table extension')

    ss.update_cache()
    rel = ss._cache['releases']['WORK']
    assert len(rel['hdus']) == 3
    assert rel['hdus']['hdu1']['name'] == 'TEST_IMAGE'
    assert rel['hdus']['hdu2']['name'] == 'TEST_CATALOG'
    assert rel['hdus']['hdu2']['description'] == 'this is a test table extension'

def test_design_par(validdesign):
    """ test we can design an Yanny par section in python """
    vd = validdesign('par')
    ss = vd.get_stub('yaml')
    ss.update_cache()
    rel = ss._cache['releases']['WORK']

    assert rel['par']['comments'] == '#This is designer Yanny par\n#\n#Add comments here\n'
    assert len(rel['par']) == 3
    assert len(rel['par']['header']) == 2
    assert rel['par']['header'][0]['key'] == 'key1'
    assert 'TABLE' in rel['par']['tables']
    assert len(rel["par"]["tables"]["TABLE"]["structure"]) == 1
    assert rel['par']['tables']['TABLE']['structure'][0]['name'] == 'col1'

    vd.design_par(header=("a", "b", "c"), name="TABLE", columns=["c1", "c2", "c3"])
    vd.design_par(header={"d": 1, "e": 2, "f": 3}, name="STUFF",
                              columns=[("d1", "float[6]"), ("d2", "int"), ("d3", "char[2]")])
    vd.design_par(name="TABLE", columns=[("plateid", "int", "the plate id of the obs")])
    ecol = {"name": "ecol", "description": "a new enum col", "type": "ETYPE", "unit": "", "is_array": False,
            "is_enum": True, "enum_values": ["GO", "NO", "FO", "SO"], "example": "GO"}
    vd.design_par(name="TABLE", columns=[ecol])

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


def test_design_hdf(validdesign):
    """ test we can design a hdfs section in python """
    vd = validdesign('h5')
    ss = vd.get_stub('yaml')
    ss.update_cache()
    rel = ss._cache['releases']['WORK']

    assert rel['hdfs']['name'] == '/'
    assert rel['hdfs']['description'] == 'a parent group description'
    assert rel['hdfs']['object'] == 'group'
    assert rel['hdfs']['n_members'] == 0
    assert rel['hdfs']['members'] == {}
    assert rel['hdfs']['attrs'] == []

    # design some stuff
    vd.design_hdf(name="/", attrs=[("foo", "bar", "a new way", "S3")])
    vd.design_hdf( name="data", description="this is a data group",
                  attrs=[("name", 1, "this is a name", "<i8")])
    vd.design_hdf(name="data/stuff", description="this is a data dataset", hdftype="dataset",
                  ds_shape=(100,), ds_dtype="S5")
    vd.design_hdf(name="defaults", description="this is a default dataset", hdftype="dataset",
                  ds_shape=(10, 20), ds_dtype="int32")

    ss.update_cache()
    rel = ss._cache['releases']['WORK']

    # reassert
    assert rel['hdfs']['n_members'] == 2
    assert len(rel['hdfs']['members']) == 3
    assert rel['hdfs']['attrs'] == [{"key": "foo", "value": "bar", "comment": "a new way", "dtype": "S3"}]
    assert 'data/stuff' in rel['hdfs']['members']
    assert rel['hdfs']['members']['data']['n_members'] == 1
    assert rel['hdfs']['members']['defaults'] == {"name": "defaults", "parent": "/", "object": "dataset",
                                                 "description": "this is a default dataset", "attrs": [],
                                                 "shape": (10, 20), "size": 200, "dtype": "int32", "ndim": 2}

def test_design_generates_file(validdesign):
    """ test we can generate a designed file """
    vd = validdesign('fits')
    assert vd.file is None
    vd.generate_designed_file(ver='v1', id='A')
    assert os.path.exists(vd.file)


def test_design_filegen_failure_invalid(yamlfile):
    """ test it fails if we don't have a valid file """
    dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits', design=True)
    with pytest.raises(ValidationError, match='1 validation error for HDU'):
        dm.generate_designed_file(ver='v1', id='A')

def test_design_filegen_failure_nokeys(yamlfile):
    """ test if fails if we don't have keyword args """
    dm = DataModel(file_spec='test', path='TEST_REDUX/{ver}/testfile_{id}.fits', design=True)
    with pytest.raises(KeyError, match='Must specify path keywords to generate a real file'):
        dm.generate_designed_file()

@pytest.fixture()
def fulldesign(designedfits):
    """ fixture to create a fully desisgned FITS file """
    designedfits.design_hdu(ext='image', name='TEST_IMAGE',
                           header=[('NAME', '', 'the name of the test image'),
                                   ('DATA', '', 'the type of data in the test image')],
                           description='this is a test image extension')

    designedfits.design_hdu(ext='table', name='TEST_CATALOG',
                           columns=[('PARAM1','10A', 'n/a'), ('PARAM2','J', 'm')],
                           description='this is a test table extension')

    ss = designedfits.get_stub('yaml')
    ss.update_cache()
    ss._cache['releases']['WORK']['hdus']['hdu2']['columns']['PARAM1']['description'] = 'string column'
    ss._cache['releases']['WORK']['hdus']['hdu2']['columns']['PARAM2']['description'] = 'int32 column'
    ss.write()

    yield designedfits

def test_updated_genfile(fulldesign):
    """ test we can update the designed file on disk """
    fulldesign.generate_designed_file(ver='v1', id='A')
    assert os.path.exists(fulldesign.file)

    hdu = fits.open(fulldesign.file)
    assert len(hdu) == 3
    assert hdu[1].name == 'TEST_IMAGE'
    assert hdu[2].name == 'TEST_CATALOG'

