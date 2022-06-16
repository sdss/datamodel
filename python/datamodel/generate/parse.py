# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: parse.py
# Project: generate
# Author: Brian Cherinka
# Created: Tuesday, 9th February 2021 3:24:33 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Tuesday, 9th February 2021 3:24:33 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import re
from collections import Counter


def get_abstract_path(path: str = None, add_brackets: bool = None) -> str:
    """ Converts a path template into an abstract path

    Converts a path template into an abstract path.  Extracts bracketed keywords
    from a path a template and converts them to named uppercase.
    For example, `MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}CUBE.fits.gz`
    is converted to `MANGA_SPECTRO_REDUX/DRPVER/PLATE/stack/manga-PLATE-IFU-WAVECUBE.fits.gz`.

    Parameters
    ----------
    path : str, optional
        the path template, by default None

    Returns
    -------
    str
        the abstracted path
    """
    if path:
        for delimeter in [("{", "}"), ("@", "|")]:
            search = r"\%s.*?\%s" % delimeter
            for keyword in re.findall(search, path):
                abstract_key = get_abstract_key(
                    key=keyword.replace(delimeter[0], "").replace(delimeter[1], ""),
                    add_brackets=add_brackets
                )
                path = path.replace(keyword, abstract_key)
    return path


def get_abstract_key(key: str = None, add_brackets: bool = None) -> str:
    """ Sanitize the path keyword name

    Sanitizes the path keyword name.  Upper cases the keyword name
    and appends any formatting numbers as an integer to the end of
    name. E.g. "plate:0>5" is converted to "PLATE5".

    Parameters
    ----------
    key : str, optional
        The keywork name, by default None

    Returns
    -------
    str
        the sanitized keyword name
    """
    try:
        if ":" in key:
            key, formats = key.split(":", 1)
            if ">" in formats:
                fmt_int = int(formats.split('>', 1)[-1])
                key = f"{key}{fmt_int}"
        key = key.upper()

        if add_brackets:
            key = f'[{key}]'

    except (ValueError, TypeError) as e:
        print(f"DATAMODEL> {e}")
        key = None
    return key


def get_file_spec(file_spec: str = None) -> str:
    """ Checks validity of file species string

    Checks if the file species name is a valid Python
    identifier.

    Parameters
    ----------
    file_spec : str, optional
        the name of the file species, by default None

    Returns
    -------
    str
        the name of the file species
    """
    # TODO add proper validation for file species name
    if file_spec and not file_spec.replace('-', '').isidentifier():
        print(f"DATAMODEL> invalid file_spec={file_spec}")
        file_spec = None
    return file_spec


def find_kwargs(location: str, example: str) -> dict:
    """ Find and extract keyword arguments

    Attempts to extract keyword argumets from an input
    abstract datamodel path `location` and its `example` path. The location
    and example parts must match exactly.  For example,
    given "{mjd}/sdR-{br}{id}-{frame}.fits.gz" and
    "55049/sdR-b1-00100006.fits.gz", it returns
    {'mjd': '55049', 'br': 'b', 'id': '1', 'frame': '00100006'}

    Parameters
    ----------
    location : str
        a datamodel abstract location
    example : str
        a datamodel example location

    Returns
    -------
    dict
        any extracted keyword arguments
    """

    # get the keyword names from the location
    names = [i.split(":")[0] for i in re.findall("{(.*?)}", location)]

    # replace any "." with "\\." and remove any string formatting
    patt = re.sub(":.*?}", "}", re.sub(r"[.](?!\*)", "\\.", location))

    # replace content between {} with a named capture group matched on pattern .+?
    new_patt = deduplicate(remap_patterns(re.sub("{(.*?)}", r"(?P<\g<1>>.+?)", patt)), names)
    dd = re.search(new_patt, example)
    if dd:
        # if kwargs found, cleanup any duplicate keys
        return cleanup_dups(dd.groupdict())


def deduplicate(value: str, names: list) -> str:
    """ De-duplicate regex pattern field names

    Some paths have duplicate field names, e.g. "run".  The default
    regex named group replace fails with duplicate field names.
    To handle this we append each duplicate field name with "_"
    so the re.groupdict method can work properly.

    Parameters
    ----------
    value : str
        the input regex search pattern
    names : list
        a list of path field names

    Returns
    -------
    str
        the new regex search pattern
    """
    # loop over duplicated names and append dups with "_"
    for term, count in Counter(names).items():
        if count > 1:
            for i in range(count - 1):
                _ = "_" * (1 + i)
                new_term = f"{_}{term.strip('<>')}"
                value = value.replace(f"<{term}>", f"<{new_term}>", 1)
    return value


def remap_patterns(value: str) -> str:
    """ Remaps regex search patterns for certain fields

    Some paths have abutted keywords, i.e. "{br}{id}" or "{dr}{version}".
    The default regex search pattern of ".+?" can sometimes handle these
    but sometimes not. We replace certain fields with specific patterns
    to help the extraction process.

    Parameters
    ----------
    value : str
        the input regex search pattern

    Returns
    -------
    str
        the new regex search pattern
    """
    # for cases with abutted kwargs, e.g. {camrow}{camcol}, {filter}{camcol}, {br}{id}, etc
    mapping = {'<dr>': "DR\\d{1,2}", '<br>': '[br]', '<id>': '.+?', "<camcol>": '[1-6]',
               "<filter>": '[ugriz]'}

    # loop over specific key names
    for i in mapping:
        if i not in value:
            continue
        # replace the pattern with the specific pattern
        value = value.replace(f"{i}.+?", f"{i}{mapping.get(i, '.+?')}")
    return value


def cleanup_dups(kwargs: dict) -> dict:
    """ Cleanup duplicate keys in the extracted keywords

    Removes the duplicated keywords from the extracted kwargs.
    If both key values are the same, uses it.  If both are digits,
    attempts to remove any front zero-padding, e.g. "45", and ""000045" -> "45".

    Parameters
    ----------
    kwargs : dict
        the input extracted keywords

    Returns
    -------
    dict
        reduced keyword dictionary
    """
    newdd = {}
    # loop over the kwargs
    for key, val in kwargs.items():
        # for duplicated keys with "_"
        if key.startswith("_"):
            other_val = kwargs.get(key.lstrip("_"))
            # use key if both are the same; otherise if digits, strip out front zero-padding
            if val == other_val:
                newdd[key.lstrip("_")] = val
            elif val.isdigit() and other_val.isdigit():
                newdd[key.lstrip("_")] = val.lstrip("0")
        elif key.lstrip("_") not in newdd:
            newdd[key] = val
    return newdd