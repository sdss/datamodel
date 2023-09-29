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
    # set of compressions to check for
    compressions = {'.gz', '.bz2', '.fz', '.zip'}

    filename, file_extension = os.path.splitext(file)
    if file_extension in compressions:
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
    aliases = []
    cache_key = None
    compressions = ['.gz', '.bz2', '.zip']

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

        # set default designed object
        self._designed_object = None

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

    @abc.abstractmethod
    def _update_partial_cache(self, cached_data: dict, old_cache: dict) -> dict:
        """ Abstract method to be implemented by subclass, for partially updating cache content

        This method updates the descriptions or comments of the new cached_data with the human-edited
        fields from the old_cache data.  Used when adding a new release to a datamodel and retaining the old
        descriptions from the previous release.  This method should return the cached_data object.

        Parameters
        ----------
        cached_data : dict
            The YAML cache for a the current release
        old_cache : dict
            The YAML cache for a previous release
        """

    def _use_full_cache(self):
        """ Default method for using the entire cache of a previous release

        This method is used when copying the entire datamodel cache of a previous release, for cases
        when the datamodel for a new release is exactly the same as a prior release.  In most case, this
        method does not need to be overridden.
        """
        self._cache['releases'][self.release] = self._cache['releases'].get(self.use_cache_release, {})

    @abc.abstractmethod
    def design_content(self):
        """ Abstract method to be implemented by subclass, for designing file content

        This method is used to design new content for a YAML datamodel cache for new files
        from within Python.  It should ultimately update the cache line
        self._cache['releases']['WORK'][self.cache_key] = [updated_cache_content]
        with the new content.  This method is called by the DataModel's global design_content method.
        """

    def create_from_cache(self, release: str = 'WORK'):
        """ Create a file object from the yaml cache

        Converts the cache_key dictionary entry in the YAML cache into
        a file object.

        Parameters
        ----------
        release : str, optional
            the name of the data release, by default 'WORK'

        Returns
        -------
        object
            a valid file object

        Raises
        ------
        ValueError
            when the release is not in the cache
        ValueError
            when the release is not WORK when in the datamodel design phase
        """
        if release not in self._cache['releases']:
            raise ValueError(f'Release {release} not found in list of cached releases.')

        if self.design and release != 'WORK':
            raise ValueError(f'Release {release} can only be "WORK" when in the datamodel design phase.')

        data = self._cache['releases'][release][self.cache_key]
        self._designed_object = self._get_designed_object(data)
        return self._designed_object

    @staticmethod
    @abc.abstractmethod
    def _get_designed_object(data: dict):
        """ Abstract static method to be implemented by subclass, for creating a valid object from cache

        This method is used to create a data object from a designed YAML cache content.  It should return
        a new designed object.  Ideally the object should be created through the Pydantic model's
        parse_obj to ensure proper validation and field type coercion.  This method is called
        by create_from_cache which sets the object as the self._designed_object attribute.

        Parameters
        ----------
        data : dict
            The YAML cache value for the ``cache_key`` field
        """

    @abc.abstractmethod
    def write_design(self, file: str, overwrite: bool = None):
        """ Abstract method to be implemented by subclass, for writing a design to a file

        This method is used to write out the designed data object.  It should call the
        self.designed_object's particular method for writing itself to a file,
        specific to that filetype.

        Parameters
        ----------
        file : str
            The datamodel filename to write to
        overwrite : bool
            Flag to overwrite the file if it exists, by default None
        """

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


def get_supported_filetypes() -> list:
    """ Get a list of supported filetypes

    Constructs a list of supported filetypes for datamodels,
    based on the BaseFile subclasses.  Collects each subclass
    file suffix attribute as well as any designated aliases.

    Returns
    -------
    list
        A list of supported file types
    """
    s = []
    for ftype in BaseFile.__subclasses__():
        s.append(ftype.suffix)
        s.extend(ftype.aliases)
    return list(map(str.lower, map(lambda x: f".{x}", s)))
