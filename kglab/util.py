#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## utilities

import math
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def get_gpu_count () -> int:
    """
Special handling for detecting GPU availability: an approach
recommended by the NVidia RAPIDS engineering team, since `nvml`
bindings are difficult for Python libraries to keep updated.

    returns:
count of available GPUs
    """
    try:
        import pynvml  # type: ignore
        pynvml.nvmlInit()

        gpu_count = pynvml.nvmlDeviceGetCount()
    except Exception: # pylint: disable=W0703
        gpu_count = 0

    return gpu_count


def calc_quantile_bins (
    num_rows: int
    ) -> np.ndarray:
    """
Calculate the bins to use for a quantile stripe, using [`numpy.linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)

    num_rows:
number of rows in the target dataframe

    returns:
the calculated bins, as a [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
    """
    granularity = max(round(math.log(num_rows) * 4), 1)
    return np.linspace(0, 1, num=granularity, endpoint=True)


def stripe_column (
    values: list,
    bins: int,
    ) -> np.ndarray:
    """
Stripe a column in a dataframe, by interpolating quantiles into a set of discrete indexes.

    values:
list of values to stripe

    bins:
quantile bins; see [`calc_quantile_bins()`](#calc_quantile_bins-function)

    returns:
the striped column values, as a [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
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
Calculate the [*root mean square*](https://mathworld.wolfram.com/Root-Mean-Square.html) of the values in the given list.

    values:
list of values to use in the RMS calculation

    returns:
RMS metric as a float
    """
    numer = sum(map(lambda x: float(x)**2.0, values))
    denom = float(len(values))
    return math.sqrt(numer / denom)
