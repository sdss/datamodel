#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2026-03-03
# @Filename: parquet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import Dict

from .base import BaseFile

try:
    import polars
except ImportError:
    polars: None = None


class ParquetFileType(BaseFile):
    """A file type for Parquet files."""

    suffix = "PARQUET"
    cache_key = "dataframe"

    def __init__(self, *args, **kwargs):
        super(ParquetFileType, self).__init__(*args, **kwargs)

        if not polars:
            raise ImportError("Polars is required to work with Parquet file products.")

        # Read in the Parquet file if not designing one.
        self.dataframe: polars.DataFrame | None = None

        if self._datamodel and not self._datamodel.design:
            self.dataframe = polars.read_parquet(self.filename)

    def _generate_new_cache(self) -> dict:
        """Generate a new cache for Parquet files."""

        columns: Dict[str, Dict] = self._parse_columns()

        return {"columns": columns}

    def _update_partial_cache(self, cached_data: dict, old_cache: dict) -> dict:
        """Update the cache with new data for Parquet files."""

        for colname in cached_data.get("columns", {}):
            old_col_data = old_cache["columns"].get(colname, {})

            if old_description := old_col_data.get("description", ""):
                cached_data["columns"][colname]["description"] = old_description

            if old_unit := old_col_data.get("unit", ""):
                cached_data["columns"][colname]["unit"] = old_unit

        return cached_data

    def _parse_columns(self) -> Dict[str, Dict]:
        """Parse the columns of the Parquet file."""

        assert self.dataframe is not None, "Dataframe is not loaded."

        columns: Dict[str, Dict] = {}

        for column in self.dataframe.columns:
            columns[column] = {
                "name": column,
                "dtype": str(self.dataframe[column].dtype),
                "unit": self._nonempty_string(),
                "description": self._nonempty_string(),
            }

        return columns

    def design_content(self) -> None:
        """Design a new Parquet file product."""

        return

    def write_design(self, file: str, overwrite: bool = False) -> None:
        """Write the design of a Parquet file product to disk."""

        return

    def _get_designed_object(self, data: dict):
        """Get the designed object for a Parquet file product."""

        if not polars:
            raise ImportError("Polars is required to work with Parquet file products.")

        return polars.DataFrame()
