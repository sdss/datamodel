# encoding: utf-8

from sdsstools import get_config, get_logger, get_package_version
from re import findall

# pip package name
NAME = "sdss-datamodel"

# Loads config. config name is the package name.
config = get_config("datamodel")

# Inits the logging system as NAME. Only shell logging, and exception and warning catching.
# File logging can be started by calling log.start_file_logger(path).  Filename can be different
# than NAME.
log = get_logger(NAME)


# package name should be pip package name
__version__ = get_package_version(path=__file__, package_name=NAME)


def get_abstract_path(path=None):
    if path:
        for delimeter in [("{", "}"), ("@", "|")]:
            search = r"\%s.*?\%s" % delimeter
            for keyword in findall(search, path):
                abstract_key = get_abstract_key(
                    key=keyword.replace(delimeter[0], "").replace(delimeter[1], "")
                )
                path = path.replace(keyword, abstract_key)
    return path


def get_abstract_key(key=None):
    try:
        if ":" in key:
            key, formats = key.split(":", 1)
            if ">" in formats:
                key = "%s%r" % (key, int(formats.split(">", 1)[-1]))
        key = key.upper()
    except Exception as e:
        print("DATAMODEL> %r" % e)
        key = None
    return key


def get_file_spec(file_spec=None):
    if file_spec and not file_spec.isidentifier():
        print("DATAMODEL> invalid file_spec=%r" % file_spec)
        file_spec = None
    return file_spec
