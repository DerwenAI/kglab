#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## subgraph transforms for visualization, graph algorithms, etc.

from kglab import KnowledgeGraph
from kglab.pkg_types import NodeLike, RDF_Node, RDF_Triple

import pyvis.network  # type: ignore
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
Constructor for creating and manipulating a *subgraph*, as a projection of an RDF graph represented by a `KnowledgeGraph` object.

    kg:
the RDF graph to project from

    preload:
an optional, pre-determined list to pre-load for the *label encoding*

    excludes:
a list of RDF predicates to exclude from projecting into the *subgraph*
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


    def transform (
        self,
        node: NodeLike,
        ) -> int:
        """
Tranform from a node in an RDF graph to a unique identifier, which can then be used in a matrix or tensor.
Effectvely, similar to the [`sklearn.preprocessing.LabelEncoder`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) –
by maintaining a node list.

Note that a special value `-1` represents the unique identifier for a null (`None`) node.
This is useful in data structures which have optional placeholders for links to RDF nodes.

     returns:
a unique identifier (an integer) for the `node` in the RDF graph
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
Inverse tranform from a unique identifier to a node in the RDF graph, using the indentifier as an index into the node list.

    returns:
node in the RDF graph
        """
        if id < 0:
            return None

        return self.id_list[id]


    def triples (
        self
        ) -> typing.Generator[RDF_Triple, None, None]:
        """
Iterator for the RDF triples to included in the subgraph.

    yields:
the RDF triples within the subgraph
        """
        for s, p, o in self.kg.rdf_graph():
            if not p in self.excludes:
                yield s, p, o


    def n3fy (
        self,
        node: RDF_Node,
        ) -> typing.Any:
        """
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize a node into a human-readable representation using N3 format.
This method provides a convenience, which in turn calls `KnowledgeGraph.n3fy()`

    node;
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

    returns:
text (or Python object) for the serialized node
        """
        return self.kg.n3fy(node)


    ######################################################################
    ## visualization
    ##
    ## Automated Network Graph: The triples describing relationships
    ## between entities can be ingested into graph visualization tools
    ## to extend or create an analyst's account-specific network
    ## model.

    def pyvis_style_node (
        self,
        pyvis_graph: pyvis.network.Network,
        node_id: int,
        label: str,
        *,
        style: dict = None,
        ) -> None :
        """
Adds a node into a [PyVis](https://pyvis.readthedocs.io/) network, optionally with styling info.

    pyvis_graph:
the [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html?highlight=network#pyvis.network.Network) being used for *interactive visualization*

    node_id:
unique identifier for a node in the RDF graph

    label:
text label for the node

    style:
optional style dictionary
        """
        if not style:
            style = {}

        prefix = label.split(":")[0]

        if prefix in style:
            pyvis_graph.add_node(
                node_id,
                label=label,
                title=label,
                color=style[prefix]["color"],
                size=style[prefix]["size"],
            )
        else:
            pyvis_graph.add_node(
                node_id,
                label=label,
                title=label,
            )


    def build_pyvis_graph (
        self,
        *,
        notebook: bool = False,
        style: dict = None,
        ) -> pyvis.network.Network:
        """
Factory pattern to create a [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html?highlight=network#pyvis.network.Network) object, populated by transforms in this subgraph.
See <https://pyvis.readthedocs.io/>

    notebook:
flag for whether or not the interactive visualization will be generated within a notebook

    style:
optional style dictionary
        """
        pyvis_graph = pyvis.network.Network(notebook=notebook)

        if not style:
            style = {}

        for s, p, o in self.triples():
            # label the subject
            s_label = self.n3fy(s)
            s_id = self.transform(s_label)
            self.pyvis_style_node(pyvis_graph, s_id, s_label, style=style)

            # label the object
            o_label = str(self.n3fy(o))
            o_id = self.transform(o_label)
            self.pyvis_style_node(pyvis_graph, o_id, o_label, style=style)

            # label the predicate
            p_label = self.n3fy(p)
            pyvis_graph.add_edge(s_id, o_id, label=p_label)

        return pyvis_graph
