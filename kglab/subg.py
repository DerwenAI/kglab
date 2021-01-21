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
Base class for projection of an RDF graph into an *algebraic object* such as a *vector*, *matrix*, or *tensor* representation, to support integration with non-RDF graph libraries.
In other words, this class provides means to vectorize selected portions of a graph as a [*dimension*](https://mathworld.wolfram.com/Dimension.html).
See <https://derwen.ai/docs/kgl/concepts/#subgraph>

Features support several areas of use cases, including:

  * label encoding
  * vectorization (parallel processing)
  * graph algorithms
  * visualization
  * embedding (deep learning)
  * probabilistic graph inference (statistical relational learning)

The base case is where a *subset* of the nodes in the source RDF graph get represented as a *vector*, in the `node_vector` member.
This provides an efficient *index* on a constructed *dimension*, solely for the context of a specific use case.
    """

    def __init__ (
        self,
        kg: KnowledgeGraph,
        *,
        preload: list = None,
        ) -> None:
        """
Constructor for creating and manipulating a *subgraph* as a [*vector*](https://mathworld.wolfram.com/Vector.html),
projecting from an RDF graph represented by a `KnowledgeGraph` object.

    kg:
the source RDF graph

    preload:
an optional, pre-determined list to pre-load for *label encoding*
        """
        self.kg = kg

        if preload:
            self.node_vector = preload
        else:
            self.node_vector = []


    def transform (
        self,
        node: NodeLike,
        ) -> int:
        """
Tranforms a node in an RDF graph to an integer value, as a unique identifier with the closure of a specific use case.
The integer value can then be used to index into an *algebraic object* such as a *matrix* or *tensor*.
Effectvely, this method is similar to a [`sklearn.preprocessing.LabelEncoder`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html).

Notes:

  * the integer value is **not** a [*uuid*](https://tools.ietf.org/html/rfc4122) since it is only defined within the closure of a specific use case.
  * a special value `-1` represents the unique identifier for a non-existant (`None`) node, which is useful in data structures that have optional placeholders for links to RDF nodes

     returns:
a unique identifier (an integer index) for the `node` in the RDF graph
        """
        if not node:
            # null case
            return -1

        if not node in self.node_vector:
            self.node_vector.append(node)

        return self.node_vector.index(node)


    def inverse_transform (
        self,
        id: int,
        ) -> NodeLike:
        """
Inverse tranform from an intenger to a node in the RDF graph, using the indentifier as an index into the node vector.

    returns:
node in the RDF graph
        """
        if id < 0:
            return None

        return self.node_vector[id]


    def n3fy (
        self,
        node: RDF_Node,
        ) -> typing.Any:
        """
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize a node into a human-readable representation using N3 format.
This method provides a convenience, which in turn calls `KnowledgeGraph.n3fy()`

    node:
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

    returns:
text (or Python object) for the serialized node
        """
        return self.kg.n3fy(node)


class SubgraphMatrix (Subgraph):
    """
Projection of a RDF graph to a [*matrix*](https://mathworld.wolfram.com/AdjacencyMatrix.html) representation.
Typical use cases include integration with non-RDF graph libraries for *graph algorithms*.
    """

    def __init__ (
        self,
        kg: KnowledgeGraph,
        *,
        excludes: list = None,
        ) -> None:
        """
Constructor for creating and manipulating a *subgraph* as a [*matrix*](https://mathworld.wolfram.com/AdjacencyMatrix.html),
projecting from an RDF graph represented by a `KnowledgeGraph` object.

    kg:
the source RDF graph

    excludes:
a list of RDF predicates to exclude from projection into the *subgraph*
        """
        super().__init__(kg=kg)

        if excludes:
            self.excludes = excludes
        else:
            self.excludes = []


class SubgraphTensor (Subgraph):
    """
Projection of a RDF graph to a [*tensor*](https://mathworld.wolfram.com/Tensor.html) representation.
Typical use cases include integration with non-RDF graph libraries for *visualization* and *embedding*.
    """

    def __init__ (
        self,
        kg: KnowledgeGraph,
        *,
        excludes: list = None,
        ) -> None:
        """
Constructor for creating and manipulating a *subgraph* as a [*tensor*](https://mathworld.wolfram.com/Tensor.html),
projecting from an RDF graph represented by a `KnowledgeGraph` object.

    kg:
the source RDF graph

    excludes:
a list of RDF predicates to exclude from projection into the *subgraph*
        """
        super().__init__(kg=kg)

        if excludes:
            self.excludes = excludes
        else:
            self.excludes = []


    def as_tuples (
        self
        ) -> typing.Generator[RDF_Triple, None, None]:
        """
Iterator for enumerating the RDF triples to be included in the subgraph, used in factory patterns for visualizations.
This allows a kind of *lazy evaluation*.

    yields:
the RDF triples within the subgraph
        """
        for s, p, o in self.kg.rdf_graph():
            if not p in self.excludes:
                yield s, p, o


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

        for s, p, o in self.as_tuples():
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
