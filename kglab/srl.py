#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## classes to support models for statistical relational learning

from icecream import ic  # type: ignore
import pandas as pd  # type: ignore
import pslpython.model  # type: ignore
import pslpython.partition  # type: ignore
import pslpython.predicate  # type: ignore
import pslpython.rule  # type: ignore
import typing


class PSLModel:
    """
Class representing a
[*probabilistic soft logic*](../glossary/#probabilistic-soft-logic)
(PSL) model.

For PSL-specific terminology used here, see <https://psl.linqs.org/wiki/master/Glossary.html>
    """

    _PSL_OPTIONS: dict = {
        "log4j.threshold": "INFO",
    }

    _PARTITIONS: dict = {
        "observations": pslpython.partition.Partition.OBSERVATIONS,
        "targets": pslpython.partition.Partition.TARGETS,
        "truth": pslpython.partition.Partition.TRUTH,
    }


    def __init__ (
        self,
        *,
        name: str = None,
        ) -> None:
        """
Wrapper for constructing a [`pslpython.model.Model`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/model.py).

    name:
optional name of the PSL model; if not supplied, PSL generates a random name
        """
        self.model = pslpython.model.Model(name)
        self.results: dict = {}


    def add_predicate (
        self,
        raw_name: str,
        *,
        size: int = None,
        closed: bool = False,
        arg_types: typing.List = None,
        ) -> "PSLModel":
        """
Add a [`pslpython.predicate.Predicate`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/predicate.py) to this model.
Enough details must be supplied for PSL to infer the number and types of each predicate's arguments.

    raw_name:
name of the predicate; must be unique among all of the predicates

    size:
optional, the number of arguments for this predicate

    closed:
indicates that this predicate is fully observed, i.e., all substitutions of this predicate have known values and will behave as evidence for inference; otherwise, if `False` then infer some values of this predicate; defaults to `False`

    arg_types:
optional, a list of types for the arguments for this predicate; all arguments will default to string

    returns:
this PSL model – use for method chaining
        """
        predicate = pslpython.predicate.Predicate(
            raw_name,
            closed=closed,
            size=size,
            arg_types=arg_types,
            )

        self.model.add_predicate(predicate)
        return self


    def add_rule (
        self,
        rule_string: str,
        *,
        weighted: bool = None,
        weight: float = None,
        squared: bool = None,
        ) -> "PSLModel":
        """
Add a [`pslpython.rule.Rule`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/rule.py) to this model.

  * a weighted rule can change its weight or squared status
  * a weighted rule cannot convert into an unweighted rule nor visa-versa
  * unweighted rules are [*constraints*](https://psl.linqs.org/wiki/master/Constraints.html)

For more details, see <https://psl.linqs.org/wiki/master/Rule-Specification.html>

    rule_string:
text representation for specifying the rule

    weighted:
indicates that this rule is weighted

    weight:
weight of this rule

    squared:
indicates that this rule's potential is squared

    returns:
this PSL model – use for method chaining
        """
        if weight:
            weighted = True

        rule = pslpython.rule.Rule(
            rule_string=rule_string,
            weighted=weighted,
            weight=weight,
            squared=squared,
        )

        self.model.add_rule(rule)
        return self


    def clear_model (
        self
        ) -> "PSLModel":
        """
Clear any pre-existing data from each of the predicates, to initialize the model.

    returns:
this PSL model – use for method chaining
        """
        for predicate in self.model.get_predicates().values():
            predicate.clear_data()

        return self


    def add_data_row (
        self,
        predicate_name: str,
        args: list,
        *,
        partition: str = "observations",
        truth_value: float = 1.0,
        verbose: bool = False,
        ) -> "PSLModel":
        """
Add a single record to a specified predicate, within a specified partition.

    predicate_name:
name of the specific predicate; name normalization will be handled internally; raises `ModelError` if the predicate name is not found

    args:
arguments for the record being added, as a list

    partition:
label for the [`pslpython.partition.Partition`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/partition.py) into which the `data` gets added; must be among `[ "observations", "targets", "truth" ]`; defaults to `"observations"`; see <https://psl.linqs.org/wiki/master/Data-Storage-in-PSL.html>

    truth_value:
optional truth value of the record being added

    verbose:
flag for verbose trace of each added record

    returns:
this PSL model – use for method chaining
        """
        try:
            predicate = self.model.get_predicate(predicate_name)
            assert predicate
        except:
            error = "Unknown predicate: {}".format(predicate_name)
            raise pslpython.model.ModelError(error)

        try:
            partition_obj = self._PARTITIONS[partition.lower()]
        except:
            error = "Unknown partition: {}".format(partition)
            raise pslpython.model.ModelError(error)

        if verbose:
            ic(predicate_name, partition, args)

        predicate.add_data_row(
            partition_obj,
            args=args,
            truth_value=truth_value,
        )

        return self


    def infer (
        self,
        *,
        method: str = "",
        cli_options: list = None,
        psl_config: dict = None,
        jvm_options: list = None,
        ) -> None:
        """
Run inference on this model, storing the inferred results in an internal dataframe.

    method:
the inference method to use

    cli_options:
additional options to pass to PSL, based on its CLI options; see <https://psl.linqs.org/wiki/master/Configuration.html>

    psl_config:
configuration options passed directly to the PSL core code; see <https://psl.linqs.org/wiki/master/Configuration-Options.html>

    jvm_options:
options passed to the JVM running the PSL Java library; most commonly `"-Xmx"` and `"-Xms"`
        """
        if not cli_options:
            cli_options = []

        if not psl_config:
            psl_config = self._PSL_OPTIONS

        if not jvm_options:
            jvm_options = []

        self.results = self.model.infer(
            method=method,
            additional_cli_optons=cli_options,
            psl_config=psl_config,
            jvm_options=jvm_options,
        )


    def get_results (
        self,
        predicate_name: str,
        ) -> pd.DataFrame:
        """
Accessor for the inferred results for a specified predicate.

    predicate_name:
name of the specific predicate; name normalization will be handled internally; raises `ModelError` if the predicate name is not found

    returns:
inferred values as a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html), with columns names for each argument plus the `"truth"` value
        """
        try:
            predicate = self.model.get_predicate(predicate_name)
            assert predicate
        except:
            error = "Unknown predicate: {}".format(predicate_name)
            raise pslpython.model.ModelError(error)

        df = self.results[predicate].copy(deep=True)
        df.insert(0, "predicate", predicate.name())
        return df
