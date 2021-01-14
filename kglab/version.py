#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import typing


######################################################################
## Python version management

MIN_PY_VERSION: typing.Tuple = (3, 6,)


def _versify (
    l: typing.Tuple
    ) -> str:
    """convert Python version (tuple) to a point release (str)"""
    return ".".join([ str(x) for x in l ])


def _check_version () -> None:
    """compare the Python version info vs. the minimum required"""
    py_version_info: typing.Tuple = sys.version_info[:2]

    if py_version_info < MIN_PY_VERSION:
        error_msg = "This version of kglab requires Python {} or later ({} detected)\n"
        raise RuntimeError(error_msg.format(_versify(MIN_PY_VERSION), _versify(py_version_info)))
