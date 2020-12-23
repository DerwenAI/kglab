#!/usr/bin/env python
# encoding: utf-8

from rdflib import plugin  # type: ignore
from rdflib.serializer import Serializer  # type: ignore
from rdflib.plugin import register, Parser, Serializer  # type: ignore
import rdflib  # type: ignore
# NB: while `plugin` and `Serializer` aren't used directly, loading
# them explicitly here causes them to become registered in `rdflib`
register("json-ld", Parser, "rdflib_jsonld.parser", "JsonLDParser")
register("json-ld", Serializer, "rdflib_jsonld.serializer", "JsonLDSerializer")

from collections import defaultdict, deque
from collections.abc import Collection
import dateutil.parser as dup
import datetime as dt
import GPUtil  # type: ignore
import json
import math
import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore
import numpy as np  # type: ignore
import owlrl  # type: ignore
import pandas as pd  # type: ignore
import pathlib
import pyarrow as pa  # type: ignore
import pyarrow.parquet as pq  # type: ignore
import pyshacl  # type: ignore
import pyvis.network  # type: ignore
import random
import typing


######################################################################
## utilities

def stripe_column (values: list, bins: int) -> np.ndarray:
    """stripe a column: interpolate quantiles to discrete indexes"""
    s = pd.Series(values)
    q = s.quantile(bins, interpolation="nearest")

    try:
        stripe = np.digitize(values, q) - 1
        return stripe
    except ValueError as e:
        # should never happen?
        print("ValueError:", str(e), values, s, q, bins)
        raise


def calc_quantile_bins (num_rows: int) -> np.ndarray:
    """calculate the number of bins to use for a quantile stripe"""
    granularity = max(round(math.log(num_rows) * 4), 1)
    return np.linspace(0, 1, num=granularity, endpoint=True)


def rms (values: list) -> float:
    """calculate a root mean square"""
    numer = sum([x for x in map(lambda x: float(x)**2.0, values)])
    denom = float(len(values))
    return math.sqrt(numer / denom)


######################################################################
## main KG class definition

PathLike = typing.TypeVar("PathLike", str, pathlib.Path)

RDF_Node = typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
RDF_Triple = typing.Tuple[RDF_Node, RDF_Node, RDF_Node]
NodeLike = typing.TypeVar("NodeLike", typing.Optional[str], RDF_Node)

ConjunctiveLike = typing.Union[rdflib.ConjunctiveGraph, rdflib.Dataset]
GraphLike = typing.Union[ConjunctiveLike, rdflib.Graph]


