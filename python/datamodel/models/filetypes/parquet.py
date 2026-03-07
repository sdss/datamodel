#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2026-03-06
# @Filename: parquet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Union

from pydantic import Field

from datamodel import log
from datamodel.models.base import CoreModel

__all__ = ["DataFrame", "DataFrameColumn", "ChangeParquet"]


try:
    import polars
except ImportError:
    polars: None = None


if TYPE_CHECKING and polars:
    DataFrameType = polars.DataFrame


class DataFrame(CoreModel):
    """Pydantic model representing a dataframe in a Parquet file.

    Parameters
    ----------
    columns: Dict[str, DataFrameColumn]
        A dictionary of columns in the dataframe, keyed by column name.
    metadata: List[Dict[str, Any]]
        A list of dictionaries containing metadata for the dataframe.

    """

    columns: Dict[str, DataFrameColumn] = Field(
        default_factory=dict,
        repr=False,
        description="A dictionary of columns in the dataframe, keyed by column name.",
    )

    metadata: List[Dict[str, Any]] = Field(
        default_factory=list,
        repr=False,
        description="A list of dictionaries containing metadata for the dataframe.",
    )

    def generate_dataframe(self) -> DataFrameType:
        """Generate a DataFrame model from this column."""

        if not polars:
            raise ImportError("Polars is required to work with Parquet file products.")

        schema = {}
        data = {}
        for col in self.columns:
            column_info = self.columns[col]

            data[col] = column_info.value

            try:
                dtype_str = column_info.dtype
                dtype = eval(f"polars.{dtype_str}")
            except Exception:
                log.warning(f"Could not parse dtype '{dtype_str}' for column '{col}'.")
                continue

            schema[col] = dtype

        df = polars.DataFrame(data=data, schema=schema)

        # Drop rows where all values are null.
        df = df.filter(polars.all_horizontal(polars.all().is_null().not_()))

        return df


class DataFrameColumn(CoreModel):
    """Pydantic model representing a column in a dataframe in a Parquet file.

    Parameters
    ----------

    name: str
        The name of the column.
    description: str
        A description of the column.
    unit: str
        The units of the column.
    dtype: str
        The data type of the column.
    value: Any
        An example value for the column.

    """

    name: str = Field(
        ...,
        description="The name of the column.",
    )
    description: str = Field(
        ...,
        description="A description of the column.",
    )
    unit: Union[str, None] = Field(
        ...,
        description="The units of the column.",
    )
    dtype: str = Field(
        ...,
        description="The data type of the column.",
    )
    value: Any = Field(
        None,
        description="An example value for the column.",
    )


class DataFrameMetadata(CoreModel):
    """Pydantic model representing the metadata of a dataframe in a Parquet file.

    Parameters
    ----------
    key: str
        The key of the metadata.
    description: str
        A description of the metadata key.
    value: Any
        An example value for the metadata.

    """

    key: str = Field(
        ...,
        description="The key of the metadata.",
    )
    description: str = Field(
        ...,
        description="Description of the metadata key.",
    )
    value: Any = Field(
        None,
        description="An example value for the metadata",
    )


class ChangeParquet(CoreModel):
    """Pydantic model representing the changes to a Parquet file between two releases.

    Parameters
    ----------
    delta_ncolumns: int
        The difference in number of columns between the two Parquet files.
    added_columns: List[str]
        A list of columns that were added between the two Parquet files.
    removed_columns: List[str]
        A list of columns that were removed between the two Parquet files.

    """

    delta_ncolumns: int = Field(
        default=0,
        description="The difference in number of columns between the two Parquet files.",
    )
    added_columns: List[str] = Field(
        default_factory=list,
        description="A list of columns that were added between the two Parquet files.",
    )
    removed_columns: List[str] = Field(
        default_factory=list,
        description="A list of columns that were removed between the two Parquet files.",
    )
