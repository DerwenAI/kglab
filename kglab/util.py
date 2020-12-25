#!/usr/bin/env python
# encoding: utf-8

import math
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import typing


######################################################################
## utilities

def calc_quantile_bins (num_rows: int) -> np.ndarray:
    """calculate the number of bins to use for a quantile stripe"""
    granularity = max(round(math.log(num_rows) * 4), 1)
    return np.linspace(0, 1, num=granularity, endpoint=True)


def stripe_column (values: list, bins: int) -> np.ndarray:
    """stripe a column: interpolate quantiles to discrete indexes"""
    s = pd.Series(values)
    q = s.quantile(bins, interpolation="nearest")

    try:
        stripe = np.digitize(values, q) - 1
        return stripe
    except ValueError as e:
        # should never happen?
        print("ValueError:", str(e), values, s, q, bins)
        raise


def root_mean_square (values: list) -> float:
    """calculate a root mean square"""
    numer = sum([x for x in map(lambda x: float(x)**2.0, values)])
    denom = float(len(values))
    return math.sqrt(numer / denom)