class KnowledgeGraph (object):
    DEFAULT_NAMESPACES: dict = {
        "dct":	"http://purl.org/dc/terms/",
        "owl":	"http://www.w3.org/2002/07/owl#",
        "rdf":	"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs":	"http://www.w3.org/2000/01/rdf-schema#",
        "skos":	"http://www.w3.org/2004/02/skos/core#",
        "xsd":	"http://www.w3.org/2001/XMLSchema#",
        }


    def __init__ (self,
                  name: str = "KGlab",
                  base_uri: str = None,
                  language: str = "en",
                  namespaces: dict = {},
                  graph: typing.Optional[GraphLike] = None
                 ) -> None:
        self.name = name
        self.base_uri = base_uri
        self.language = language
        self.gpus = GPUtil.getGPUs()

        if not graph:
            self._g = rdflib.Graph()
        else:
            self._g = graph

        self._ns: dict = {}
        self.merge_ns({ **self.DEFAULT_NAMESPACES, **namespaces })


    ######################################################################
    ## namespace management and graph building
    ##
    ## Using and building ontologies: To attribute characteristics and
    ## relationships to well-understood entities, we want to research
    ## the implementation of existing top-level ontologies. In such an
    ## implementation, however, we would not want to prevent mid-level
    ## and domain specific ontologies from being developed organically
    ## for classification with greater precision and nuance. We want
    ## to explore ways to perform entity recognition and
    ## entity-resolution probabilistically rather than by strict
    ## rulesets.

    def merge_ns (self, ns_set: dict) -> None:
        for prefix, uri in ns_set.items():
            self.add_ns(prefix, uri)


    def add_ns (self, prefix: str, uri: str) -> None:
        """Since rdflib converts Namespace bindings to URIRef, we'll keep references to them"""
        self._ns[prefix] = rdflib.Namespace(uri)
        self._g.namespace_manager.bind(prefix, self._ns[prefix])


    def get_ns (self, prefix: str) -> rdflib.Namespace:
        return self._ns[prefix]


    def get_context (self) -> dict:
        """return a context needed for JSON-LD serialization"""
        context: dict = {
            "@language": self.language,
            }

        if self.base_uri:
            context["@vocab"] = self.base_uri

        for prefix, uri in self._ns.items():
            if uri != self.base_uri:
                context[prefix] = uri

        return context


    def add (self, s: RDF_Node, p: RDF_Node, o: RDF_Node) -> None:
        self._g.add((s, p, o,))


    @classmethod
    def type_date (cls, date: str, tz: dict) -> rdflib.Literal:
        """input `date` should be interpretable as having a local timezone"""
        date_tz = dup.parse(date, tzinfos=tz)
        return rdflib.Literal(date_tz, datatype=rdflib.XSD.dateTime)


    ######################################################################
    ## serialization
    ##
    ## Format and software agnostic: We are interested in technology
    ## that will not be a barrier to widespread use. We want to allow
    ## the export of the entity triples in a variety of formats, at
    ## the most basic level as a csv, so that an analyst can load the
    ## results into their system of choice. By prioritizing
    ## non-proprietary, universal formats the results can be easily
    ## integrated into several of the existing tools for network
    ## graphing.

    def load_ttl (self,
                  path: PathLike,
                  format: str = "n3",
                  encoding: str = "utf-8"
                 ) -> None:
        if isinstance(path, pathlib.Path):
            filename = path.as_posix()
        else:
            filename = path

        self._g.parse(filename, format=format, encoding=encoding)


    def load_ttl_text (self,
                       data: typing.AnyStr,
                       format: str = "n3",
                       encoding: str = "utf-8"
                      ) -> None:
        self._g.parse(data=data, format=format, encoding=encoding);


    def save_ttl (self,
                  path: PathLike,
                  format: str = "n3",
                  encoding: str = "utf-8"
                 ) -> None:
        if isinstance(path, pathlib.Path):
            filename = path.as_posix()
        else:
            filename = path

        self._g.serialize(destination=filename, format=format, encoding=encoding)


    def save_ttl_text (self,
                       format: str = "n3",
                       encoding: str = "utf-8"
                      ) -> str:
        return self._g.serialize(destination=None, format=format, encoding=encoding).decode(encoding) 


    def load_jsonld (self,
                     path: PathLike,
                     encoding: str = "utf-8"
                    ) -> None:
        with open(path, "r", encoding=encoding) as f:
            data = json.load(f)
            self._g.parse(data=json.dumps(data), format="json-ld", encoding=encoding)


    def save_jsonld (self,
                     path: PathLike,
                     encoding: str = "utf-8"
                    ) -> None:
        data = self._g.serialize(
            format = "json-ld",
            context = self.get_context(),
            indent = 2,
            encoding = encoding
            )

        with open(path, "wb") as f:
            f.write(data)


    def load_parquet (self,
                      path: PathLike
                     ) -> None:
        df = pq.read_pandas(path).to_pandas()

        for index, row in df.iterrows():
            triple = "{} {} {} .".format(row[0], row[1], row[2])
            self._g.parse(data=triple, format="n3")


    def save_parquet (self,
                      path: PathLike,
                      compression: str = "gzip"
                     ) -> None:
        rows_list = [ {"s": s.n3(), "p": p.n3(), "o": o.n3()} for s, p, o in self._g ]
        df = pd.DataFrame(rows_list, columns=("s", "p", "o"))
        table = pa.Table.from_pandas(df)
        pq.write_table(table, path, use_dictionary=True, compression=compression)


    ######################################################################
    ## SPARQL queries

    def query (self,
               sparql: str,
               bindings: dict = {}
              ) -> typing.Iterable:
        for row in self._g.query(sparql, initBindings=bindings):
            yield row


    @classmethod
    def n3fy (cls, 
              d: dict, 
              nm: rdflib.namespace.NamespaceManager, 
              pythonify: bool = True
             ) -> dict:
        if not pythonify:
            return dict([ (k, v.n3(nm),) for k, v in d.items() ])
        else:
            items: list = []

            for k, v in d.items():
                if isinstance(v, rdflib.term.Literal):
                    items.append([ k, v.toPython() ])
                else:
                    items.append([ k, v.n3(nm) ])

            return dict(items)


    def query_as_df (self,
                     sparql: str,
                     bindings: dict = {},
                     simplify: bool = True,
                     pythonify: bool = True
                    ) -> pd.DataFrame:
        iter = self._g.query(sparql, initBindings=bindings)

        if simplify:
            nm = self._g.namespace_manager
            df = pd.DataFrame([ self.n3fy(row.asdict(), nm, pythonify) for row in iter ])
        else:
            df = df = pd.DataFrame([ row.asdict() for row in iter ])
        
        return df


    ######################################################################
    ## SHACL validation

    def validate (self,
                  shacl_graph: typing.Optional[typing.Union[GraphLike, typing.AnyStr]] = None,
                  shacl_graph_format: typing.Optional[str] = None,
                  ont_graph: typing.Optional[typing.Union[GraphLike, typing.AnyStr]] = None,
                  ont_graph_format: typing.Optional[str] = None,
                  advanced: typing.Optional[bool] = False,
                  inference: typing.Optional[str] = None,
                  abort_on_error: typing.Optional[bool] = None,
                  serialize_report_graph: typing.Optional[str] = "n3",
                  debug: bool = False,
                  **kwargs: typing.Any
                 ):

        conforms, report_graph_data, report_text = pyshacl.validate(
            self._g,
            shacl_graph=shacl_graph,
            shacl_graph_format=shacl_graph_format,
            ont_graph=ont_graph,
            ont_graph_format=ont_graph_format,
            advanced=advanced,
            inference=inference,
            abort_on_error=abort_on_error,
            debug=debug,
            serialize_report_graph=serialize_report_graph,
            *kwargs,
            )
       
        namespaces = {
            "sh":     "http://www.w3.org/ns/shacl#",
            "schema": "http://schema.org/",
        }

        g = rdflib.Graph()
        g.parse(data=report_graph_data, format="n3", encoding="utf-8")
        report_graph = KnowledgeGraph(graph=g, name="report graph", namespaces=namespaces)

        return conforms, report_graph, report_text


    ######################################################################
    ## SKOS inference
    ## adapted from `skosify` https://github.com/NatLibFi/Skosify
    ## it wasn't being updated regularly, but may be integrated again

    def infer_skos_related (self) -> None:
        """Make sure that skos:related is stated in both directions (S23)."""
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.related):
            self._g.add((o, _skos.related, s))


    def infer_skos_topConcept (self) -> None:
        """Infer skos:topConceptOf/skos:hasTopConcept (S8) and skos:inScheme (S7)."""
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.hasTopConcept):
            self._g.add((o, _skos.topConceptOf, s))

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self._g.add((o, _skos.hasTopConcept, s))

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self._g.add((s, _skos.inScheme, o))


    def infer_skos_hierarchical (self, narrower: bool = True) -> None:
        """Infer skos:broader/skos:narrower (S25) but only keep skos:narrower on request.
        :param bool narrower: If set to False, skos:narrower will not be added,
        but rather removed.
        """
        _skos = self.get_ns("skos")

        if narrower:
            for s, o in self._g.subject_objects(_skos.broader):
                self._g.add((o, _skos.narrower, s))

        for s, o in self._g.subject_objects(_skos.narrower):
            self._g.add((o, _skos.broader, s))

            if not narrower:
                self._g.remove((s, _skos.narrower, o))


    def infer_skos_transitive (self, narrower: bool = True) -> None:
        """Perform transitive closure inference (S22, S24)."""
        _skos = self.get_ns("skos")

        for conc in self._g.subjects(self.get_ns("rdf").type, _skos.Concept):
            for bt in self._g.transitive_objects(conc, _skos.broader):
                if bt == conc:
                    continue

                self._g.add((conc, _skos.broaderTransitive, bt))

                if narrower:
                    self._g.add((bt, _skos.narrowerTransitive, conc))


    def infer_skos_symmetric_mappings (self, related: bool = True) -> None:
        """Ensure that the symmetric mapping properties (skos:relatedMatch,
        skos:closeMatch and skos:exactMatch) are stated in both directions (S44).
        :param bool related: Add the skos:related super-property for all
            skos:relatedMatch relations (S41).
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.relatedMatch):
            self._g.add((o, _skos.relatedMatch, s))

            if related:
                self._g.add((s, _skos.related, o))
                self._g.add((o, _skos.related, s))

        for s, o in self._g.subject_objects(_skos.closeMatch):
            self._g.add((o, _skos.closeMatch, s))

        for s, o in self._g.subject_objects(_skos.exactMatch):
            self._g.add((o, _skos.exactMatch, s))


    def infer_skos_hierarchical_mappings (self, narrower: bool = True) -> None:
        """Infer skos:broadMatch/skos:narrowMatch (S43) and add the super-properties
        skos:broader/skos:narrower (S41).
        :param bool narrower: If set to False, skos:narrowMatch will not be added,
            but rather removed.
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.broadMatch):
            self._g.add((s, _skos.broader, o))

            if narrower:
                self._g.add((o, _skos.narrowMatch, s))
                self._g.add((o, _skos.narrower, s))

        for s, o in self._g.subject_objects(_skos.narrowMatch):
            self._g.add((o, _skos.broadMatch, s))
            self._g.add((o, _skos.broader, s))

            if narrower:
                self._g.add((s, _skos.narrower, o))
            else:
                self._g.remove((s, _skos.narrowMatch, o))


    def infer_rdfs_classes (self) -> None:
        """Perform RDFS subclass inference.
        Mark all resources with a subclass type with the upper class."""
        _rdfs = self.get_ns("rdfs")

        # find out the subclass mappings
        upperclasses: typing.Dict[typing.Any, typing.Any] = {}  # key: class val: set([superclass1, superclass2..])

        for s, o in self._g.subject_objects(_rdfs.subClassOf):
            upperclasses.setdefault(s, set())

            for uc in self._g.transitive_objects(s, _rdfs.subClassOf):
                if uc != s:
                    upperclasses[s].add(uc)

        # set the superclass type information for subclass instances
        for s, ucs in upperclasses.items():
            #logging.debug("setting superclass types: %s -> %s", s, str(ucs))
            for res in self._g.subjects(self.get_ns("rdf").type, s):
                for uc in ucs:
                    self._g.add((res, self.get_ns("rdf").type, uc))


    def infer_rdfs_properties (self) -> None:
        """Perform RDFS subproperty inference.
        Add superproperties where subproperties have been used."""
        _rdfs = self.get_ns("rdfs")

        # find out the subproperty mappings
        superprops: typing.Dict[typing.Any, typing.Any] = {}  # key: property val: set([superprop1, superprop2..])

        for s, o in self._g.subject_objects(_rdfs.subPropertyOf):
            superprops.setdefault(s, set())

            for sp in self._g.transitive_objects(s, _rdfs.subPropertyOf):
                if sp != s:
                    superprops[s].add(sp)

        # add the superproperty relationships
        for p, sps in superprops.items():
            #logging.debug("setting superproperties: %s -> %s", p, str(sps))
            for s, o in self._g.subject_objects(p):
                for sp in sps:
                    self._g.add((s, sp, o))

                    
    def infer_rdfs_closure (self) -> None:
        """add inferred triples from RDFS based on OWL-RL,
        see https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib
        """
        rdfs = owlrl.RDFSClosure.RDFS_Semantics(self._g, False, False, False)
        rdfs.closure()
        rdfs.flush_stored_triples()


    def infer_owlrl_closure (self) -> None:
        """add inferred triples from OWL based on OWL-RL,
        see https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib
        """
        owl = owlrl.OWLRL_Semantics(self._g, False, False, False)
        owl.closure()
        owl.flush_stored_triples()

        
