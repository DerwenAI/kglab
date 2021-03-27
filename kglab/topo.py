#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

######################################################################
## graph topology

from kglab import KnowledgeGraph
from kglab.pkg_types import Census_Item, Census_Dyad_Tally

from collections import defaultdict
import pandas as pd  # type: ignore  # pylint: disable=E0401
import rdflib  # type: ignore  # pylint: disable=E0401
import typing


class Simplex0:
    """
Count the distribution of a class of items in an RDF graph.
In other words, tally an "item census" – to be consistent with the usage of that term.
    """

    def __init__ (
        self,
        name: str = "generic",
        ) -> None:
        """
Constructor for an item census.

    name:
optional name for this measure
        """
        self.name = name
        self.count: dict = defaultdict(int)
        self.df = None


    def increment (
        self,
        item0: Census_Item,
        ) -> None:
        """
Increment the count for this item.

    item0:
an item (domain: node, predicate, label, URL, literal, etc.) to be counted
        """
        self.count[item0] += 1


    def get_tally (
        self
        ) -> typing.Optional[pd.DataFrame]:
        """
Accessor for the item counts.

    returns:
a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with the count distribution, sorted in ascending order
        """
        self.df = pd.DataFrame.from_dict(
            self.count,
            orient="index",
            columns=["count"],
            ).sort_values("count", ascending=False)
        return self.df


    def get_keyset (
        self
        ) -> set:
        """
Accessor for the set of items (domain) counted.

    returns:
set of keys for the items (domain: nodes, predicates, labels, URLs, literals, etc.) that were counted
        """
        return { key.toPython() for key in self.count.keys() }


class Simplex1 (Simplex0):
    """
Measure a dyad census in an RDF graph, i.e., count the relations (directed edges) which connect two nodes.
    """

    def __init__ (
        self,
        name: str = "generic",
        ) -> None:
        """
Constructor for a dyad census.

    name:
optional name for this measure
        """
        super().__init__(name=name)  # type: ignore
        self.link_map: typing.Optional[dict] = None


    def increment (  # type: ignore # pylint: disable=W0221 # lgtm[py/inheritance/signature-mismatch]
        self,
        item0: Census_Item,
        item1: Census_Item,
        ) -> None:
        """
Increment the count for a dyad represented by the two given items.

    item0:
"source" item (domain: node, label, URL, etc.) to be counted

    item1:
"sink" item (range: node, label, literal, URL, etc.) to be counted
        """
        link = (item0, item1,)
        self.count[link] += 1


    def get_tally_map (
        self
        ) -> Census_Dyad_Tally:
        """
Accessor for the dyads census.

    returns:
a tuple of a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with the count distribution, sorted in ascending order; and a map of the observed links between "source" and "sink" items
        """
        super().get_tally()
        self.link_map = defaultdict(set)

        for index, _ in self.df.iterrows():  # type: ignore
            item0, item1 = index
            self.link_map[item0].add(item1)

        return self.df, self.link_map


class Measure:
    """
This class measures an RDF graph.
Its downstream use cases include: graph size estimates; computation costs; constructed shapes.
See <https://derwen.ai/docs/kgl/concepts/#measure>

Core feature areas include:

  * descriptive statistics
  * topological analysis
    """

    def __init__ (
        self,
        *,
        name: str = "generic",
        ) -> None:
        """
Constructor for this graph measure.

    name:
optional name for this measure
        """
        self.name = name
        self.edge_count = 0
        self.node_count = 0
        self.reset()


    def reset (
        self
        ) -> None:
        """
Reset (reinitialize) all of the counts for different kinds of census, which include:

  * total nodes
  * total edges
  * count for each kind of *subject* (`Simplex0`)
  * count for each kind of *predicate* (`Simplex0`)
  * count for each kind of *object* (`Simplex0`)
  * count for each kind of *literal* (`Simplex0`)
  * item census (`Simplex1`)
  * dyad census (`Simplex1`)
        """
        self.edge_count = 0
        self.node_count = 0
        self.s_gen = Simplex0("subject")
        self.p_gen = Simplex0("predicate")
        self.o_gen = Simplex0("object")
        self.l_gen = Simplex0("literal")
        self.n_gen = Simplex1("node")
        self.e_gen = Simplex1("edge")


    def get_node_count (
        self
        ) -> int:
        """
Accessor for the node count.

    returns:
value of `node_count`
        """
        return self.node_count


    def get_edge_count (
        self
        ) -> int:
        """
Accessor for the edge count.

    returns:
value of `edge_count`
        """
        return self.edge_count


    def measure_graph (
        self,
        kg: KnowledgeGraph,
        ) -> None:
        """
Run a full measure of the given RDF graph.

    kg:
`KnowledgeGraph` object representing the RDF graph to be measured
        """
        for s, p, o in kg.rdf_graph():
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


    def get_keyset (
        self,
        *,
        incl_pred: bool = True,
        ) -> typing.List[str]:
        """
Accessor for the set of items (domain: nodes, predicates, labels, URLs, literals, etc.) that were measured.
Used for *label encoding* in the transform between an RDF graph and a matrix or tensor representation.

    incl_pred:
flag to include the predicates in the set of keys to be encoded

    returns:
sorted list of keys to be used in the encoding
        """
        keys = self.s_gen.get_keyset().union(self.o_gen.get_keyset())

        if incl_pred:
            keys = keys.union(self.p_gen.get_keyset())

        return sorted(list(keys))
