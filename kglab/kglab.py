#!/usr/bin/env python
# encoding: utf-8

from rdflib import plugin
from rdflib.serializer import Serializer
from rdflib.plugin import register, Parser, Serializer
import rdflib
# NB: while `plugin` and `Serializer` aren't used directly, loading
# them explicitly here causes them to become registered in `rdflib`
register("json-ld", Parser, "rdflib_jsonld.parser", "JsonLDParser")
register("json-ld", Serializer, "rdflib_jsonld.serializer", "JsonLDSerializer")

from collections import defaultdict
from typing import NamedTuple
import dateutil.parser as dup
import json
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import pathlib
import pyarrow as pa
import pyarrow.parquet as pq
import pyvis.network
import pyshacl
import random


######################################################################
## Shape Prediction

class EvoShapeNode (object):
    def __init__ (self, uri=None, terminal=False):
        self.uri = uri
        self.terminal = terminal
        self.done = terminal # initially
        self.edges = []


class EvoShapeEdge(NamedTuple):
    pred: str
    obj: EvoShapeNode


class EvoShape (object):
    def __init__ (self, kg, measure):
        self.kg = kg
        self.measure = measure
        self.root = EvoShapeNode(uri=None)
        self.nodes = set([self.root])

    def add_link (self, s, p, o):
        edge = EvoShapeEdge(pred=p, obj=o)
        s.edges.append(edge)
        self.nodes.add(o)
        
    def get_sparql (self):
        var_list = []
        clauses = []
        bindings = {}
        node_list = list(self.nodes)
        
        for node_num in range(len(node_list)):
            node = node_list[node_num]

            # name the subject
            if not node.uri:
                subj = "?v{}".format(node_num)
                var_list.append(subj)
            else:
                subj = "?node{}".format(node_num)
                bindings[subj] = rdflib.URIRef(node.uri)

            # generate a clause for each tuple
            pred_name = {}
            
            for edge_num in range(len(node.edges)):
                edge = node.edges[edge_num]

                if edge.pred in pred_name:
                    pred = pred_name[edge.pred]
                else:
                    pred = "?pred{}".format(edge_num)
                    pred_name[edge.pred] = pred

                bindings[pred] = rdflib.URIRef(edge.pred)

                obj = "?obj{}".format(edge_num)
                bindings[obj] = rdflib.URIRef(edge.obj.uri)

                clauses.append(" ".join([ subj, pred, obj ]))

        sparql = "SELECT DISTINCT {} WHERE {{ {} }}".format(" ".join(var_list), " . ".join(clauses))
        return sparql, bindings

    def get_rank_vector (self):
        nodes = len(list(self.nodes))
        edges = sum([ len(n.edges) for n in self.nodes ])

        sparql, bindings = self.get_sparql()
        instances = len(list(self.kg.query(sparql, bindings=bindings)))
        return nodes, edges, instances

    def calc_distance (self, es1):
        n0 = set([ n.uri for n in self.nodes ])
        n1 = set([ n.uri for n in es1.nodes ])
        distance = len(n0.intersection(n1)) / float(max(len(n0), len(n1)))
        return distance


class ShapeFactory (object):
    def __init__ (self, kg, measure):
        self.kg = kg
        self.measure = measure

        # enum action space of types
        type_sparql = "SELECT DISTINCT ?n WHERE {[] rdf:type ?n}"
        self.type_list = [ r.n for r in kg.query(type_sparql) ]

    def new_shape (self):
        es = EvoShape(self.kg, self.measure)
        ## RANDOM CHOICE => OBS
        ## TODO: generate from gamma dist
        type_uri = random.choice(self.type_list)
        type_node = EvoShapeNode(type_uri, terminal=True)
        es.add_link(es.root, rdflib.RDF.type, type_node)
        return es


######################################################################
## measure graph topology

class Simplex0 (object):
    def __init__ (self, name="generic"):
        self.name = name
        self.count = defaultdict(int)
        self.df = None

    def increment (self, item):
        self.count[item] += 1

    def get_tally (self):
        self.df = pd.DataFrame.from_dict(self.count, orient="index", columns=["count"]).sort_values("count", ascending=False)
        return self.df