######################################################################
## graph topology

Census_Item = typing.TypeVar("Census_Item", str, RDF_Node)
Census_Dyad_Tally = typing.Tuple[pd.DataFrame, dict]


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

    def get_keyset (self) -> typing.List[str]:
        keys = self.s_gen.get_keyset().union(self.p_gen.get_keyset().union(self.o_gen.get_keyset()))
        return sorted(list(keys))


######################################################################
## subgraph transforms for visualization, graph algorithms, etc.

class Subgraph (object):
    def __init__ (self, kg: KnowledgeGraph, preload: list = [], excludes: list = []) -> None:
        self.kg = kg
        self.id_list = preload
        self.excludes = excludes

    def triples (self) -> typing.Generator[RDF_Triple, None, None]:
        """iterator for triples to include in the subgraph"""
        for s, p, o in self.kg._g:
            if not p in self.excludes:
                yield s, p, o

    def transform (self, node: NodeLike) -> int:
        """label encoding: return a unique integer ID for the given graph node"""
        if not node:
            # null case
            return -1
        elif not node in self.id_list:
            self.id_list.append(node)

        return self.id_list.index(node)

    def inverse_transform (self, id: int) -> NodeLike:
        """label encoding: return the graph node corresponding to a unique integer ID"""
        if id < 0:
            return None
        else:
            return self.id_list[id]
    
    def get_name (self, node: RDF_Node) -> str:
        """return a human-readable label for an RDF node"""
        return node.n3(self.kg._g.namespace_manager)


    ######################################################################
    ## visualization
    ##
    ## Automated Network Graph: The triples describing relationships
    ## between entities can be ingested into graph visualization tools
    ## to extend or create an analyst's account-specific network
    ## model.

    def pyvis_style_node (self, g: pyvis.network.Network, node_id: int, label: str, style: dict = {}) -> None :
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


    def vis_pyvis (self, notebook: bool = False, style: dict = {}) -> pyvis.network.Network:
        """
        https://pyvis.readthedocs.io/
        this is one example; you may need to copy and replicate 
        to construct the graph design you need
        """
        g = pyvis.network.Network(notebook=notebook)

        for s, p, o in self.triples():
            # label the subject
            s_label = s.n3(self.kg._g.namespace_manager)
            s_id = self.transform(s_label)
            self.pyvis_style_node(g, s_id, s_label, style=style)

            # lable the object
            if isinstance(o, rdflib.term.Literal):
                o_label = str(o.toPython())
            else:
                o_label = o.n3(self.kg._g.namespace_manager)

            o_id = self.transform(o_label)
            self.pyvis_style_node(g, o_id, o_label, style=style)

            # label the predicate
            p_label = p.n3(self.kg._g.namespace_manager)
            g.add_edge(s_id, o_id, label=p_label)

        return g


