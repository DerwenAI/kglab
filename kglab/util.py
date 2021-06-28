#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

######################################################################
## utilities

import math
import numpy as np  # type: ignore  # pylint: disable=E0401
import pandas as pd  # type: ignore  # pylint: disable=E0401


def get_gpu_count () -> int:
    """
Special handling for detecting GPU availability: an approach
recommended by the NVIDIA RAPIDS engineering team, since `nvml`
bindings are difficult for Python libraries to keep updated.

This has the side-effect of importing the `cuDF` library, when
GPUs are available.

    returns:
count of available GPUs
    """
    try:
        import pynvml  # type: ignore  # pylint: disable=E0401
        pynvml.nvmlInit()

        gpu_count = pynvml.nvmlDeviceGetCount()

        if gpu_count > 0:
            import cudf  # type: ignore # pylint: disable=E0401,W0611,W0621
            # print(f"using {gpu_count} GPUs")

    except Exception: # pylint: disable=W0703
        gpu_count = 0

    return gpu_count


## NB: workaround for GitHub CI

if get_gpu_count() > 0:
    import cudf  # type: ignore # pylint: disable=E0401


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
    *,
    use_gpus: bool = False,
    ) -> np.ndarray:
    """
Stripe a column in a dataframe, by interpolating quantiles into a set of discrete indexes.

    values:
list of values to stripe

    bins:
quantile bins; see [`calc_quantile_bins()`](#calc_quantile_bins-function)

    use_gpus:
optionally, use the NVidia GPU devices with the [RAPIDS libraries](https://rapids.ai/) if these libraries have been installed and the devices are available; defaults to `False`

    returns:
the striped column values, as a [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html); uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled
    """
    if use_gpus:
        s = cudf.Series(values)
    else:
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
    s = sum(map(lambda x: float(x)**2.0, values))
    n = float(len(values))
    return math.sqrt(s / n)
