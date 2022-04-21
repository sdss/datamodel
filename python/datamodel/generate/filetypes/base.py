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
    """ Base class for supported datamodel file types

    This is the abstract base class used for defining new file types to be supported
    by the sdss datamodel product.

    Parameters
    ----------
    cache : dict
        The initial yaml cache to be populated.
    datamodel : DataModel, optional
        an SDSS datamodel for the file, by default None
    stub : Stub, optional
        an datamodel Stub for the file, by default None
    filename : str, optional
        the name of file, by default None
    release : str, optional
        the data release, by default None
    file_species : str, optional
        the file species name, by default None
    design : bool, optional
        whether the datamodel is in design mode, by default None
    use_cache_release : str, optional
        the release to pull existing cache from, by default None
    full_cache : bool, optional
        whether to use the entire previous cache, by default None

    Raises
    ------
    ValueError
        when datamodel is not provided when (filename, release, file_species) are not provided.
    """
    suffix = None
    cache_key = None

    def __init__(self, cache: dict, datamodel=None, stub=None, filename: str = None,
                 release: str = None, file_species: str = None, design: bool = None,
                 use_cache_release: str = None, full_cache: bool = None):
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
        """ Default method for setting new cache content based on the type of file """

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
    def _generate_new_cache(self) -> dict:
        """ Abstract method to be implemented by subclass, for generating new cache content

        This method is used to generate the file content for new datamodel YAML files.  It
        should return a dictionary to be stored as the value of the cache key.
        """
        pass

    @abc.abstractmethod
    def _update_partial_cache(self, cached_data: dict, old_cache: dict) -> dict:
        """ Abstract method to be implemented by subclass, for partially updating cache content

        This method updates the descriptions or comments of the new cached_data with the human-edited
        fields from the old_cache data.  Used when adding a new release to a datamodel and retaining the old
        descriptions from the previous release.  This method should return the cached_data object.
        """
        pass

    def _use_full_cache(self):
        """ Default method for using the entire cache of a previous release

        This method is used when copying the entire datamodel cache of a previous release, for cases
        when the datamodel for a new release is exactly the same as a prior release.  In most case, this
        method does not need to be overridden.
        """
        self._cache['releases'][self.release] = self._cache['releases'].get(self.use_cache_release, {})

    @abc.abstractmethod
    def design_content(self):
        """ Abstract method to be implemented by subclass, for designing file content """
        pass

    @abc.abstractmethod
    def create_from_cache(self, release: str = 'WORK'):
        """ Abstract method to be implemented by subclass, for creating a valid object from cache """
        pass

    @abc.abstractmethod
    def write_design(self, file: str, overwrite: bool = None):
        """ Abstract method to be implemented by subclass, for writing a design to a file """
        pass

    @staticmethod
    def _nonempty_string(value: str = None) -> str:
        """Jinja2 Filter to map the format value to a string.

        Parameters
        ----------
        value : str
            The non-null value to check

        Returns
        -------
        string: str
            The string.
        """
        return f"{value}" if value else 'replace me - with content'


def file_selector(suffix: str = None) -> BaseFile:
    """ Selects the correct File class given a file suffix """

    for ftype in BaseFile.__subclasses__():
        if suffix and suffix.upper() == ftype.suffix:
            return ftype