######################################################################
## Shape Prediction

SPARQL_Bindings = typing.Tuple[str, dict]

SerializedEvoEdge = typing.Tuple[int, int]
SerializedEvoNode = typing.Tuple[int, typing.List[SerializedEvoEdge]]

Evolike = typing.TypeVar("Evolike", int, SerializedEvoNode)
SerializedEvoShape = typing.List[Evolike]

EvoShapeBoard = typing.List[SerializedEvoShape]
EvoShapeDistance = typing.Tuple[int, int, float]


class EvoShapeNode (object):
    def __init__ (self, uri: str = None, terminal: bool = False) -> None:
        self.uri = uri
        self.terminal = terminal
        self.done = terminal # initially
        self.edges: typing.List[EvoShapeEdge] = []

    def serialize (self, subgraph: Subgraph) -> SerializedEvoNode:
        edge_list = sorted([ (subgraph.transform(e.pred), subgraph.transform(e.obj.uri),) for e in self.edges ])
        return subgraph.transform(self.uri), edge_list

    @classmethod
    def deserialize (cls, dat: SerializedEvoNode, subgraph: Subgraph, uri_map: dict, root_node: "EvoShapeNode" = None) -> "EvoShapeNode":
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
            
            edge = EvoShapeEdge(pred=subgraph.inverse_transform(p), obj=obj)
            node.edges.append(edge)

        return node


