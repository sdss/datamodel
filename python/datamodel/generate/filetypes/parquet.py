#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2026-03-03
# @Filename: parquet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Dict, Union

from datamodel.generate.filetypes.base import BaseFile
from datamodel.models.filetypes.parquet import DataFrame as DataFrameModel

try:
    import polars
except ImportError:
    polars: None = None


if TYPE_CHECKING and polars:
    DataFrameType = polars.DataFrame


__all__ = ["ParquetFileType"]


class ParquetFileType(BaseFile):
    """A file type for Parquet files."""

    suffix = "PARQUET"
    cache_key = "dataframe"

    def __init__(self, *args, **kwargs):
        super(ParquetFileType, self).__init__(*args, **kwargs)

        self._designed_object: Union[DataFrameType, None] = None

        if not polars:
            raise ImportError("Polars is required to work with Parquet file products.")

        # Read in the Parquet file if not designing one.
        self.dataframe: Union[DataFrameType, None] = None

        if self._datamodel and not self._datamodel.design:
            self.dataframe = polars.read_parquet(self.filename)

    def _generate_new_cache(self) -> dict:
        """Generate a new cache for Parquet files."""

        assert polars, "Polars is required to work with Parquet file products."

        columns: Dict[str, Dict] = self._parse_columns()

        metadata: Dict[str, str] = polars.read_parquet_metadata(self.filename)

        # Delete some keys that are added by Pandas or are
        # part of the Parquet file specification.
        for key in ["pandas", "ARROW:schema"]:
            if key in metadata:
                metadata.pop(key)

        return {
            "columns": columns,
            "metadata": {
                key: {"key": key, "description": self._nonempty_string()}
                for key in metadata
            },
        }

    def _update_partial_cache(self, cached_data: dict, old_cache: dict) -> dict:
        """Update the cache with new data for Parquet files."""

        for colname in cached_data.get("columns", {}):
            old_col_data = old_cache["columns"].get(colname, {})

            if old_description := old_col_data.get("description", ""):
                cached_data["columns"][colname]["description"] = old_description

            if old_unit := old_col_data.get("unit", ""):
                cached_data["columns"][colname]["unit"] = old_unit

        for key in cached_data.get("metadata", {}):
            old_key_data = old_cache["metadata"].get(key, {})
            if old_description := old_key_data.get("description", ""):
                cached_data["metadata"][key]["description"] = old_description

        return cached_data

    def _parse_columns(
        self,
        df: Union[DataFrameType, None] = None,
        get_value: bool = False,
    ) -> Dict[str, Dict]:
        """Parse the columns of the Parquet file."""

        df = df or self.dataframe
        assert df is not None, "Dataframe is not loaded."

        columns: Dict[str, Dict] = {}

        row0 = df.row(0) if len(df) > 0 else None

        for column in df.columns:
            columns[column] = {
                "name": column,
                "dtype": str(df[column].dtype),
                "unit": self._nonempty_string(),
                "description": self._nonempty_string(),
                "value": row0[df.columns.index(column)] if row0 else None,
            }

            if not get_value:
                columns[column].pop("value")

        return columns

    def design_content(
        self,
        dataframe: Union[DataFrameType, None] = None,
        columns: Union[Dict[str, Dict], None] = {},
        metadata: Union[Dict[str, str], None] = {},
        **kwargs,
    ) -> None:
        """Design a new Parquet file product.

        Parameters
        ----------
        dataframe: DataFrame, optional
            A Polars DataFrame to use as the design for the Parquet file product. If
            not provided, the design will be based on the provided columns dictionary.
        columns: Dict[str, Any], optional
            A dictionary of column information to use for the design of the Parquet file
            product.
        metadata: Dict[str, str], optional
            A dictionary of metadata to include in the design of the Parquet file
            product.

        """

        assert polars, "Polars is required to work with Parquet file products."

        if not self.design or (self.filename and os.path.exists(self.filename)):
            raise RuntimeError(
                "Cannot design a new Parquet file when not in the datamodel "
                "design phase or if a real file already exists."
            )

        cached_df = self._cache["releases"]["WORK"][self.cache_key]

        if dataframe is None and not columns:
            columns = {}

        if dataframe is not None:
            dm_columns = self._parse_columns(dataframe, get_value=True)
        elif columns is not None:
            dm_columns = {}

            for colname, colinfo in columns.items():
                dm_columns[colname] = {
                    "name": colname,
                    "dtype": str(colinfo["dtype"]),
                    "unit": self._nonempty_string()
                    if colinfo["unit"] is None
                    else colinfo["unit"],
                    "description": self._nonempty_string()
                    if colinfo["description"] is None
                    else colinfo["description"],
                }

        cached_df["columns"] = dm_columns

        metadata = metadata or {}
        cached_df["metadata"] = {
            key: {
                "key": key,
                "description": self._nonempty_string(),
                "value": str(value),
            }
            for key, value in metadata.items()
        }

        self._cache["releases"]["WORK"][self.cache_key] = cached_df

        return

    def write_design(self, file: str, overwrite: bool = False) -> None:
        """Write the design of a Parquet file product to disk."""

        if self._designed_object is None:
            raise AttributeError("Cannot write. Designed object does not exist.")

        if os.path.exists(file) and not overwrite:
            raise FileExistsError(f"File {file!r} already exists.")

        cache = self._cache["releases"]["WORK"][self.cache_key]
        metadata = cache.get("metadata", {})

        self._designed_object.write_parquet(
            file,
            metadata={item["key"]: item.get("value", "") for item in metadata.values()},
        )

    def _get_designed_object(self, data: dict) -> DataFrameType:
        """Get the designed object for a Parquet file product."""

        if not polars:
            raise ImportError("Polars is required to work with Parquet file products.")

        return DataFrameModel.model_validate(data).generate_dataframe()
