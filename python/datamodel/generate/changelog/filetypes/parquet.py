#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2026-03-06
# @Filename: parquet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import absolute_import, annotations, division, print_function

from datamodel.generate.changelog.yaml import YamlDiff

__all__ = ["YamlParquet"]


class YamlParquet(YamlDiff):
    """Class for supporting YAML changelog generation for Parquet files."""

    suffix = "PARQUET"
    cache_key = "dataframe"

    def _get_changes(self, version1: str, version2: str, simple: bool = False) -> dict:
        """Changelog computer for Parques files.

        Parameters
        ----------
        version1 : str
            The newer version for which to compute changes.
        version2 : str
            The older version against which to compare.
        simple : bool, optional
            If True, simplifies the changelog entries to only non-null values, by default False.

        Returns
        -------
        dict
            A dictionary of found changes.

        """

        parquet_1 = self.releases.get(version1, {}).get("dataframe", {})
        parquet_2 = self.releases.get(version2, {}).get("dataframe", {})

        if not parquet_1 or not parquet_2:
            raise ValueError("No dataframe object found for input versions.")

        columns_1 = set(parquet_1.get("columns", {}).keys())
        columns_2 = set(parquet_2.get("columns", {}).keys())

        # Find added and removed columns
        added_columns = columns_1 - columns_2
        removed_columns = columns_2 - columns_1
        delta_ncolumns = abs(len(columns_1) - len(columns_2))

        # Find added and removed metadata entries
        metadata_1 = set(parquet_1.get("metadata", {}).keys())
        metadata_2 = set(parquet_2.get("metadata", {}).keys())

        added_metadata = metadata_1 - metadata_2
        removed_metadata = metadata_2 - metadata_1
        delta_nmetadata = abs(len(metadata_1) - len(metadata_2))

        changes = {
            version1: {
                "from": version2,
                "delta_ncolumns": delta_ncolumns,
                "delta_nmetadata": delta_nmetadata,
                "added_columns": list(added_columns),
                "removed_columns": list(removed_columns),
                "added_metadata": list(added_metadata),
                "removed_metadata": list(removed_metadata),
            }
        }

        # Return only entries that are not null
        if simple:
            changes[version1] = self.clean_empty(changes[version1])

        return changes
