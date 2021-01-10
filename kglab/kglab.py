#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## kglab - core classes

import sys
if sys.version_info < (3, 6, ):
    raise RuntimeError("This version of kglab cannot be used in Python < 3.6")

from rdflib import plugin  # type: ignore
from rdflib.serializer import Serializer  # type: ignore
from rdflib.plugin import register, Parser, Serializer  # type: ignore
import rdflib  # type: ignore
# NB: while `plugin` and `Serializer` aren't used directly, loading
# them explicitly here causes them to become registered in `rdflib`
register("json-ld", Parser, "rdflib_jsonld.parser", "JsonLDParser")
register("json-ld", Serializer, "rdflib_jsonld.serializer", "JsonLDSerializer")

from kglab.pkg_types import PathLike, IOPathLike, GraphLike, RDF_Node

import chocolate  # type: ignore
import codecs
import dateutil.parser as dup
import datetime as dt
import GPUtil  # type: ignore
import io
import json
import owlrl  # type: ignore
import pandas as pd  # type: ignore
import pathlib
import pyshacl  # type: ignore
import typing
import urlpath  # type: ignore
import warnings


class KnowledgeGraph (object):
    _DEFAULT_NAMESPACES: dict = {
        "dct":  "http://purl.org/dc/terms/",
        "owl":  "http://www.w3.org/2002/07/owl#",
        "rdf":  "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "xsd":  "http://www.w3.org/2001/XMLSchema#",
        }


    def __init__ (
        self,
        *,
        name: str = "kg+lab",
        base_uri: str = None,
        language: str = "en",
        namespaces: dict = {},
        graph: typing.Optional[GraphLike] = None
        ) -> None:
        """
        """
        self.name = name
        self.base_uri = base_uri
        self.language = language
        self.gpus = GPUtil.getGPUs()

        if graph:
            self._g = graph
        else:
            self._g = rdflib.Graph()

        self._ns: dict = {}
        self.merge_ns({ **self._DEFAULT_NAMESPACES, **namespaces })


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

    def merge_ns (
        self,
        ns_set: dict
        ) -> None:
        """
        """
        for prefix, uri in ns_set.items():
            self.add_ns(prefix, uri)


    def add_ns (
        self,
        prefix: str,
        uri: str
        ) -> None:
        """
        Since rdflib converts Namespace bindings to URIRef, we'll keep references to them
        """
        self._ns[prefix] = rdflib.Namespace(uri)
        self._g.namespace_manager.bind(prefix, self._ns[prefix])


    def get_ns (
        self,
        prefix: str
        ) -> rdflib.Namespace:
        """
        prefix: the TTL-format prefix used to reference the namespace
        return: rdflib.Namespace
        """
        return self._ns[prefix]


    def get_context (
        self
        ) -> dict:
        """
        Return a context needed for JSON-LD serialization
        """
        context: dict = {
            "@language": self.language,
            }

        if self.base_uri:
            context["@vocab"] = self.base_uri

        for prefix, uri in self._ns.items():
            if uri != self.base_uri:
                context[prefix] = uri

        return context


    def add (
        self,
        s: RDF_Node,
        p: RDF_Node,
        o: RDF_Node
        ) -> None:
        """
        """
        self._g.add((s, p, o,))


    @classmethod
    def type_date (
        cls,
        date: str,
        tz: dict
        ) -> rdflib.Literal:
        """
        input `date` should be interpretable as having a local timezone
        """
        date_tz = dup.parse(date, tzinfos=tz)
        return rdflib.Literal(date_tz, datatype=rdflib.XSD.dateTime)


    ######################################################################
    ## serialization
    ##
    ## Format and software agnostic: We are interested in technology
    ## that will not be a barrier to widespread use. We want to allow
    ## the export of the entity triples in a variety of formats, at
    ## the most basic level as a CSV, so that an analyst can load the
    ## results into their system of choice. By prioritizing
    ## non-proprietary, universal formats the results can be easily
    ## integrated into several of the existing tools for creating 
    ## network graphs.

    _ERROR_PATH: str = "The `path` file object must be a writable, bytes-like object"
    _ERROR_ENCODE: str = "The text `encoding` value does not match anything in the Python codec registry"

    # PEP 586, although not until Py 3.8 
    # RDF_FORMAT = typing.Literal[ "n3", "ttl", "turtle", "nt", "xml", "pretty-xml", "trix", "trig", "nquads" ]

    _RDF_FORMAT: list = [
        "n3", 
        "ttl", 
        "turtle", 
        "nt", 
        "xml", 
        "pretty-xml", 
        "trix", 
        "trig", 
        "nquads"
    ]
    
    
    @classmethod
    def _get_filename (
        cls,
        path: PathLike
        ) -> typing.Optional[str]:
        if not path:
            filename = None
        elif isinstance(path, urlpath.URL):
            filename = str(path)
        elif isinstance(path, pathlib.Path):
            filename = path.as_posix()
        else:
            filename = path

        return filename

    
    def load_rdf (
        self,
        path: IOPathLike,
        *,
        format: str = "n3",
        encoding: str = "utf-8"
        ) -> None:
        """
        """
        if hasattr(path, "read"):
            self._g.parse(path, format=format, encoding=encoding)
        else:
            self._g.parse(self._get_filename(path), format=format, encoding=encoding)


    def load_rdf_text (
        self,
        data: typing.AnyStr,
        *,
        format: str = "n3",
        encoding: str = "utf-8"
        ) -> None:
        """
        """
        self._g.parse(data=data, format=format, encoding=encoding);


    def save_rdf (
        self,
        path: IOPathLike,
        *,
        format: str = "n3",
        base: str = None,
        encoding: str = "utf-8",
        **args: typing.Any
        ) -> None:
        """
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination.
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

    format:
serialization format, defaults to N3 triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking the `format` paramter
        if format == "json-ld":
            raise TypeError("Use the save_jsonld() method instead")
        elif format not in self._RDF_FORMAT:
            try:
                s = rdflib.plugin.get(format, rdflib.serializer.Serializer)
            except Exception as e:
                raise TypeError("unknown format: {}".format(format))

        # error checking for the `encoding` parameter
        try:
            codecs.lookup(encoding)
        except LookupError as e:
            raise LookupError(self._ERROR_ENCODE)

        # substitute the `KnowledgeGraph.base_uri` base set for the graph, if used
        if not base and self.base_uri:
            base = self.base_uri
      
        # error checking for a file-like object `path` paramter
        if hasattr(path, "write"):
            if hasattr(path, "encoding"):
                raise TypeError(self._ERROR_PATH)
            else:
                try:
                    self._g.serialize(
                        destination=path,
                        format=format,
                        base=base,
                        encoding=encoding,
                        **args
                    )
                except io.UnsupportedOperation as e:
                    raise TypeError(self._ERROR_PATH)

        # otherwise write to a local file reference
        else:
            self._g.serialize(
                destination=self._get_filename(path),
                format=format,
                base=base,
                encoding=encoding,
                **args
            )


    def save_rdf_text (
        self,
        *,
        format: str = "n3",
        base: str = None,
        encoding: str = "utf-8",
        **args: typing.Any
        ) -> typing.AnyStr:
        """
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to a string.

    format:
