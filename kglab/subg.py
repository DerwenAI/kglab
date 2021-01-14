#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## subgraph transforms for visualization, graph algorithms, etc.

from kglab import KnowledgeGraph
from kglab.pkg_types import NodeLike, RDF_Node, RDF_Triple

import pyvis.network  # type: ignore
import rdflib  # type: ignore
import typing


class Subgraph:
    """
This class transforms RDF graphs to matrix/tensor representation, to integrate with non-RDF graph libraries.
See <https://derwen.ai/docs/kgl/concepts/#subgraph>

Core feature areas include:

  * label encoding
  * visualization
  * graph algorithms
  * probabilistic graph inference
  * embedding
    """

    def __init__ (
        self,
        kg: KnowledgeGraph,
        *,
        preload: list = None,
        excludes: list = None,
        ) -> None:
        """
        """
        self.kg = kg

        if preload:
            self.id_list = preload
        else:
            self.id_list = []

        if excludes:
            self.excludes = excludes
        else:
            self.excludes = []


    def triples (
        self
        ) -> typing.Generator[RDF_Triple, None, None]:
        """
Iterator for the RDF triples to be included in the subgraph.
        """
        for s, p, o in self.kg.rdf_graph():
            if not p in self.excludes:
                yield s, p, o


    def transform (
        self,
        node: NodeLike,
        ) -> int:
        """
Label encoding: return a unique integer ID for the given graph node.
        """
        if not node:
            # null case
            return -1

        if not node in self.id_list:
            self.id_list.append(node)

        return self.id_list.index(node)


    def inverse_transform (
        self,
        id: int,
        ) -> NodeLike:
        """
Label encoding: return the graph node corresponding to a unique integer ID.
        """
        if id < 0:
            return None

        return self.id_list[id]


    def get_name (
        self,
        node: RDF_Node,
        ) -> str:
        """
Produce a human-readable label from an RDF node.
        """
        return node.n3(self.kg.rdf_graph().namespace_manager)


    ######################################################################
    ## visualization
    ##
    ## Automated Network Graph: The triples describing relationships
    ## between entities can be ingested into graph visualization tools
    ## to extend or create an analyst's account-specific network
    ## model.

    def pyvis_style_node (
        self,
        g: pyvis.network.Network,
        node_id: int,
        label: str,
        *,
        style: dict = None,
        ) -> None :
        """
        """
        if not style:
            style = {}

        prefix = label.split(":")[0]

        if prefix in style:
            g.add_node(
                node_id,
                label=label,
                title=label,
                color=style[prefix]["color"],
                size=style[prefix]["size"],
            )
        else:
            g.add_node(node_id, label=label, title=label)


    def vis_pyvis (
        self,
        *,
        notebook: bool = False,
        style: dict = None,
        ) -> pyvis.network.Network:
        """
This is one example; you may need to copy and replicate to construct the graph design you need.
See <https://pyvis.readthedocs.io/>
        """
        g = pyvis.network.Network(notebook=notebook)

        if not style:
            style = {}

        for s, p, o in self.triples():
            # label the subject
            s_label = s.n3(self.kg.rdf_graph().namespace_manager)
            s_id = self.transform(s_label)
            self.pyvis_style_node(g, s_id, s_label, style=style)

            # label the object
            if isinstance(o, rdflib.term.Literal):
                o_label = str(o.toPython())
            else:
                o_label = o.n3(self.kg.rdf_graph().namespace_manager)

            o_id = self.transform(o_label)
            self.pyvis_style_node(g, o_id, o_label, style=style)

            # label the predicate
            p_label = p.n3(self.kg.rdf_graph().namespace_manager)
            g.add_edge(s_id, o_id, label=p_label)

        return g
