#!/usr/bin/env python
"""Collection of functions for the manipulation of time series."""

from __future__ import absolute_import, division, print_function

from argparse import RawTextHelpFormatter
import os
import warnings

import mando
import pandas as pd

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import typic

from .. import tsutils

warnings.filterwarnings("ignore")


@mando.command("read", formatter_class=RawTextHelpFormatter)
@tsutils.doc(tsutils.docstrings)
def read_cli(
    force_freq=None,
    append="columns",
    columns=None,
    start_date=None,
    end_date=None,
    dropna="no",
    skiprows=None,
    index_type="datetime",
    names=None,
    clean=False,
    source_units=None,
    target_units=None,
    float_format="g",
    round_index=None,
    tablefmt="csv",
    *filenames,
):
    """
    Combines time-series from a list of pickle or csv files.

    Prints the read in time-series in the tstoolbox standard format.

    WARNING: Accepts naive and timezone aware time-series by converting all to
    UTC and removing timezone information.

    Parameters
    ----------
    filenames : str
        From the command line a list of comma or space delimited filenames to
        read time series from.  Using the Python API a list or tuple of
        filenames.
    append : str
        [optional, default is 'columns']

        The type of appending to do.  For "combine" option matching
        column indices will append rows, matching row indices will
        append columns, and matching column/row indices use the value
        from the first dataset.  You can use "row" or "column" to force
        an append along either axis.
    {force_freq}

        {pandas_offset_codes}

    {columns}
    {start_date}
    {end_date}
    {dropna}
    {skiprows}
    {index_type}
    {names}
    {clean}
    {source_units}
    {target_units}
    {float_format}
    {round_index}
    {tablefmt}

    """
    tsutils.printiso(
        read(
            *filenames,
            force_freq=force_freq,
            append=append,
            columns=columns,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            clean=clean,
            source_units=source_units,
            target_units=target_units,
            round_index=round_index,
        ),
        float_format=float_format,
        tablefmt=tablefmt,
    )


@typic.al
def read(
    *filenames,
    force_freq=None,
    append: Literal["columns", "rows", "combine"] = "columns",
    columns=None,
    start_date=None,
    end_date=None,
    dropna="no",
    skiprows=None,
    index_type="datetime",
    names=None,
    clean=False,
    source_units=None,
    target_units=None,
    round_index=None,
):
    """Collect time series from a list of pickle or csv files."""
    if force_freq is not None:
        dropna = "no"

    # # Check for older style where comma delimited list of only files.
    # # If so, rework as space delimited.
    # fcheck = True
    # for fname in tsutils.make_list(filenames):
    #     if not os.path.exists(fname):
    #         fcheck = False
    #         break
    # if fcheck is False:
    #     # All filenames are real files.  Therefore old style and just make a simple
    #     # list.
    #     filenames = tsutils.make_list(filenames)
    filenames = tsutils.make_list(filenames, sep=" ")

    tsd = tsutils.common_kwds(
        input_tsd=filenames,
        skiprows=skiprows,
        names=names,
        index_type=index_type,
        start_date=start_date,
        end_date=end_date,
        round_index=round_index,
        dropna=dropna,
        force_freq=force_freq,
        clean=clean,
        source_units=source_units,
        target_units=target_units,
        usecols=columns,
    )

    return tsd


read.__doc__ = read_cli.__doc__
