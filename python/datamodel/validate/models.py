# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pathlib
from datamodel.generate import DataModel


def validate_models():
    """ Check YAML datamodel validation

    Checks all YAML datamodels for corresponding validated JSON models.

    Raises
    ------
    ValueError
        when invalidated YAML models are found
    """
    # get or set the datamodel directory
    dmdir = os.getenv("DATAMODEL_DIR")
    if not dmdir:
        dmdir = pathlib.Path(__file__).parent.parent.parent.parent

    # get the list of JSON and YAML datamodels
    jsons = pathlib.Path(dmdir) / "datamodel" / "products" / "json"
    yamls = pathlib.Path(dmdir) / "datamodel" / "products" / "yaml"
    yfiles = yamls.rglob("*.yaml")
    jfiles = list(jsons.rglob("*.json"))

    # look for any YAML datamodels that don't have corresponding JSON models
    invalid = []
    for y in yfiles:
        newy = pathlib.Path(y.as_posix().replace("yaml", "json"))
        if newy not in jfiles:
            invalid.append(y.name)

    # raise error for any not-yet-validated YAML datamodels
    if any(invalid):
        jinv = "\n".join(sorted(invalid))
        raise ValueError(f'The following YAMLs do not yet have validated JSON datamodels:\n{jinv}')


def revalidate(species: str, release: str = None, verbose: bool = None):
    """ Rewrite JSON datamodels

    Rewrites all the datamodel stubs for a given
    existing file species and release.

    Parameters
    ----------
    species : str
        the file species name of a YAML datamodel
    release : str, optional
        the SDSS release, by default None
    verbose : bool, optional
        if True, turn on verbosity, by default None
    """
    dm = DataModel.from_yaml(species=species, release=release, verbose=verbose)
    dm.write_stubs()