class EvoShapeEdge (typing.NamedTuple):
    pred: str
    obj: EvoShapeNode


class EvoShape (object):
    def __init__ (self, kg: KnowledgeGraph, measure: Measure) -> None:
        self.kg = kg
        self.measure = measure
        self.root = EvoShapeNode(uri=None)
        self.nodes = set([self.root])

    def add_link (self, s: RDF_Node, p: RDF_Node, o: RDF_Node) -> None:
        edge = EvoShapeEdge(pred=p, obj=o)
        s.edges.append(edge)
        self.nodes.add(o)
        
    def serialize (self, subgraph: Subgraph) -> SerializedEvoShape:
        """transform to ordinal format which can be serialized/deserialized with a consistent subgraph"""
        d: deque = deque(sorted([ n.serialize(subgraph) for n in self.nodes.difference({self.root}) ]))
        d.appendleft(self.root.serialize(subgraph))
        d.appendleft(self.get_cardinality())
        return list(d)

    def deserialize (self, dat_list: SerializedEvoShape, subgraph: Subgraph) -> dict:
        """replace shape definition with parsed content"""
        instances = dat_list.pop(0) # ignore
        uri_map: dict = {}
        self.nodes = set()

        root_dat = dat_list.pop(0)
        self.root = EvoShapeNode.deserialize(root_dat, subgraph, uri_map)
        self.nodes.add(self.root)

        for node_dat in dat_list:
            node = EvoShapeNode.deserialize(node_dat, subgraph, uri_map, root_node=self.root)
            self.nodes.add(node)

        return uri_map

    def get_rdf (self) -> typing.List[str]:
        """for debugging purposes: by definition, a shape is not fully qualified"""
        rdf_list: typing.List[str] = []
        
        for node in list(self.nodes):          
            if not node.uri:
                b = rdflib.BNode()
                subj = str(b.n3())
            else:
                subj = rdflib.term.URIRef(node.uri).n3(self.kg._g.namespace_manager)

            for edge in node.edges:
                pred = rdflib.term.URIRef(edge.pred).n3(self.kg._g.namespace_manager)
                obj = rdflib.term.URIRef(edge.obj.uri).n3(self.kg._g.namespace_manager)
                triple = "{} {} {} .".format(subj, pred, obj)
                rdf_list.append(triple)

        return rdf_list


    def get_sparql (self) -> SPARQL_Bindings:
        var_list: typing.List[str] = []
        clauses: typing.List[str] = []
        uri_map: dict = {}
        bindings: dict = {}
        node_list = list(self.nodes)
        
        for node_num in range(len(node_list)):
            node = node_list[node_num]

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

    def get_cardinality (self) -> int:
        sparql, bindings = self.get_sparql()
        return len(list(self.kg.query(sparql, bindings=bindings)))

    def calc_distance (self, other: "EvoShape") -> float:
        n0 = set([ n.uri for n in self.nodes ])
        n1 = set([ n.uri for n in other.nodes ])
        distance = len(n0.intersection(n1)) / float(max(len(n0), len(n1)))
        return distance


