# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import abc
import os


def format_bytes(value: int = None) -> str:
    """Convert an integer to human-readable format.

    Parameters
    ----------
    value : int
        An integer representing number of bytes.

    Returns
    -------
    str
        Size of the file in human-readable format.
    """

    try:
        value = int(value)
    except:
        value = 0

    for unit in ("bytes", "KB", "MB", "GB"):
        if value < 1024:
            return "{0:d} {1}".format(int(value), unit)
        else:
            value /= 1024.0

    return "{0:3.1f} {1}".format(value, "TB")


def get_filesize(file) -> str:
    """Get the size of the input file.

    Returns
    -------
    str
        Size of the file in human-readable format.
    """
    return format_bytes(os.path.getsize(file))


def get_filetype(file) -> str:
    """Get the extension of the input file.

    Returns
    -------
    str
        File type in upper case.
    """
    filename, file_extension = os.path.splitext(file)
    if "gz" in file_extension:
        filename, file_extension = os.path.splitext(filename)
    return file_extension[1:].upper()


class BaseFile(abc.ABC):
    suffix = None
    cache_key = None

    def __init__(self, cache: dict, datamodel=None, stub=None, filename=None, release=None, file_species=None,
                 design=None, use_cache_release=None, full_cache=None):
        self._cache = cache
        self._datamodel = datamodel
        self._stub = stub
        self.filename = filename
        self.release = release
        self.file_species = file_species
        self.design = design
        self.use_cache_release = use_cache_release
        self.full_cachce = full_cache

        # check input datamodel or needed kwargs
        if self._datamodel:
            self.filename = self._datamodel.file
            self.release = self._datamodel.release
            self.file_species = self._datamodel.file_species
            self.design = self._datamodel.design
        elif not (filename and release and file_species):
            raise ValueError("Must specify filename, release, file_species if no datamodel is provided.")

        # check input stub or needed kwargs
        if self._stub:
            self.use_cache_release = self._stub.use_cache_release
            self.full_cache = self._stub.full_cache

    def __repr__(self):
        return f'<{self.__class__.__name__}("{self.filename}")>'
    
    def _set_cache(self, force=None):
        # get the cached data
        cached_data = self._cache['releases'][self.release].get(self.cache_key, {})

        # set an empty data cache when in design phase
        if not cached_data and self.design:
            self.design_content()
            return

        # if no cache exists or forced update, generate a new cache from file
        if not cached_data or force:
            cached_data = self._generate_new_cache()

        # updating the data section of the cache
        if self.use_cache_release and not force:
            old_cache = self._cache['releases'][self.use_cache_release].get(self.cache_key, {})
            if not self.full_cache:
                # partial copy of the cache
                cached_data = self._update_partial_cache(cached_data, old_cache)
            else:
                # full copy of the cache
                cached_data = old_cache

        # set the yanny cache to the given release
        self._cache['releases'][self.release][self.cache_key] = cached_data
        

    @abc.abstractmethod        
    def _update_partial_cache(self, cached_data, old_cache):
        pass

    def _use_full_cache(self):
        self._cache['releases'][self.release] = self._cache['releases'].get(self.use_cache_release, {})
               
    @abc.abstractmethod        
    def _generate_new_cache(self):
        pass
    
    @abc.abstractmethod        
    def design_content(self):
        pass

    @staticmethod
    def _nonempty_string(value: str = None) -> str:
        """Jinja2 Filter to map the format value to a string.

        Parameters
        ----------
        value : str?
            Not sure what type this is supposed to have.

        Returns
        -------
        string: str
            The string.
        """
        return f"{value}" if value else 'replace me - with content'


def file_selector(suffix: str = None) -> BaseFile:
    """ Select the correct class given a file suffix """

    for ftype in BaseFile.__subclasses__():
        if suffix and suffix.upper() == ftype.suffix:
            return ftype
