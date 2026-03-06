#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2026-03-06
# @Filename: parquet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import Dict

from pydantic import Field

from datamodel.models.base import CoreModel


class DataFrame(CoreModel):
    """Pydantic model representing a dataframe in a Parquet file.

    Parameters
    ----------
    columns: Dict[str, DataFrameColumn]
        A dictionary of columns in the dataframe, keyed by column name.

    """

    columns: Dict[str, DataFrameColumn] = Field(
        default_factory=dict,
        repr=False,
        description="A dictionary of columns in the dataframe, keyed by column name.",
    )


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

    """

    name: str = Field(
        ...,
        description="The name of the column.",
    )
    description: str = Field(
        ...,
        description="A description of the column.",
    )
    unit: str = Field(
        ...,
        description="The units of the column.",
    )
    dtype: str = Field(
        ...,
        description="The data type of the column.",
    )
