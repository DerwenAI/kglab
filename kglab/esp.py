#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright
# mypy: ignore-errors
# pylint: disable-all

######################################################################
## Evolunationary Shape Prediction

from kglab import KnowledgeGraph, Measure, Subgraph
from kglab.pkg_types import RDF_Node, SPARQL_Bindings
import kglab.util

from collections import deque
import pandas as pd  # type: ignore
import random
import rdflib  # type: ignore
import typing

SerializedEvoEdge = typing.Tuple[int, int]
SerializedEvoNode = typing.Tuple[int, typing.List[SerializedEvoEdge]]

Evolike = typing.TypeVar("Evolike", int, SerializedEvoNode)
SerializedEvoShape = typing.List[Evolike]

EvoShapeBoard = typing.List[SerializedEvoShape]
EvoShapeDistance = typing.Tuple[int, int, float]


class EvoShapeNode:
    """
    """

    def __init__ (
        self,
        *,
        uri: str = None,
        terminal: bool = False,
        ) -> None:
        """
        """
        self.uri = uri
        self.terminal = terminal
        self.done = terminal # initially
        self.edges: typing.List[EvoShapeEdge] = []


    def serialize (
        self,
        subgraph: Subgraph,
        ) -> SerializedEvoNode:
        """
        """
        edge_list = sorted([ (subgraph.transform(e.pred), subgraph.transform(e.obj.uri),) for e in self.edges ])
        return subgraph.transform(self.uri), edge_list


    @classmethod
    def deserialize (
        cls,
        dat: SerializedEvoNode,
        subgraph: Subgraph,
        uri_map: dict,
        *,
        root_node: "EvoShapeNode" = None,
        ) -> "EvoShapeNode":
        """
        """
        node_id, edge_list = dat
        uri = subgraph.inverse_transform(node_id)

        if uri in uri_map:
            node = uri_map[uri]
        else:
            node = EvoShapeNode(uri=uri)
            uri_map[uri] = node

        for p, o in edge_list:
            uri = subgraph.inverse_transform(o)

            if not uri and root_node:
                node = root_node
            elif uri in uri_map:
                obj = uri_map[uri]
            else:
                obj = EvoShapeNode(uri=uri)
                uri_map[uri] = obj

            edge = EvoShapeEdge(pred=str(subgraph.inverse_transform(p)), obj=obj)
            node.edges.append(edge)

        return node


class EvoShapeEdge (typing.NamedTuple):
    """
    """

    pred: str
    obj: EvoShapeNode


class EvoShape:
    """
    """

    def __init__ (
        self,
        kg: KnowledgeGraph,
        measure: Measure,
        ) -> None:
        """
        """
        self.kg = kg
        self.measure = measure
        self.root = EvoShapeNode(uri=None)
        self.nodes = set([self.root])


    def add_link (
        self,
        s: RDF_Node,
        p: RDF_Node,
        o: RDF_Node,
        ) -> None:
        """
        """
        edge = EvoShapeEdge(pred=p, obj=o)
        s.edges.append(edge)
        self.nodes.add(o)


    def serialize (
        self,
        subgraph: Subgraph,
        ) -> SerializedEvoShape:
        """
Transform to ordinal format which can be serialized/deserialized, using a `Subgraph` with a consistent ordering across different distributed processes.
        """
        d: deque = deque(sorted([ n.serialize(subgraph) for n in self.nodes.difference({self.root}) ]))
        d.appendleft(self.root.serialize(subgraph))
        d.appendleft(self.get_cardinality())
        return list(d)


    def deserialize (
        self,
        dat_list: SerializedEvoShape,
        subgraph: Subgraph,
        ) -> dict:
        """
Replace shape definition with parsed content.
        """
        dat_list.pop(0) # ignore the instances
        uri_map: dict = {}
        self.nodes = set()

        root_dat = dat_list.pop(0)
        self.root = EvoShapeNode.deserialize(root_dat, subgraph, uri_map)
        self.nodes.add(self.root)

        for node_dat in dat_list:
            node = EvoShapeNode.deserialize(node_dat, subgraph, uri_map, root_node=self.root)
            self.nodes.add(node)

        return uri_map


    def get_rdf (
        self
        ) -> typing.List[str]:
        """
For debugging purposes only:
since by definition, a shape is not fully qualified RDF.
        """
        rdf_list: typing.List[str] = []

        for node in list(self.nodes):
            if not node.uri:
                b = rdflib.BNode()
                subj = str(b.n3())
            else:
                subj = rdflib.term.URIRef(node.uri).n3(self.kg.rdf_graph().namespace_manager)

            for edge in node.edges:
                pred = rdflib.term.URIRef(edge.pred).n3(self.kg.rdf_graph().namespace_manager)
                obj = rdflib.term.URIRef(edge.obj.uri).n3(self.kg.rdf_graph().namespace_manager)
                triple = "{} {} {} .".format(subj, pred, obj)
                rdf_list.append(triple)

        return rdf_list


    def get_sparql (
        self
        ) -> SPARQL_Bindings:
        """
        """
        var_list: typing.List[str] = []
        clauses: typing.List[str] = []
        uri_map: dict = {}
        bindings: dict = {}
        node_list = list(self.nodes)

        for node_num, node in enumerate(node_list):
            # name the subject
            if not node.uri:
                subj = "?v{}".format(node_num)
                var_list.append(subj)
            elif node.uri in uri_map:
                subj = uri_map[node.uri]
            else:
                subj = "?node{}".format(node_num)
                uri_map[node.uri] = subj
                bindings[subj] = rdflib.URIRef(node.uri)

            # generate a clause for each tuple
            for edge_num in range(len(node.edges)):
                edge = node.edges[edge_num]

                if edge.pred in uri_map:
                    pred = uri_map[edge.pred]
                else:
                    pred = "?pred{}_{}".format(node_num, edge_num)
                    uri_map[edge.pred] = pred
                    bindings[pred] = rdflib.URIRef(edge.pred)

                if edge.obj.uri in uri_map:
                    obj = uri_map[edge.obj.uri]
                else:
                    obj = "?obj{}_{}".format(node_num, edge_num)
                    uri_map[edge.obj.uri] = obj
                    bindings[obj] = rdflib.URIRef(edge.obj.uri)

                clauses.append(" ".join([ subj, pred, obj ]))

        sparql = "SELECT DISTINCT {} WHERE {{ {} }}".format(" ".join(var_list), " . ".join(clauses))
        return sparql, bindings


    def get_cardinality (
        self
        ) -> int:
        """
        """
        sparql, bindings = self.get_sparql()
        return len(list(self.kg.query(sparql, bindings=bindings)))


    def calc_distance (
        self,
        other: "EvoShape",
        ) -> float:
        """
        """
        n0 = { n.uri for n in self.nodes }
        n1 = { n.uri for n in other.nodes }
        distance = len(n0.intersection(n1)) / float(max(len(n0), len(n1)))
        return distance


