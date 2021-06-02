# encoding: utf-8

import os
import pathlib
from sdsstools import get_config, get_logger, get_package_version

# pip package name
NAME = "sdss-datamodel"

# Loads config. config name is the package name.
config = get_config("datamodel")

# Inits the logging system as NAME. Only shell logging, and exception and warning catching.
# File logging can be started by calling log.start_file_logger(path).  Filename can be different
# than NAME.
log = get_logger(NAME)

# determine DATAMODEL_DIR
dmdir = os.getenv("DATAMODEL_DIR")
if not dmdir:
    path = pathlib.Path(__file__).parent
    if path.match('site-packages/datamodel'):
        # conda environment
        os.environ['DATAMODEL_DIR'] = str(path)
    elif path.match('datamodel/python/datamodel'):
        # github checkout
        os.environ['DATAMODEL_DIR'] = str(path.parent.parent)


# package name should be pip package name
__version__ = get_package_version(path=__file__, package_name=NAME)

