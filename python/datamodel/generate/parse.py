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
    if file_spec and not file_spec.replace('-','').isidentifier():
        print(f"DATAMODEL> invalid file_spec={file_spec}")
        file_spec = None
    return file_spec
