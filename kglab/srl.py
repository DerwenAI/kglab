#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

######################################################################
## classes to support models for statistical relational learning

from icecream import ic  # type: ignore  # pylint: disable=E0401
import pandas as pd  # type: ignore  # pylint: disable=E0401
import pathlib
import pslpython.model  # type: ignore  # pylint: disable=E0401
import pslpython.partition  # type: ignore  # pylint: disable=E0401
import pslpython.predicate  # type: ignore  # pylint: disable=E0401
import pslpython.rule  # type: ignore  # pylint: disable=E0401
import typing


class PSLModel:
    """
Class representing a
[*probabilistic soft logic*](../glossary/#probabilistic-soft-logic)
(PSL) model.

For PSL-specific terminology used here, see <https://psl.linqs.org/wiki/master/Glossary.html>

Note: You need to have a Java JDK installed to run PSL.
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


    @classmethod
    def _raise_model_error (
        cls,
        obj: str,
        msg: str,
        ) -> None:
        """
Semiprivate helper function to format and raise a `ModelError` exception.

    obj:
name of the object to be reported

    msg:
the exception message to use
        """
        error = "{}: {}".format(msg, obj)
        raise pslpython.model.ModelError(error)


    def _get_predicate (
        self,
        predicate_name: str,
        ) -> pslpython.predicate.Predicate:
        """
Semiprivate accessor method to lookup a predicate, with error checking.

    predicate_name:
name of the specific predicate; name normalization will be handled internally; raises `ModelError` if the predicate name is not found

    returns:
predicate object
        """
        try:
            predicate = self.model.get_predicate(predicate_name)

            if not predicate:
                self._raise_model_error(predicate_name, "Unknown predicate")
        except:  # pylint: disable=W0702 # lgtm[py/catch-base-exception]
            self._raise_model_error(predicate_name, "Unknown predicate")

        return predicate


    def _get_partition (
        self,
        partition: str,
        ) -> pslpython.partition.Partition:
        """
Semiprivate accessor method to lookup a partition, with error checking.

    partition:
label for the [`pslpython.partition.Partition`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/partition.py) into which the `data` gets added; must be among `[ "observations", "targets", "truth" ]`; see <https://psl.linqs.org/wiki/master/Data-Storage-in-PSL.html>

    returns:
partition object
        """
        try:
            partition_obj = self._PARTITIONS[partition.lower()]

            if not partition_obj:
                self._raise_model_error(partition, "Unknown partition")
        except:  # pylint: disable=W0702 # lgtm[py/catch-base-exception]
            self._raise_model_error(partition, "Unknown partition")

        return partition_obj


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
        if verbose:
            ic(predicate_name, partition, args)

        predicate = self._get_predicate(predicate_name)

        predicate.add_data_row(
            self._get_partition(partition),
            args=args,
            truth_value=truth_value,
        )

        return self


    def trace_predicate (
        self,
        predicate_name: str,
        *,
        partition: str = "observations",
        path: pathlib.Path = None,
        ) -> pd.DataFrame:
        """
Construct a trace of the data in a specified predicate, within a specified partition, formatted as a dataframe.
Use a consistent column naming and sort order, so that these values can be used later in testing.
Optionally write out this out to a TSV file.

    predicate_name:
name of the specific predicate; name normalization will be handled internally; raises `ModelError` if the predicate name is not found

    partition:
label for the [`pslpython.partition.Partition`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/partition.py) into which the `data` gets added; must be among `[ "observations", "targets", "truth" ]`; defaults to `"observations"`; see <https://psl.linqs.org/wiki/master/Data-Storage-in-PSL.html>

    path:
optional output path for the TSV file; defaults to `None`

    returns:
dataframe representing the traced partition data
        """
        predicate = self._get_predicate(predicate_name)
        partition_obj = self._get_partition(partition)

        df = predicate._data[partition_obj].copy(deep=True)  # pylint: disable=W0212
        df.columns = [ "P1", "P2", "value" ]
        df = df.sort_values(by=[ "P1", "P2" ]).reset_index(drop=True)

        if path:
            df.to_csv(path, sep="\t", index=False)

        return df


    @classmethod
    def compare_predicate (
        cls,
        df: pd.DataFrame,
        trace_path: pathlib.Path,
        ) -> pd.DataFrame:
        """
Compare the values of a predict with its expected values which get loaded from a file.
This will print any expected (missing) or error (mismatched) rows.

    df:
dataframe from `trace_predicate`

    trace_path:
path to a TSV file of expected values, saved from the trace of a baseline run

    returns:
dataframe loaded from the expected values
        """
        df_known = pd.read_csv(trace_path, sep="\t")
        df_known[[ "P1", "P2" ]] = df_known[[ "P1", "P2" ]].astype(int)
        df_known = df_known.sort_values(by=[ "P1", "P2" ]).reset_index(drop=True)

        for _, row in df_known.iterrows():
            p1, p2, value = row
            loc = df.loc[(df["P1"] == p1) & (df["P2"] == p2)]

            if len(loc) > 0:
                loc_val = float(loc["value"])

                if value != loc_val:
                    print(" expected", loc)
            else:
                print(" error", int(p1), int(p2), value)

        return df_known


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
        predicate = self._get_predicate(predicate_name)
        df = self.results[predicate].copy(deep=True)
        df.insert(0, "predicate", predicate.name())

        return df
