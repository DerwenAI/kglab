#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## graph topology

from kglab import KnowledgeGraph
from kglab.types import Census_Item, Census_Dyad_Tally, RDF_Node

from collections import defaultdict
import pandas as pd  # type: ignore
import rdflib  # type: ignore
import typing


class Simplex0 (object):
    def __init__ (self, name: str = "generic") -> None:
        self.name = name
        self.count: dict = defaultdict(int)
        self.df = None


    def increment (self, item: Census_Item) -> None:
        self.count[item] += 1


    def get_tally (self) ->  typing.Optional[pd.DataFrame]:
        self.df = pd.DataFrame.from_dict(self.count, orient="index", columns=["count"]).sort_values("count", ascending=False)
        return self.df


    def get_keyset (self) -> set:
        return set([ key.toPython() for key in self.count.keys() ])


class Simplex1 (Simplex0):
    """Measuring a dyad census"""

    def __init__ (self, name: str = "generic") -> None:
        super().__init__(name=name)  # type: ignore
        self.link_map: typing.Optional[dict] = None


    def increment (self, item0: Census_Item, item1: Census_Item) -> None:  # type: ignore
        link = (item0, item1,)
        self.count[link] += 1


    def get_tally_map (self) -> Census_Dyad_Tally:
        super().get_tally()
        self.link_map = defaultdict(set)

        for index, row in self.df.iterrows():  # type: ignore
            item0, item1 = index
            self.link_map[item0].add(item1)

        return self.df, self.link_map


class Measure (object):
    def __init__ (self, name: str = "generic") -> None:
        self.reset()


    def reset (self) -> None:
        self.edge_count = 0
        self.node_count = 0
        self.s_gen = Simplex0("subject")
        self.p_gen = Simplex0("predicate")
        self.o_gen = Simplex0("object")
        self.l_gen = Simplex0("literal")
        self.n_gen = Simplex1("node")
        self.e_gen = Simplex1("edge")


    def measure_graph (self, kg: KnowledgeGraph) -> None:
        for s, p, o in kg._g:
            self.edge_count += 1
            self.s_gen.increment(s)
            self.p_gen.increment(p)
            self.n_gen.increment(s, p)
    
            if isinstance(o, rdflib.term.Literal):
                self.l_gen.increment(o)
            else:
                self.o_gen.increment(o)
                self.e_gen.increment(p, o)
    
        self.node_count = len(set(self.s_gen.count.keys()).union(set(self.o_gen.count.keys())))


    def get_keyset (self, incl_pred: bool = True) -> typing.List[str]:
        keys = self.s_gen.get_keyset().union(self.o_gen.get_keyset())

        if incl_pred:
            keys = keys.union(self.p_gen.get_keyset())
            
        return sorted(list(keys))
