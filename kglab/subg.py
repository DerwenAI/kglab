#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

######################################################################
## subgraph transforms for visualization, graph algorithms, etc.

from kglab import KnowledgeGraph
from kglab.topo import Measure
from kglab.pkg_types import NodeLike, RDF_Node, RDF_Triple
from kglab.util import get_gpu_count

from icecream import ic  #  type: ignore # pylint: disable=W0611,E0401
from tqdm import tqdm  # type: ignore # pylint: disable=E0401
import pandas as pd  # type: ignore # pylint: disable=E0401
import pyvis.network  # type: ignore # pylint: disable=E0401
import networkx as nx  # type: ignore # pylint: disable=E0401
import torch  # type: ignore # pylint: disable=E0401
import typing

if get_gpu_count() > 0:
    import cudf  # type: ignore # pylint: disable=E0401
    import cugraph # type: ignore # pylint: disable=E0401,W0611 # lgtm[py/unused-import]


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
Transforms a node in an RDF graph to an integer value, as a unique identifier with the closure of a specific use case.
The integer value can then be used to index into an *algebraic object* such as a *matrix* or *tensor*.
Effectvely, this method is similar to a [`sklearn.preprocessing.LabelEncoder`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html).

Notes:

  * the integer value is **not** a [*uuid*](https://tools.ietf.org/html/rfc4122) since it is only defined within the closure of a specific use case.
  * a special value `-1` represents the unique identifier for a non-existent (`None`) node, which is useful in data structures that have optional placeholders for links to RDF nodes

    node:
a node in the RDF graph

    returns:
a unique identifier (an integer index) for the `node` in the RDF graph
        """
        # NB: workaround to avoid Python calling `node.__nonzero__()`
        # https://amir.rachum.com/blog/2012/08/25/you-cant-handle-the-truth/

        # otherwise, if `node` is a literal (e.g., an int, float, string,
        # duration, etc.) that evals to any zero value then this function
        # would behave incorrectly

        if node is None:
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
Inverse transform from an intenger to a node in the RDF graph, using the identifier as an index into the node vector.

    id:
an integer index for the `node` in the RDF graph

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
    _SRC_DST_MAP: typing.List[str] = ["subject", "object"]

    def __init__ (
        self,
        kg: KnowledgeGraph,
        sparql: str,
        *,
        bindings: dict = None,
        src_dst: typing.List[str] = None,
        ) -> None:
        """
Constructor for creating and manipulating a *subgraph* as a [*matrix*](https://mathworld.wolfram.com/AdjacencyMatrix.html),
projecting from an RDF graph represented by a `KnowledgeGraph` object.

    kg:
the source RDF graph

    sparql:
text for a SPARQL query that yields pairs to project into the *subgraph*; by default this expects the query to return bindings for `subject` and `object` nodes in the RDF graph

    bindings:
initial variable bindings

    src_dst:
an optional map to override the  `subject` and `object` bindings expected in the SPARQL query results; defaults to `None`
        """
        super().__init__(kg=kg)
        self.sparql = sparql
        self.bindings:typing.Optional[dict] = bindings

        if src_dst:
            self.src_dst: typing.List[str] = src_dst
        else:
            self.src_dst = self._SRC_DST_MAP


    def build_df (
        self,
        *,
        show_symbols: bool = False,
        ) -> pd.DataFrame:
        """
Factory pattern to populate a [`pandas.DataFrame`](https://pandas.pydata.org/docs/reference/frame.html) object, using transforms in this subgraph.

Note: this method is primarily intended for [`cuGraph`](https://docs.rapids.ai/api/cugraph/stable/) support. Loading via a `DataFrame` is required – in lieu of using the `nx.add_node()` approach.
Therefore the support for representing *bipartite* graphs is still pending.

    show_symbols:
optionally, include the symbolic representation for each node; defaults to `False`

    returns:
the populated `DataFrame` object; uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled
        """
        col_names: typing.List[str] = [ "src", "dst", "src_sym", "dst_sym" ]
        row_iter = self.kg.query(self.sparql, bindings=self.bindings)

        if not show_symbols:
            col_names = col_names[:2]

            rows_list: typing.List[dict] = [
                {
                    col_names[0]: self.transform(row[self.src_dst[0]]),
                    col_names[1]: self.transform(row[self.src_dst[1]]),
                }
                for row in row_iter
                ]
        else:
            rows_list = [
                {
                    col_names[0]: self.transform(row[self.src_dst[0]]),
                    col_names[1]: self.transform(row[self.src_dst[1]]),
                    col_names[2]: self.n3fy(row[self.src_dst[0]]),
                    col_names[3]: self.n3fy(row[self.src_dst[1]]),
                }
                for row in row_iter
                ]

        if self.kg.use_gpus:
            df = cudf.DataFrame(rows_list, columns=col_names)
        else:
            df = pd.DataFrame(rows_list, columns=col_names)

        return df


    def build_nx_graph (
        self,
        nx_graph: nx.DiGraph,
        *,
        bipartite: bool = False,
        ) -> nx.DiGraph:
        """
Factory pattern to populate a [`networkx.DiGraph`](https://networkx.org/documentation/latest/reference/classes/digraph.html) object, using transforms in this subgraph.
See <https://networkx.org/>

    nx_graph:
pass in an unpopulated [`networkx.DiGraph`](https://networkx.org/documentation/latest/reference/classes/digraph.html) object; must be a [`cugraph.DiGraph`](https://docs.rapids.ai/api/cugraph/stable/api.html#digraph) if GPUs are enabled

    bipartite:
flag for whether the `(subject, object)` pairs should be partitioned into *bipartite sets*, in other words whether the *adjacency matrix* is symmetric; ignored if GPUs are enabled

    returns:
the populated `NetworkX` graph object; uses the [RAPIDS `cuGraph` library](https://docs.rapids.ai/api/cugraph/stable/) if GPUs are enabled
        """
        if self.kg.use_gpus:
            df = self.build_df()
            nx_graph.from_cudf_edgelist(df, source="src", destination="dst")
        else:
            for row in self.kg.query(self.sparql, bindings=self.bindings):
                s_id = self.transform(row[self.src_dst[0]])
                s_label = self.n3fy(row[self.src_dst[0]])

                o_id = self.transform(row[self.src_dst[1]])
                o_label = self.n3fy(row[self.src_dst[1]])

                if bipartite:
                    nx_graph.add_node(s_id, label=s_label, bipartite=0)
                    nx_graph.add_node(o_id, label=o_label, bipartite=1)
                else:
                    nx_graph.add_node(s_id, label=s_label)
                    nx_graph.add_node(o_id, label=o_label)

                nx_graph.add_edge(s_id, o_id)

        return nx_graph


    def build_ig_graph (
        self,
        ig_graph: typing.Any,
        ) -> typing.Any:
        """
Factory pattern to populate an [`igraph.Graph`](https://igraph.org/python/doc/igraph.Graph-class.html) object, using transforms in this subgraph.
See <https://igraph.org/python/doc/>

Note that `iGraph` is somewhat notorious for being quite difficult to install correctly across a wide range of different platforms and environments.
Consequently this has been removed from being a dependency for `kglab`; to use `iGraph` please install and import it separately.

    ig_graph:
pass in an unpopulated [`igraph.Graph`](https://igraph.org/python/doc/igraph.Graph-class.html) object

    returns:
the populated  `iGraph` graph object
        """
        measure = Measure()
        measure.measure_graph(self.kg)
        keyset = measure.get_keyset(incl_pred=False)

        ig_graph.add_vertices(n=keyset)

        for row in self.kg.query(self.sparql, bindings=self.bindings):
            s_id = self.transform(row[self.src_dst[0]])
            o_id = self.transform(row[self.src_dst[1]])
            ig_graph.add_edges([ (s_id, o_id,) ])

        ig_graph.vs["label"] = ig_graph.vs["name"] # pylint: disable=E1136,E1137
        return ig_graph


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


    def as_tensor_edges (
        self
        ) -> typing.Generator[typing.List[int], None, None]:
        """
Iterator for enumerating the edges connecting to each predicate in the
subgraph, to be used to represent the KG in `PyTorch`.

    yields:
a subject and object edge for each predicate, in tensor representation
        """
        for s, p, o in self.as_tuples():
            s_label = self.n3fy(s)
            s_id = self.transform(s_label)

            p_label = self.n3fy(p)
            p_id = self.transform(p_label)

            o_label = self.n3fy(o)
            o_id = self.transform(o_label)

            yield [s_id, o_id, 2 * p_id]
            yield [o_id, s_id, 2 * p_id + 1]


    def as_tensor (
        self,
        *,
        quiet: bool = True,
        ) -> torch.Tensor:
        """
Represents the KG as a PyTorch [`Tensor`](https://pytorch.org/docs/stable/tensors.html),
loaded from an edge list where each predicate has edges connecting to
its subject and object.

    quiet:
boolean flag to disable `tqdm` progress bar calculation and output

    returns:
the loaded tensor object
        """
        edge_list: list = [
            edge_tuple
            for edge_tuple in tqdm(self.as_tensor_edges(), disable=quiet)  # pylint: disable=R1721
            ]

        tensor = torch.tensor(edge_list, dtype=torch.long).t().contiguous()  # pylint: disable=E1101,E1102
        return tensor


    ######################################################################
    ## visualization
    ##
    ## Automated Network Graph: The triples describing relationships
    ## between entities can be ingested into graph visualization tools
    ## to extend or create an analyst's account-specific network
    ## model.

    def pyvis_style_node ( # pylint: disable=R0201
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

    returns:
a `PyVis` network object
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
