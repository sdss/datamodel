# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
from .releases import releases


def replace_me(value: str) -> str:
    """ Validator for datamodel text fields

    Validator for yaml fields where the string values have the text
    "replace me" within it.  This text indicates a template text that
    must be replaced.

    Parameters
    ----------
    value : str
        the value of the field

    Returns
    -------
    str
        the value of the field

    Raises
    ------
    ValueError
        when "replace me" is the in the value text
    """
    if 'replace me' in value:
        raise ValueError('Generic text needs to be replaced with specific content!')
    return value


def check_release(value: dict) -> str:
    """ Validator for datamodel release keys

    Validator for yaml "releases" fields.  Checks the "releases" keys against
    valid SDSS releases, from the Releases Model.

    Parameters
    ----------
    value : dict
        the value of the field

    Returns
    -------
    str
        the value of the field

    Raises
    ------
    ValueError
        when the release key is not a valid release
    """
    rr = [i.name for i in releases]
    badkeys = set(value.keys()) - set(rr)
    if badkeys:
        raise ValueError(f"Invalid key(s) {','.join(badkeys)} in releases dict.")
    return value