class ShapeFactory (object):
    def __init__ (self, kg: KnowledgeGraph, measure: Measure) -> None:
        self.kg = kg
        self.measure = measure
        self.subgraph = Subgraph(kg, preload=measure.get_keyset())

        # enum action space of possible RDF types (i.e., "superclasses")
        type_sparql = "SELECT DISTINCT ?n WHERE {[] rdf:type ?n}"
        self.type_list = [ r.n for r in kg.query(type_sparql) ]

    def new_shape (self, type_uri: str = None) -> EvoShape:
        es = EvoShape(self.kg, self.measure)

        if not type_uri:
            ## RANDOM CHOICE => OBS
            ## TODO: generate from gamma dist -- or specify
            type_uri = random.choice(self.type_list)
    
        type_node = EvoShapeNode(type_uri, terminal=True)
        es.add_link(es.root, rdflib.RDF.type, type_node)
        return es


class Leaderboard (object):
    COLUMNS: typing.List[str] = ["instances", "nodes", "distance", "rank", "shape"]

    def __init__ (self) -> None:
        self.df = pd.DataFrame([], columns=self.COLUMNS)

    def get_board (self) -> EvoShapeBoard:
        """return a list of shapes, i.e., dataframe without metrics"""
        return list(self.df["shape"].to_numpy())
    
    @classmethod
    def compare (cls, shape: SerializedEvoShape, board: EvoShapeBoard) -> EvoShapeDistance:
        """compare shape distances"""
        n0 = set([n for n, e in shape[1:]])
        
        if len(board) < 2:
            min_dist = 0.0
        else:
            distances: list = []
    
            for b in board:
                n1 = set([n for n, e in b[1:]])
                d = len(n0.intersection(n1)) / float(max(len(n0), len(n1)))
        
                if d < 1.0:
                    distances.append(d)

            min_dist = min(distances)

        return int(shape[0]), len(n0), min_dist

    @classmethod
    def insert (cls, shape: SerializedEvoShape, board: EvoShapeBoard) -> pd.DataFrame:
        """rank this shape within a new dataframe"""
        board.append(shape)
        df1 = pd.DataFrame([ cls.compare(s, board) for s in board ], columns=cls.COLUMNS[:3])

        # normalize by column
        df2 = df1.apply(lambda x: x/x.max(), axis=0)
        bins = calc_quantile_bins(len(df2.index))

        # stripe each column to approximate a pareto front
        stripes = [ stripe_column(values, bins) for _, values in df2.items() ]
        df3 = pd.DataFrame(stripes).T

        # rank based on RMS of striped indices per row
        df1["rank"] = df3.apply(lambda row: rms(row), axis=1)
        df1["shape"] = pd.Series(board, index=df1.index)

        # sort descending
        return df1.sort_values(by=["rank"], ascending=False)

    def get_position (self, shape: SerializedEvoShape) -> int:
        """return distance-from-bottom for the given shape"""
        return len(self.df.index) - list(self.df["shape"].to_numpy()).index(shape) - 1

    def add_shape (self, shape: SerializedEvoShape) -> int:
        """insert the given shape into the leaderboard, returning its position"""
        self.df = self.insert(shape, self.get_board())
        return self.get_position(shape)