class Simplex1 (Simplex0):
    def __init__ (self, name="generic"):
        super().__init__(name=name)
        self.link_map = None

    def increment (self, item0, item1):
        link = (item0, item1,)
        self.count[link] += 1

    def get_tally_map (self):
        super().get_tally()
        self.link_map = defaultdict(set)

        for index, row in self.df.iterrows():
            item0, item1 = index
            self.link_map[item0].add(item1)

        return self.df, self.link_map


class Measure (object):
    def __init__ (self, name="generic"):
        self.reset()

    def reset (self):
        self.edge_count = 0
        self.node_count = 0
        self.s_gen = Simplex0("subject")
        self.p_gen = Simplex0("predicate")
        self.o_gen = Simplex0("object")
        self.l_gen = Simplex0("literal")
        self.n_gen = Simplex1("node")
        self.e_gen = Simplex1("edge")

    def measure_graph (self, kg):
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


######################################################################
## KG class definition

class KnowledgeGraph (object):
    DEFAULT_NAMESPACES = {
        "dc":	"https://purl.org/dc/terms/",
        "dct":	"https://purl.org/dc/dcmitype/",
        "owl":	"https://www.w3.org/2002/07/owl#",
        "rdf":	"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs":	"http://www.w3.org/2000/01/rdf-schema#",
        "skos":	"https://www.w3.org/2004/02/skos/core#",
        "xsd":	"http://www.w3.org/2001/XMLSchema#",
        }


    def __init__ (self, name="KGlab", base_uri=None, language="en", namespaces={}):
        self._g = rdflib.Graph()
        self.id_list = []

        self.name = name
        self.base_uri = base_uri
        self.language = language

        self._ns = {}
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

    def merge_ns (self, ns_set):
        for prefix, uri in ns_set.items():
            self.add_ns(prefix, uri)


    def add_ns (self, prefix, uri):
        self._ns[prefix] = rdflib.Namespace(uri)
        self._g.namespace_manager.bind(prefix, self._ns[prefix])


    def get_ns (self, prefix):
        return self._ns[prefix]


    def get_context (self):
        """return a context needed for JSON-LD serialization"""
        context = {
            "@language": self.language,
            }

        if self.base_uri:
            context["@vocab"] = self.base_uri

        for prefix, uri in self._ns.items():
            if uri != self.base_uri:
                context[prefix] = uri

        return context


    def add (self, s, p, o):
        self._g.add((s, p, o,))


    @classmethod
    def type_date (cls, date, tz):
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

    def load_ttl (self, path, encoding="utf-8", format="n3"):
        if isinstance(path, pathlib.Path):
            filename = path.as_posix()
        else:
            filename = path

        self._g.parse(filename, format=format, encoding=encoding)


    def save_ttl (self, path, encoding="utf-8", format="n3"):
        if isinstance(path, pathlib.Path):
            filename = path.as_posix()
        else:
            filename = path

        self._g.serialize(destination=filename, format=format, encoding=encoding)


    def load_jsonld (self, path, encoding="utf-8"):
        with open(path, "r", encoding=encoding) as f:
            data = json.load(f)
            self._g.parse(data=json.dumps(data), format="json-ld", encoding=encoding)


    def save_jsonld (self, path, encoding="utf-8"):
        data = self._g.serialize(
            format = "json-ld",
            context = self.get_context(),
            indent = 2,
            encoding = encoding
            )

        with open(path, "wb") as f:
            f.write(data)


    def load_parquet (self, path):
        df = pq.read_pandas(path).to_pandas()

        for index, row in df.iterrows():
            triple = "{} {} {} .".format(row[0], row[1], row[2])
            self._g.parse(data=triple, format="n3")


    def save_parquet (self, path):
        rows_list = [ {"s": s.n3(), "p": p.n3(), "o": o.n3()} for s, p, o in self._g ]
        df = pd.DataFrame(rows_list, columns=("s", "p", "o"))
        table = pa.Table.from_pandas(df)
        pq.write_table(table, path, use_dictionary=True, compression="gzip")


    ######################################################################
    ## node labels

    def get_node_id (self, node):
        """return a unique integer ID for the given RDF node"""
        if not node in self.id_list:
            self.id_list.append(node)

        return self.id_list.index(node)


    def get_node (self, id):
        """return the RDF node corresponding to a unique integer ID"""
        return self.id_list[id]


    def get_node_label (self, node):
        """return the label for the given RDF node"""
        return node.n3(self._g.namespace_manager)


    ######################################################################
    ## visualization
    ##
    ## Automated Network Graph: The triples describing relationships
    ## between entities can be ingested into graph visualization tools
    ## to extend or create an analyst's account-specific network
    ## model.

    def pyvis_style_node (self, g, node_id, label, style={}):
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


    def vis_pyvis (self, notebook=False, style={}):
        """
        https://pyvis.readthedocs.io/
        """
        g = pyvis.network.Network(notebook=notebook)
        g.force_atlas_2based()

        for s, p, o in self._g:
            s_label = s.n3(self._g.namespace_manager)
            s_id = self.get_node_id(s)

            p_label = p.n3(self._g.namespace_manager)

            if isinstance(o, rdflib.term.Literal):
                o_label = str(o.toPython())
            else:
                o_label = o.n3(self._g.namespace_manager)

            o_id = self.get_node_id(o)
    
            self.pyvis_style_node(g, s_id, s_label, style=style)
            self.pyvis_style_node(g, o_id, o_label, style=style)

            g.add_edge(s_id, o_id, label=p_label)

        return g


    ######################################################################
    ## SPARQL queries

    def query (self, sparql, bindings={}):
        for row in self._g.query(sparql, initBindings=bindings):
            yield row

    def query_as_df (self, sparql, bindings={}):
        return pd.DataFrame([ row.asdict() for row in self._g.query(sparql, initBindings=bindings) ])


    ######################################################################
    ## SHACL validation

    def validate (self, shacl_graph=None, shacl_graph_format="turtle", ont_graph=None, advanced=False, inference="rdfs", debug=False, abort_on_error=None, serialize_report_graph=False, **kwargs):

        conforms, v_graph, v_text = pyshacl.validate(
            self._g,
            shacl_graph=shacl_graph,
            shacl_graph_format=shacl_graph_format,
            ont_graph=ont_graph,
            advanced=advanced,
            inference=inference,
            abort_on_error=abort_on_error,

            debug=debug,
            serialize_report_graph=serialize_report_graph,
            *kwargs,
            )

        return conforms, v_graph, v_text


    ######################################################################
    ## SKOS inference
    ## adapted from `skosify` https://github.com/NatLibFi/Skosify
    ## it wasn't being updated regularly, but may be integrated again

    def infer_skos_related (self):
        """Make sure that skos:related is stated in both directions (S23)."""
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.related):
            self._g.add((o, _skos.related, s))


    def infer_skos_topConcept (self):
        """Infer skos:topConceptOf/skos:hasTopConcept (S8) and skos:inScheme (S7)."""
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.hasTopConcept):
            self._g.add((o, _skos.topConceptOf, s))

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self._g.add((o, _skos.hasTopConcept, s))

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self._g.add((s, _skos.inScheme, o))


    def infer_skos_hierarchical (self, narrower=True):
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


    def infer_skos_transitive (self, narrower=True):
        """Perform transitive closure inference (S22, S24)."""
        _skos = self.get_ns("skos")

        for conc in self._g.subjects(self.get_ns("rdf").type, _skos.Concept):
            for bt in self._g.transitive_objects(conc, _skos.broader):
                if bt == conc:
                    continue

                self._g.add((conc, _skos.broaderTransitive, bt))

                if narrower:
                    self._g.add((bt, _skos.narrowerTransitive, conc))


    def infer_skos_symmetric_mappings (self, related=True):
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


    def infer_skos_hierarchical_mappings (self, narrower=True):
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


    def infer_rdfs_classes (self):
        """Perform RDFS subclass inference.
        Mark all resources with a subclass type with the upper class."""
        _rdfs = self.get_ns("rdfs")

        # find out the subclass mappings
        upperclasses = {}  # key: class val: set([superclass1, superclass2..])

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


    def infer_rdfs_properties (self):
        """Perform RDFS subproperty inference.
        Add superproperties where subproperties have been used."""
        _rdfs = self.get_ns("rdfs")

        # find out the subproperty mappings
        superprops = {}  # key: property val: set([superprop1, superprop2..])

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
