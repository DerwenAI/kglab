#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

"""
Queryable abstraction layer.
"""

from abc import ABC, abstractmethod
import typing

import pandas as pd  # type: ignore  # pylint: disable=E0401


class Queryable (ABC):
    """
Abstract class for query support.
    """

    @abstractmethod
    def query (
        self,
        query: str,
        ) -> typing.Iterable:
        """
Abstract method for querying.
        """
        pass  # pylint: disable=W0107


    @abstractmethod
    def query_as_df (
        self,
        query: str,
        ) -> pd.DataFrame:
        """
Abstract method for querying, which returns a pandas DataFrame.
        """
        pass  # pylint: disable=W0107
