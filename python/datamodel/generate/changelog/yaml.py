
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import absolute_import, division, print_function

import abc
import re
import yaml



class YamlDiff(abc.ABC):
    """ Computes the difference between two releases in YAML cache

    Computes the differences in HDU content between releases in a given
    YAML datamodel file, or cached dictionary.

    Parameters
    ----------
    content : dict, optional
        The yaml cache content for a given datamodel, by default None
    file : str, optional
        A path to a yaml datamodel file, by default None

    Raises
    ------
    ValueError
        when no yaml filepath or cache content is provided
    ValueError
        when no releases can be identified from the yaml content
    """
    suffix = None
    cache_key = None

    def __init__(self, content: dict = None, file: str = None) -> None:
        self.content = content
        self.file = file

        if not self.file and not self.content:
            raise ValueError('Either a yaml filepath or yaml content dict must be specified.')

        if self.file:
            self._read_content()

        # attempt to get the file species name
        self.name = self.content.get('general', {}).get('name', '')

        # get datatype
        self.datatype = self.content.get('general', {}).get('datatype', '')

        if 'releases' in self.content:
            self.releases = self.content['releases']
        elif re.findall(r'WORK|DR\d{1,2}|MPL\d{1,2}|IPL\d{1,2}', ';'.join(self.content.keys())):
            self.releases = self.content
        else:
            raise ValueError('Cannot identify releases dict from input content or file')

    def __repr__(self) -> str:
        return f'<YamlDiff (name="{self.name}")>'

    def _read_content(self) -> None:
        """ Reads the content of YAML file """
        with open(self.file, 'r') as f:
            self.content = yaml.load(f.read(), Loader=yaml.FullLoader)

    def compute_changelog(self, version1: str = 'A', version2: str = 'B', simple: bool = False) -> dict:
        """ Compute the changelog between two releases

        Computes the changes between two releases in a given YAML cache.  Compares the
        "hdus" entries in each release, and looks for differences in HDU extension number,
        added or removed HDU extensions, differences in primary header keyword number, and
        any added or removed primary header keywords.

        Parameters
        ----------
        version1 : str, optional
            The release to check differences against, by default 'A'
        version2 : str, optional
            The release to check differences from, by default 'B'
        simple : bool, optional
            If True, simplfies the changelog entries to only non-null values, by default False

        Returns
        -------
        dict
            a dictionary of found changes

        Raises
        ------
        ValueError
            when no HDULists are found in the YAML cache
        """

        if self.datatype.lower() != self.suffix.lower():
            raise AttributeError(f'Datatype {self.datatype} does not match class suffix {self.suffix}.')

        return self._get_changes(version1, version2, simple=simple)

    @abc.abstractmethod
    def _get_changes(self, version1: str, version2: str, simple: bool = None) -> dict:
        """ Abstract method to be implemented by subclass, for generating changelog content

        This method is used to construct a dictionary of changes between two releases for the
        given file YAML content.  It should return a dictionary object, minimally of the form
        {version1: {"from": version2, "key1": value1, "key2": value2, ...}} where key1: value1, etc are
        the custom changes between the two releases.  The input version1 is the new release, and
        version2 is the older release of which to compute the difference.

        """
        pass

    def clean_empty(self, d: dict) -> dict:
        """ clean up an empty dictionary """
        if isinstance(d, dict):
            return {k: v for k, v in ((k, self.clean_empty(v)) for k, v in d.items()) if v}
        if isinstance(d, list):
            return [v for v in map(self.clean_empty, d) if v]
        return d

    def has_changes(self, version1: str = 'A', version2: str = 'B') -> bool:
        """ Check if there are any changes between two releases

        Computes the changelog between two releases and returns a flag if changes
        are detected.  Compares the differences of release "version1" from release
        "version2".

        Parameters
        ----------
        version1 : str, optional
            The release to check differences against, by default 'A'
        version2 : str, optional
            The release to check differences from, by default 'B'

        Returns
        -------
        bool
            True if any changes detected
        """
        changes = self.compute_changelog(version1=version1, version2=version2, simple=True)
        values = changes[version1]
        return (set(values) - set({"from"})) != set()


    def generate_changelog(self, order: list = None, simple: bool = False) -> dict:
        """ Generate a full changelog dictionary across all releases

        Iterate over all releases and generate a complete changelog from one release
        to another.  The release order to compute the changelog can be specified by passing
        in a desired list of releases to the `order` keyword.  Set `simple` to True to produce
        a cleaner, simpler changelog, containing only non-null entries.

        Parameters
        ----------
        order : list, optional
            The order of releases to generate changelog from, by default None
        simple : bool, optional
            If True, simplfies the changelog entries to only non-null values, by default False

        Returns
        -------
        dict
            A complete changelog dictionary over all releases
        """
        changes = {}

        # build the release order
        rel_list = list(self.releases.keys())
        if order:
            rev_list = [rel_list[rel_list.index(i)] for i in order]
        else:
            rev_list = list(reversed(rel_list))

        zipped_rels = zip(rev_list[:-1], rev_list[1:])
        for item in zipped_rels:
            if self.has_changes(item[0], item[1]):
                changes.update(self.compute_changelog(item[0], item[1], simple=simple))
            else:
                changes.update({item[0]: {'from': item[1], 'note': 'No changes'}})
        return changes


def yamldiff_selector(suffix: str = None) -> YamlDiff:
    """ Select the correct class given a file suffix """

    for ftype in YamlDiff.__subclasses__():
        if suffix and suffix.upper() == ftype.suffix:
            return ftype