serialization format, defaults to N3 triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

    returns:
A string representing the RDF graph
        """
        # error checking the `format` paramter
        if format not in self._RDF_FORMAT:
            try:
                s = rdflib.plugin.get(format, rdflib.serializer.Serializer)
            except Exception as e:
                raise TypeError("unknown format: {}".format(format))

        # error checking for the `encoding` parameter
        try:
            codecs.lookup(encoding)
        except LookupError as e:
            raise LookupError(self._ERROR_ENCODE)

        # substitute the `KnowledgeGraph.base_uri` base set for the graph, if used
        if not base and self.base_uri:
            base = self.base_uri

        return self._g.serialize(
            destination=None,
            format=format,
            base=base,
            encoding=encoding,
            **args
        ).decode(encoding) 


    def load_jsonld (
        self,
        path: PathLike,
        *,
        encoding: str = "utf-8"
        ) -> None:
        """
        """
        with open(path, "r", encoding=encoding) as f:
            data = json.load(f)
            self._g.parse(
                data=json.dumps(data),
                format="json-ld",
                encoding=encoding
            )


    def save_jsonld (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        **args: typing.Any
        ) -> None:
        """
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination as [JSON-LD](https://json-ld.org/).

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

    encoding:
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking for a file-like object `path` paramter
        if hasattr(path, "write"):
            if hasattr(path, "encoding"):
                raise TypeError(self._ERROR_PATH)
            else:
                f = path
        else:
            f = open(self._get_filename(path), "wb") # type: ignore

        # error checking for the `encoding` parameter
        try:
            codecs.lookup(encoding)
        except LookupError as e:
            raise LookupError(self._ERROR_ENCODE)

        f.write( # type: ignore
            self._g.serialize(
                format="json-ld",
                context=self.get_context(),
                indent=2,
                encoding=encoding,
                **args
            )
        )


    def load_parquet (
        self,
        path: IOPathLike,
        **kwargs: typing.Any
        ) -> None:
        """
        """
        df = pd.read_parquet(
            path,
            **chocolate.filter_args(kwargs, pd.read_parquet)
        )

        for index, row in df.iterrows():
            triple = "{} {} {} .".format(row[0], row[1], row[2])
            self._g.parse(data=triple, format="n3")


    def save_parquet (
        self,
        path: IOPathLike,
        *,
        compression: str = "snappy",
        **kwargs: typing.Any
        ) -> None:
        """
        """
        rows_list = [ {"s": s.n3(), "p": p.n3(), "o": o.n3()} for s, p, o in self._g ]
        df = pd.DataFrame(rows_list, columns=("s", "p", "o"))
        
        df.to_parquet(
            path,
            compression=compression,
            **chocolate.filter_args(kwargs, df.to_parquet)
        )


    ######################################################################
    ## SPARQL queries

    def query (
        self,
        sparql: str,
        *,
        bindings: dict = {}
        ) -> typing.Iterable:
        """
        """
        for row in self._g.query(sparql, initBindings=bindings):
            yield row


    @classmethod
    def n3fy (
        cls,
        d: dict,
        nm: rdflib.namespace.NamespaceManager,
        *,
        pythonify: bool = True
        ) -> dict:
        """
        """
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


    def query_as_df (
        self,
        sparql: str,
        *,
        bindings: dict = {},
        simplify: bool = True,
        pythonify: bool = True
        ) -> pd.DataFrame:
        """
        """
        iter = self._g.query(sparql, initBindings=bindings)

        if simplify:
            nm = self._g.namespace_manager
            df = pd.DataFrame([ self.n3fy(row.asdict(), nm, pythonify=pythonify) for row in iter ])
        else:
            df = df = pd.DataFrame([ row.asdict() for row in iter ])
        
        return df


    ######################################################################
    ## SHACL validation

    def validate (
        self,
        *,
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
        ) -> typing.Tuple[bool, "KnowledgeGraph", str]:
        """
        """
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
            **chocolate.filter_args(kwargs, pyshacl.validate),
            )
       
        namespaces = {
            "sh":     "http://www.w3.org/ns/shacl#",
            "schema": "http://schema.org/",
        }

        g = rdflib.Graph()
        g.parse(data=report_graph_data, format="n3", encoding="utf-8")
        report_graph = KnowledgeGraph(graph=g, 
                                      name="report graph", 
                                      namespaces=namespaces
                                     )

        return conforms, report_graph, report_text


    ######################################################################
    ## SKOS inference
    ## adapted from `skosify` https://github.com/NatLibFi/Skosify
    ## it wasn't being updated regularly, but may be integrated again

    def infer_skos_related (
        self
        ) -> None:
        """
        Make sure that skos:related is stated in both directions (S23).
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.related):
            self._g.add((o, _skos.related, s))


    def infer_skos_topConcept (
        self
        ) -> None:
        """
        Infer skos:topConceptOf/skos:hasTopConcept (S8) and skos:inScheme (S7).
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.hasTopConcept):
            self._g.add((o, _skos.topConceptOf, s))

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self._g.add((o, _skos.hasTopConcept, s))

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self._g.add((s, _skos.inScheme, o))


    def infer_skos_hierarchical (
        self,
        *,
        narrower: bool = True
        ) -> None:
        """
        Infer skos:broader/skos:narrower (S25) but only keep skos:narrower on request.
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


    def infer_skos_transitive (
        self,
        *,
        narrower: bool = True
        ) -> None:
        """
        Perform transitive closure inference (S22, S24).
        """
        _skos = self.get_ns("skos")

        for conc in self._g.subjects(self.get_ns("rdf").type, _skos.Concept):
            for bt in self._g.transitive_objects(conc, _skos.broader):
                if bt == conc:
                    continue

                self._g.add((conc, _skos.broaderTransitive, bt))

                if narrower:
                    self._g.add((bt, _skos.narrowerTransitive, conc))


    def infer_skos_symmetric_mappings (
        self,
        *,
        related: bool = True
        ) -> None:
        """
        Ensure that the symmetric mapping properties (skos:relatedMatch,
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


    def infer_skos_hierarchical_mappings (
        self,
        *,
        narrower: bool = True
        ) -> None:
        """
        Infer skos:broadMatch/skos:narrowMatch (S43) and add the super-properties
        skos:broader/skos:narrower (S41).
        :param bool narrower: If set to False, skos:narrowMatch will be removed not added.
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


    def infer_rdfs_classes (
        self
        ) -> None:
        """
        Perform RDFS subclass inference.
        Mark all resources with a subclass type with the upper class.
        """
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


    def infer_rdfs_properties (
        self
        ) -> None:
        """
        Perform RDFS subproperty inference.
        Add superproperties where subproperties have been used.
        """
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

                    
    def infer_rdfs_closure (
        self
        ) -> None:
        """
        Add inferred triples from RDFS based on OWL-RL,
        see <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>
        """
        rdfs = owlrl.RDFSClosure.RDFS_Semantics(self._g, False, False, False)
        rdfs.closure()
        rdfs.flush_stored_triples()


    def infer_owlrl_closure (
        self
        ) -> None:
        """
        Add inferred triples from OWL based on OWL-RL,
        see <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>
        """
        owl = owlrl.OWLRL_Semantics(self._g, False, False, False)
        owl.closure()
        owl.flush_stored_triples()
