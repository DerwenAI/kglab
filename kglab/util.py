#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## utilities

import math
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import typing


def calc_quantile_bins (
    num_rows: int
    ) -> np.ndarray:
    """
    Calculate the bins to use for a quantile stripe, using [`numpy.linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)

    num_rows: number of rows in the dataframe
    return: the calculated bins, as a NumPy array
    """
    granularity = max(round(math.log(num_rows) * 4), 1)
    return np.linspace(0, 1, num=granularity, endpoint=True)


def stripe_column (
    values: list,
    bins: int
    ) -> np.ndarray:
    """
    Stripe a column in a dataframe, by interpolated quantiles into a set of discrete indexes.

    values: list of values to stripe
    bins: quantile bins; see [`calc_quantile_bins()`](#calc_quantile_bins-function)
    return: the striped column values, as a NumPy array
    """
    s = pd.Series(values)
    q = s.quantile(bins, interpolation="nearest")

    try:
        stripe = np.digitize(values, q) - 1
        return stripe
    except ValueError as e:
        # should never happen?
        print("ValueError:", str(e), values, s, q, bins)
        raise


def root_mean_square (
    values: list
    ) -> float:
    """
    Calculate the *root mean square* of the values in the given list.

    values: list of values to use in the RMS calculation
    return: RMS metric as a float
    """
    numer = sum([x for x in map(lambda x: float(x)**2.0, values)])
    denom = float(len(values))
    return math.sqrt(numer / denom)
