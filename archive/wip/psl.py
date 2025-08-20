#!/usr/bin/env python3

from icecream import ic
from pslpython.model import Model
from pslpython.partition import Partition
from pslpython.predicate import Predicate
from pslpython.rule import Rule
import os
import pandas as pd
import pathlib
import sys

# from:
# <https://github.com/linqs/psl-examples/blob/master/simple-acquaintances/python/simple-acquaintances.py>


DATA_DIR = os.path.join("..", "dat", "psl")

ADDITIONAL_PSL_OPTIONS: dict = {
    "log4j.threshold": "INFO"
}

ADDITIONAL_CLI_OPTIONS: list = [
    # "--postgres"
]


def add_predicates (model):
    predicate = Predicate("Knows", closed = False, size = 2)
    model.add_predicate(predicate)

    predicate = Predicate("Likes", closed = True, size = 2)
    model.add_predicate(predicate)

    predicate = Predicate("Lived", closed = True, size = 2)
    model.add_predicate(predicate)


def add_rules (model):
    model.add_rule(Rule("20: Lived(P1, L) & Lived(P2, L) & (P1 != P2) -> Knows(P1, P2) ^2"))
    model.add_rule(Rule("5: Lived(P1, L1) & Lived(P2, L2) & (P1 != P2) & (L1 != L2) -> !Knows(P1, P2) ^2"))
    model.add_rule(Rule("10: Likes(P1, L) & Likes(P2, L) & (P1 != P2) -> Knows(P1, P2) ^2"))
    model.add_rule(Rule("5: Knows(P1, P2) & Knows(P2, P3) & (P1 != P3) -> Knows(P1, P3) ^2"))
    model.add_rule(Rule("Knows(P1, P2) = Knows(P2, P1) ."))
    model.add_rule(Rule("5: !Knows(P1, P2) ^2"))


def add_data (model):
    for predicate in model.get_predicates().values():
        predicate.clear_data()

    path = os.path.join(DATA_DIR, "knows_obs.txt")
    model.get_predicate("Knows").add_data_file(Partition.OBSERVATIONS, path)

    path = os.path.join(DATA_DIR, "lived_obs.txt")
    model.get_predicate("Lived").add_data_file(Partition.OBSERVATIONS, path)

    path = os.path.join(DATA_DIR, "likes_obs.txt")
    model.get_predicate("Likes").add_data_file(Partition.OBSERVATIONS, path)

    path = os.path.join(DATA_DIR, "knows_targets.txt")
    model.get_predicate("Knows").add_data_file(Partition.TARGETS, path)

    path = os.path.join(DATA_DIR, "knows_truth.txt")
    model.get_predicate("Knows").add_data_file(Partition.TRUTH, path)


def trace_predicate (predicate_name, partition, out_path):
    """
TODO: migrate this into `kglab` for unit tests
    """
    df = model.get_predicate(predicate_name)._data[partition]
    df.columns = [ "P1", "P2", "value" ]
    df = df.sort_values(by=[ "P1", "P2" ])
    df.to_csv(out_path, sep="\t", index=False)

    return df


def compare_predicate (trace_path, df):
    """
TODO: migrate this into `kglab` for unit tests
    """
    df_known = pd.read_csv(trace_path, sep="\t")
    return df_known.compare(df)


def infer (model):
    add_data(model)

    df = model.infer(
        additional_cli_optons = ADDITIONAL_CLI_OPTIONS,
        psl_config = ADDITIONAL_PSL_OPTIONS
        )

    return df


def write_results (results, model):
    out_dir = "."
    os.makedirs(out_dir, exist_ok = True)

    for predicate in model.get_predicates().values():
        if not predicate.closed():
            out_path = os.path.join(out_dir, "%s.txt" % (predicate.name()))
            results[predicate].to_csv(out_path, sep = "\t", header = False, index = False)


if __name__ == "__main__":
    model = Model("simple-acquaintances")

    add_predicates(model)
    add_rules(model)

    # inference

    results = infer(model)
    write_results(results, model)

    # save intermediate results

    out_path = pathlib.Path("knows_obs.tsv")
    ic(out_path)
    df = trace_predicate("Knows", Partition.OBSERVATIONS, out_path)
    ic(df)
    ic(compare_predicate(out_path, df))

    out_path = pathlib.Path("lived_obs.tsv")
    ic(out_path)
    df = trace_predicate("Lived", Partition.OBSERVATIONS, out_path)
    ic(df)

    out_path = pathlib.Path("likes_obs.tsv")
    ic(out_path)
    df = trace_predicate("Likes", Partition.OBSERVATIONS, out_path)
    ic(df)

    out_path = pathlib.Path("knows_tar.tsv")
    ic(out_path)
    df = trace_predicate("Knows", Partition.TARGETS, out_path)
    ic(df)

    out_path = pathlib.Path("knows_tru.tsv")
    ic(out_path)
    df = trace_predicate("Knows", Partition.TRUTH, out_path)
    ic(df)