class ShapeFactory:
    """
    """

    def __init__ (
        self,
        kg: KnowledgeGraph,
        measure: Measure,
        ) -> None:
        """
        """
        self.kg = kg
        self.measure = measure
        self.subgraph = Subgraph(kg, preload=measure.get_keyset())

        # enum action space of possible RDF types (i.e., "superclasses")
        type_sparql = "SELECT DISTINCT ?n WHERE {[] rdf:type ?n}"
        self.type_list = [ r.n for r in kg.query(type_sparql) ]


    def new_shape (
        self,
        *,
        type_uri: str = None,
        ) -> EvoShape:
        """
        """
        es = EvoShape(self.kg, self.measure)

        if not type_uri:
            ## RANDOM CHOICE => RL observation?
            ## TODO: generate from gamma dist -- or specify
            type_uri = random.choice(self.type_list)  # nosec

        type_node = EvoShapeNode(uri=type_uri, terminal=True)
        es.add_link(es.root, rdflib.RDF.type, type_node)
        return es


class Leaderboard:
    """
    """

    _COLUMNS: typing.List[str] = ["instances", "nodes", "distance", "rank", "shape"]

    def __init__ (
        self
        ) -> None:
        """
        """
        self.df = pd.DataFrame([], columns=self._COLUMNS)


    def get_board (
        self
        ) -> EvoShapeBoard:
        """
        Return a list of shapes, i.e., dataframe without any metrics.
        """
        return list(self.df["shape"].to_numpy())


    @classmethod
    def compare (
        cls,
        shape: SerializedEvoShape,
        board: EvoShapeBoard,
        ) -> EvoShapeDistance:
        """
        Compare distances among the shapes.
        """
        n0 = { n for n, e in shape[1:] }

        if len(board) < 2:
            min_dist = 0.0
        else:
            distances: list = []

            for b in board:
                n1 = { n for n, e in b[1:] }
                d = len(n0.intersection(n1)) / float(max(len(n0), len(n1)))

                if d < 1.0:
                    distances.append(d)

            min_dist = min(distances)

        return int(shape[0]), len(n0), min_dist


    @classmethod
    def insert (
        cls,
        shape: SerializedEvoShape,
        board: EvoShapeBoard,
        ) -> pd.DataFrame:
        """
Rank this `shape` within a dataframe generated from the given `board` object.
        """
        board.append(shape)
        df1 = pd.DataFrame([ cls.compare(s, board) for s in board ], columns=cls._COLUMNS[:3])

        # normalize by column
        df2 = df1.apply(lambda x: x/x.max(), axis=0)
        bins = kglab.util.calc_quantile_bins(len(df2.index))

        # stripe each column to approximate a pareto front
        stripes = [ kglab.util.stripe_column(values, bins) for _, values in df2.items() ]
        df3 = pd.DataFrame(stripes).T

        # rank based on RMS of striped indices per row
        df1["rank"] = df3.apply(kglab.util.root_mean_square, axis=1)
        df1["shape"] = pd.Series(board, index=df1.index)

        # sort descending
        return df1.sort_values(by=["rank"], ascending=False)


    def get_position (
        self,
        shape: SerializedEvoShape,
        ) -> int:
        """
Calculate a *distance-from-bottom* metric for the given `shape`.
        """
        return len(self.df.index) - list(self.df["shape"].to_numpy()).index(shape) - 1


    def add_shape (
        self,
        shape: SerializedEvoShape,
        ) -> int:
        """
Insert the given `shape` into the leaderboard, returning its position metric.
        """
        self.df = self.insert(shape, self.get_board())
        return self.get_position(shape)
