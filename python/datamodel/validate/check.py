# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import re
import pathlib
from typing import Union

from datamodel import log
from datamodel.products import SDSSDataModel
from tree import Tree


def get_products(release: str = None) -> dict:
    """ Get the access info for all SDSS data products

    Get the access datamodel info for all SDSS data products
    of a given release.  If no release specified, returns
    the info for all products for all releases.

    Parameters
    ----------
    release : str, optional
        The SDSS data release, by default None

    Returns
    -------
    dict
        The datamodel path access information
    """
    dm = SDSSDataModel()
    access = {}
    for pp in dm.products:
        with pp.loader() as prod:
            if not release or release in prod.releases:
                access[prod.name] = prod.get_access(release=release)
    return access


def yield_products(release: str = None) -> tuple:
    """ Generator to yield the access info for all SDSS data products

    Yield the access datamodel info for all SDSS data products
    of a given release.  If no release specified, returns
    the info for all products for all releases.

    Parameters
    ----------
    release : str, optional
        The SDSS data release, by default None

    Returns
    -------
    tuple
        The product name and its datamodel access dictionary

    Yields
    ------
    Iterator[tuple]
        The product name and its datamodel access dictionary
    """
    dm = SDSSDataModel()
    for pp in dm.products:
        with pp.loader() as prod:
            if not prod.releases:
                log.warning(f'Error. No releases found for {prod.name}. Product not properly loaded.')
                continue
            if not release or release in prod.releases:
                yield prod.name, prod.get_access(release=release)


def check_products(release: str = None, verbose: bool = None) -> None:
    """ Validate the data product path information

    Checks the datamodel product access path information against the tree path
    information for consistency.  Checks path name, template, and access_string.

    Parameters
    ----------
    release : str, optional
        The SDSS data release, by default None
    verbose : bool, optional
        If True, turn on verbosity, by default None

    Raises
    ------
    ValueError
        when any of the product paths are invalid against tree
    """

    # if the release is work, check tree cfgs sdss5 -> sdsswork in that order
    if release and verbose:
        log.info(f'Validating product paths in tree for release {release}.')

    # loop over all data products
    invalid = []
    for product, data in yield_products(release=release):
        if not release:
            # if no release, loop over all releases in each product
            for rel, info in data.items():
                log.info(f'Validating product paths in tree for release {rel}.') if verbose else None
                # check for invalid path info
                path = check_invalid(product, info, rel, verbose=verbose)
                if path:
                    invalid.append(path)
        else:
            # check for invalid path info
            path = check_invalid(product, data, release, verbose=verbose)
            if path:
                invalid.append(path)

    # raise error if any invalid paths found
    if any(invalid):
        jinv = "\n".join(f"{i}: {v}" for i, v in invalid)
        raise ValueError(f'The following products have invalid tree paths:\n{jinv}')

    # log if valid
    if verbose:
        log.info('All products paths are successfully validated.')


def check_invalid(product: str, data: dict, release: str, verbose: bool = None) -> Union[tuple, None]:
    """ Check for an invalid product access path

    For a given release, checks the datamodel product access info against the relevant
    Tree configuration path info for consistency. If the release is "WORK", checks both
    the "sdss5" and "sdsswork" configs.  If both configs return an invalidation, then the
    product path is invalid.

    Parameters
    ----------
    product : str
        The name of the datamodel product, i.e. file species name
    data : dict
        The datamodel access info dictionary
    release : str, optional
        The SDSS data release, by default None
    verbose : bool, optional
        If True, turn on verbosity, by default None

    Returns
    -------
    Union[tuple, None]
        Either None for a valid path or a tuple of the invalid path info
    """
    # for WORK release check against both sdss5 and sdsswork
    if release == 'WORK':
        path5 = check_path(product, data, Tree('sdss5'), verbose=verbose)
        pathwork = check_path(product, data, Tree('sdsswork'), verbose=verbose)
        # if both are invalid then the product path is really invalid
        if all([path5, pathwork]):
            return path5[0], f'{path5[1]}; {pathwork[1]}'
    else:
        # check for all other releases
        path = check_path(product, data, Tree(release.lower()), verbose=verbose)
        if path:
            return path


def check_path(product: str, data: dict, tree: Tree, verbose: bool = None) -> Union[tuple, None]:
    """ Checks a product access path

    Checks the product access path name is in the list of tree paths.  Checks the product access
    path template is the same as the tree path template.  Checks the product access access_string
    is consistent with the tree path template.  For tree paths that start with a special function
    rather than an environment variable, e.g. @spectrodir|, only checks the common
    part of the path.

    Parameters
    ----------
    product : str
        The name of the datamodel product, i.e. file species name
    data : dict
        The datamodel access info dictionary
    tree : Tree, optional
        The SDSS tree config
    verbose : bool, optional
        If True, turn on verbosity, by default None

    Returns
    -------
    Union[tuple, None]
        None for a valid path or a tuple of the invalid path info
    """
    # do nothing if no data dict
    if not data:
        return

    # do nothing if product does not exist in sdss_access
    if not data['in_sdss_access']:
        return

    # check if path name is in the tree paths
    if data['path_name'] not in tree.paths:
        msg = f"path name {data['path_name']} not found in {tree.config_name} tree."
        if verbose:
            log.error(msg)
        return (product, msg)

    # check if the path template is correct in tree paths
    if data['path_template'] != tree.paths[data['path_name']]:
        msg = f"product path template {data['path_template']} does not match {tree.config_name} tree path template {tree.paths[data['path_name']]}"
        if verbose:
            log.error(msg)
        return (product, msg)

    # check if the access_string matches the tree path template
    path_template = data.get("access_string").replace(" = ", "=").split('=')[-1]

    # get tree path and remove any special key formatting, e.g. {plateid:0>4} -> {plateid}
    tree_path = tree.paths[data["path_name"]]
    tree_path = re.sub(r':.*?}', "}", tree_path)

    # check if the tree path starts with a special function symbol @
    special_fxn = tree_path.startswith("@")
    msg = f"product access key {path_template} does not match {tree.config_name} tree path template {tree_path}."

    # check case of normal path template
    if not special_fxn and (not compare_path(path_template, tree_path)):
        if verbose:
            log.error(msg)
        return (product, msg)

    # check case when path template starts with a special function, e.g. @spectrodir|
    # only compare path part that isn't the envvar/specialfxn name
    if special_fxn and (not compare_path(path_template.split("/", 1)[-1], tree_path.split("/", 1)[-1])):
        if verbose:
            log.error(msg)
        return (product, msg)


def compare_path(a: str, b: str) -> bool:
    """ Compares two paths

    Compares two paths for equality.  Tries to account for comparison
    between a path with and without compression suffixes,
    i.e. "fits" and "fits.gz".  Strips the last suffix from paths with
    more than one.

    Parameters
    ----------
    a : str
        a str filepath or path location
    b : str
        a str filepath or path location

    Returns
    -------
    bool
        If the two paths are the same
    """
    a = pathlib.Path(a)
    a = a.parent / (a.stem if len(a.suffixes) > 1 else a.name)

    b = pathlib.Path(b)
    b = b.parent / (b.stem if len(b.suffixes) > 1 else b.name)

    return a == b








