#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2026-03-03
# @Filename: parquet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Tuple, Type

from datamodel.generate.filetypes.base import BaseFile
from datamodel.models.filetypes.parquet import DataFrame as DataFrameModel

try:
    import polars
except ImportError:
    polars: None = None


if TYPE_CHECKING and polars:
    DataFrameType = polars.DataFrame
    DType = polars.datatypes.DataType
    ColumnDType = DType | Type[DType] | str | Tuple[DType | Type[DType] | str, Any]


__all__ = ["ParquetFileType"]


class ParquetFileType(BaseFile):
    """A file type for Parquet files."""

    suffix = "PARQUET"
    cache_key = "dataframe"

    def __init__(self, *args, **kwargs):
        super(ParquetFileType, self).__init__(*args, **kwargs)

        self._designed_object: DataFrameType | None = None

        if not polars:
            raise ImportError("Polars is required to work with Parquet file products.")

        # Read in the Parquet file if not designing one.
        self.dataframe: DataFrameType | None = None

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

    def _parse_columns(
        self,
        df: DataFrameType | None = None,
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
        dataframe: DataFrameType | None = None,
        columns: Dict[str, ColumnDType] | None = {},
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
            product. The keys should be column names. Values can be either a tuple
            of data type and example value, or just the date type, in which case
            the row value will be set to null.

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
                if isinstance(colinfo, tuple):
                    dtype, value = colinfo
                else:
                    dtype, value = colinfo, None

                if isinstance(dtype, (polars.datatypes.DataType, str)):
                    pass
                elif issubclass(dtype, polars.datatypes.DataType):
                    pass
                else:
                    raise ValueError("Data type must be a string or a Polars DataType.")

                dm_columns[colname] = {
                    "name": colname,
                    "dtype": str(dtype),
                    "unit": self._nonempty_string(),
                    "description": self._nonempty_string(),
                    "value": value,
                }

        cached_df["columns"] = dm_columns
        self._cache["releases"]["WORK"][self.cache_key] = cached_df

        return

    def write_design(self, file: str, overwrite: bool = False) -> None:
        """Write the design of a Parquet file product to disk."""

        if self._designed_object is None:
            raise AttributeError("Cannot write. Designed object does not exist.")

        if os.path.exists(file) and not overwrite:
            raise FileExistsError(f"File {file!r} already exists.")

        self._designed_object.write_parquet(file)

    def _get_designed_object(self, data: dict) -> DataFrameType:
        """Get the designed object for a Parquet file product."""

        if not polars:
            raise ImportError("Polars is required to work with Parquet file products.")

        return DataFrameModel.model_validate(data).generate_dataframe()
