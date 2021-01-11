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
import copy
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


class KnowledgeGraph (object):
    _DEFAULT_NAMESPACES: dict = {
        "dct":    "http://purl.org/dc/terms/",
        "owl":    "http://www.w3.org/2002/07/owl#",
        "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
        "schema": "http://schema.org/",
        "sh":     "http://www.w3.org/ns/shacl#",
        "skos":   "http://www.w3.org/2004/02/skos/core#",
        "xsd":    "http://www.w3.org/2001/XMLSchema#",
        }


    def __init__ (
        self,
        *,
        name: str = "generic",
        base_uri: str = None,
        language: str = "en",
        namespaces: dict = {},
        graph: typing.Optional[GraphLike] = None,
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
            
        for prefix, uri in self._DEFAULT_NAMESPACES.items():
            self.add_ns(prefix, uri)

        for prefix, uri in namespaces.items():
            self.add_ns(prefix, uri)


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

    def add_ns (
        self,
        prefix: str,
        uri: str,
        ) -> None:
        """
Since rdflib converts Namespace bindings to URIRef, we'll keep references to them
        """
        self._ns[prefix] = rdflib.Namespace(uri)
        self._g.namespace_manager.bind(prefix, self._ns[prefix])


    def get_ns (
        self,
        prefix: str,
        ) -> rdflib.Namespace:
        """
    prefix:
N3-format prefix used to reference a namespace

    returns:
rdflib.Namespace
        """
        return self._ns[prefix]


    def get_context (
        self
        ) -> dict:
        """
    returns:
context needed for JSON-LD serialization
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


    @classmethod
    def encode_date (
        cls,
        datetime: str,
        tzinfos: dict,
        ) -> rdflib.Literal:
        """
Helper method to ensure that an input `datetime` value has a timezone that can be interpreted by [`rdflib.XSD.dateTime`](https://www.w3.org/TR/xmlschema-2/#dateTime).

    datetime:
input datetime as a string

    tzinfos:
timezones as a dict, used by
[`dateutil.parser.parse()`](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse) as additional time zone names or aliases which may be present in the input `datetime` string

    returns:
[`rdflib.Literal`](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#literals) formatted as an XML Schema 2 `dateTime` value.
        """
        date_tz = dup.parse(datetime, tzinfos=tzinfos)
        return rdflib.Literal(date_tz, datatype=rdflib.XSD.dateTime)


    def add (
        self,
        s: RDF_Node,
        p: RDF_Node,
        o: RDF_Node,
        ) -> None:
        """
        """
        self._g.add((s, p, o,))


    def remove (
        self,
        s: RDF_Node,
        p: RDF_Node,
        o: RDF_Node,
        ) -> None:
        """
        """
        self._g.remove((s, p, o,))


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

    _RDF_FORMAT: list = [
        # RDFXMLParser
        "application/rdf+xml", 
        "xml",
        # N3Parser
        "text/n3",
        "n3",
        # TurtleParser
        "text/turtle",
        "turtle",
        "ttl",
        # NTParser
        "application/n-triples",
        "ntriples",
        "nt",
        "nt11",
        # NQuadsParser
        "application/n-quads",
        "nquads",
        # TriXParser
        "application/trix",
        "trix",
        # TrigParser
        "trig",
        # JsonLDParser
        "json-ld",
    ]

    _ERROR_ENCODE: str = "The text `encoding` value does not match anything in the Python codec registry"
    _ERROR_PATH: str = "The `path` file object must be a writable, bytes-like object"


    @classmethod
    def _check_format (
        cls,
        format: str,
        ) -> None:
        """
Semiprivate method to error-check that a `format` parameter corresponds to a known RDFlib serialization plugin; otherwise this throws a `TypeError` exception
        """
        if format not in cls._RDF_FORMAT:
            try:
                s = rdflib.plugin.get(format, rdflib.serializer.Serializer)
            except Exception as e:
                raise TypeError("unknown format: {}".format(format))


    @classmethod
    def _check_encoding (
        cls,
        encoding: str,
        ) -> None:
        """
Semiprivate method to error-check that an `encoding` parameter is within the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        try:
            codecs.lookup(encoding)
        except LookupError as e:
            raise LookupError(cls._ERROR_ENCODE)


    @classmethod
    def _get_filename (
        cls,
        path: PathLike,
        ) -> typing.Optional[str]:
        """
Semiprivate method to extract a file name (str) for a file reference from a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) or its subclasses

    returns:
a string as a file name or URL to a file reference
        """
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
        format: str = "ttl",
        base: str = None,
        **args: typing.Any,
        ) -> None:
        """
A wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from the `path` source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds triples/quads to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
logical URI to use as the document base; if not specified the document location is used
        """
        # error checking for the `format` parameter
        if format == "json-ld":
            raise TypeError("Use the load_jsonld() method instead")
        else:
            self._check_format(format)

        # substitute the `KnowledgeGraph.base_uri` as the document base, if used
        if not base and self.base_uri:
            base = self.base_uri

        if hasattr(path, "read"):
            self._g.parse(
                path,
                format=format,
                publicID=base,
                **args,
            )
        else:
            self._g.parse(
                self._get_filename(path),
                format=format,
                publicID=base,
                **args,
            )


    def load_rdf_text (
        self,
        data: typing.AnyStr,
        *,
        format: str = "ttl",
        base: str = None,
        **args: typing.Any,
        ) -> None:
        """
A wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from a text.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds triples/quads to an RDF graph, it does not overwrite the existing RDF graph.

    data:
text representation of RDF graph data

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
logical URI to use as the document base; if not specified the document location is used
        """
        # error checking for the `format` parameter
        self._check_format(format)

        # substitute the `KnowledgeGraph.base_uri` as the document base, if used
        if not base and self.base_uri:
            base = self.base_uri

        self._g.parse(
            data=data,
            format=format,
            publicID=base,
            **args,
        )


    def save_rdf (
        self,
        path: IOPathLike,
        *,
        format: str = "ttl",
        base: str = None,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> None:
        """
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination.
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking for the `format` paramter
        if format == "json-ld":
            raise TypeError("Use the save_jsonld() method instead")
        else:
            self._check_format(format)

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

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
                        **args,
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
                **args,
            )


    def save_rdf_text (
        self,
        *,
        format: str = "ttl",
        base: str = None,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> typing.AnyStr:
        """
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to a string.

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

    returns:
text representing the RDF graph
        """
        # error checking for the `format` parameter
        self._check_format(format)

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # substitute the `KnowledgeGraph.base_uri` base set for the graph, if used
        if not base and self.base_uri:
            base = self.base_uri

        return self._g.serialize(
            destination=None,
            format=format,
            base=base,
            encoding=encoding,
            **args,
        ).decode(encoding) 


    def load_jsonld (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> None:
        """
A wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from a [JSON-LD](https://json-ld.org/) source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds triples/quads to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); otherwise this throws a `TypeError` exception

    encoding:
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking for a file-like object `path` paramter
        if hasattr(path, "read"):
            f = path
        else:
            f = open(path, "r", encoding=encoding) # type: ignore

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        self._g.parse(
            # TODO
            data=json.dumps(json.load(f)),  # type: ignore
            format="json-ld",
            encoding=encoding,
            **args,
        )


    def save_jsonld (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> None:
        """
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination as [JSON-LD](https://json-ld.org/).
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

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
        self._check_encoding(encoding)

        # TODO
        f.write( # type: ignore
            self._g.serialize(
                format="json-ld",
                context=self.get_context(),
                indent=2,
                encoding=encoding,
                **args,
            )
        )


    def load_parquet (
        self,
        path: IOPathLike,
        **kwargs: typing.Any,
        ) -> None:
        """
        """
        df = pd.read_parquet(
            path,
            **chocolate.filter_args(kwargs, pd.read_parquet)
        )

        for _, row in df.iterrows():
            triple = "{} {} {} .".format(row[0], row[1], row[2])
            self._g.parse(data=triple, format="ttl")


    def save_parquet (
        self,
        path: IOPathLike,
        *,
        compression: str = "snappy",
        **kwargs: typing.Any,
        ) -> None:
        """
        """
        rows_list = [ {"s": s.n3(), "p": p.n3(), "o": o.n3()} for s, p, o in self._g ]
        df = pd.DataFrame(rows_list, columns=("s", "p", "o"))
        
        df.to_parquet(
            path,
            compression=compression,
            **chocolate.filter_args(kwargs, df.to_parquet),
        )


    ######################################################################
    ## SPARQL queries

    @classmethod
    def n3fy (
        cls,
        d: dict,
        nm: rdflib.namespace.NamespaceManager,
        *,
        pythonify: bool = True,
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


    def query (
        self,
        sparql: str,
        *,
        bindings: dict = {},
        ) -> typing.Iterable:
        """
        """
        for row in self._g.query(sparql, initBindings=bindings):
            yield row


    def query_as_df (
        self,
        sparql: str,
        *,
        bindings: dict = {},
        simplify: bool = True,
        pythonify: bool = True,
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
        serialize_report_graph: typing.Optional[str] = "ttl",
        debug: bool = False,
        **kwargs: typing.Any,
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

        g = rdflib.Graph()
        
        g.parse(
            data=report_graph_data,
            format="ttl",
            encoding="utf-8"
        )
        
        report_graph = KnowledgeGraph(
            graph=g,
            name="report graph",
        )

        return conforms, report_graph, report_text


    ######################################################################
    ## OWL RL inference
    ## adapted from <https://wiki.uib.no/info216/index.php/Python_Examples>

    def infer_owlrl_closure (
        self
        ) -> None:
        """
Infer deductive closure for [OWL 2 RL semantics](https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules) based on [OWL-RL](https://owl-rl.readthedocs.io/en/latest/stubs/owlrl.html#module-owlrl)

See <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>
        """
        owl = owlrl.OWLRL_Semantics(self._g, False, False, False)
        owl.closure()
        owl.flush_stored_triples()


    def infer_rdfs_closure (
        self
        ) -> None:
        """
Infer deductive closure for [RDFS semantics](https://www.w3.org/TR/rdf-mt/) based on [OWL-RL](https://owl-rl.readthedocs.io/en/latest/stubs/owlrl.html#module-owlrl)

See <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>
        """
        rdfs = owlrl.RDFSClosure.RDFS_Semantics(self._g, False, False, False)
        rdfs.closure()
        rdfs.flush_stored_triples()


    def infer_rdfs_properties (
        self
        ) -> None:
        """
Perform RDFS sub-property inference, adding super-properties where sub-properties have been used.

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.
        """
        _rdfs = self.get_ns("rdfs")

        # determine sub-property mappings
        # key: property val: set([superprop1, superprop2..])
        super_props: typing.Dict[typing.Any, typing.Any] = {}

        for s, o in self._g.subject_objects(_rdfs.subPropertyOf):
            super_props.setdefault(s, set())

            for sub_prop in self._g.transitive_objects(s, _rdfs.subPropertyOf):
                if sub_prop != s:
                    super_props[s].add(sub_prop)

        # add super-property relationships
        for p, sup_prop_list in super_props.items():
            for s, o in self._g.subject_objects(p):
                for sup_prop in sup_prop_list:
                    self.add(s, sup_prop, o)

    
    def infer_rdfs_classes (
        self
        ) -> None:
        """
Perform RDFS subclass inference, marking all resources having a subclass type with their superclass.
        
Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.
        """
        _rdfs = self.get_ns("rdfs")

        # determine subclass mappings
        # key: class val: set([superclass1, superclass2..])
        super_classes: typing.Dict[typing.Any, typing.Any] = {}

        for s, o in self._g.subject_objects(_rdfs.subClassOf):
            super_classes.setdefault(s, set())

            for sup_class in self._g.transitive_objects(s, _rdfs.subClassOf):
                if sup_class != s:
                    super_classes[s].add(sup_class)

        # set the superclass type information for subclass instances
        for s, sup_class_list in super_classes.items():
            for sub_inst in self._g.subjects(self.get_ns("rdf").type, s):
                for sup_class in sup_class_list:
                    self.add(sub_inst, self.get_ns("rdf").type, sup_class)


    ######################################################################
    ## SKOS inference
    ## adapted from `skosify` https://github.com/NatLibFi/Skosify
    ## it wasn't being updated regularly, but may be integrated again

    def infer_skos_related (
        self
        ) -> None:
        """
Infer OWL symmetry (both directions) for `skos:related`
[(*S23*)](https://www.w3.org/TR/skos-reference/#S23)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.related):
            self.add(o, _skos.related, s)


    def infer_skos_concept (
        self
        ) -> None:
        """
Infer `skos:topConceptOf` as a sub-property of `skos:inScheme`
[(*S7*)](https://www.w3.org/TR/skos-reference/#S7)

Infer `skos:topConceptOf` as `owl:inverseOf` the property `skos:hasTopConcept`
[(*S8*)](https://www.w3.org/TR/skos-reference/#S8)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.hasTopConcept):
            self.add(o, _skos.topConceptOf, s)

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self.add(o, _skos.hasTopConcept, s)

        for s, o in self._g.subject_objects(_skos.topConceptOf):
            self.add(s, _skos.inScheme, o)


    def infer_skos_hierarchical (
        self,
        *,
        narrower: bool = True,
        ) -> None:
        """
Infer `skos:narrower` as `owl:inverseOf` the property `skos:broader`; although only keep `skos:narrower` on request
[(*S25*)](https://www.w3.org/TR/skos-reference/#S25)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

    narrower:
if false, `skos:narrower` will be removed instead of added
        """
        _skos = self.get_ns("skos")

        if narrower:
            for s, o in self._g.subject_objects(_skos.broader):
                self.add(o, _skos.narrower, s)

        for s, o in self._g.subject_objects(_skos.narrower):
            self.add(o, _skos.broader, s)

            if not narrower:
                self.remove(s, _skos.narrower, o)


    def infer_skos_transitive (
        self,
        *,
        narrower: bool = True,
        ) -> None:
        """
Infer transitive closure,
`skos:broader` as a sub-property of `skos:broaderTransitive`, and `skos:narrower` as a sub-property of `skos:narrowerTransitive`
[(*S22*)](https://www.w3.org/TR/skos-reference/#S22)

Infer `skos:broaderTransitive` and `skos:narrowerTransitive` (on request only) as instances of `owl:TransitiveProperty`
[(*S24*)](https://www.w3.org/TR/skos-reference/#S24)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

    narrower:
also infer transitive closure for `skos:narrowerTransitive`
        """
        _skos = self.get_ns("skos")

        for concept in self._g.subjects(self.get_ns("rdf").type, _skos.Concept):
            for broader_concept in self._g.transitive_objects(concept, _skos.broader):
                if broader_concept != concept:
                    self.add(concept, _skos.broaderTransitive, broader_concept)

                    if narrower:
                        self.add(broader_concept, _skos.narrowerTransitive, concept)


    def infer_skos_symmetric_mappings (
        self,
        *,
        related: bool = True,
        ) -> None:
        """
Infer symmetric mapping properties (`skos:relatedMatch`, `skos:closeMatch`, `skos:exactMatch`) as instances of `owl:SymmetricProperty`
[(*S44*)](https://www.w3.org/TR/skos-reference/#S44)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

    related:
infer the `skos:related` super-property for all `skos:relatedMatch` relations
[(*S41*)](https://www.w3.org/TR/skos-reference/#S41)
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.relatedMatch):
            self.add(o, _skos.relatedMatch, s)

            if related:
                self.add(s, _skos.related, o)
                self.add(o, _skos.related, s)

        for s, o in self._g.subject_objects(_skos.closeMatch):
            self.add(o, _skos.closeMatch, s)

        for s, o in self._g.subject_objects(_skos.exactMatch):
            self.add(o, _skos.exactMatch, s)


    def infer_skos_hierarchical_mappings (
        self,
        *,
        narrower: bool = True,
        ) -> None:
        """
Infer `skos:narrowMatch` as `owl:inverseOf` the property `skos:broadMatch`
[(*S43*)](https://www.w3.org/TR/skos-reference/#S43)

Infer the `skos:related` super-property for all `skos:relatedMatch` relations
[(*S41*)](https://www.w3.org/TR/skos-reference/#S41)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

        narrower:
if false, `skos:narrowMatch` will be removed instead of added
        """
        _skos = self.get_ns("skos")

        for s, o in self._g.subject_objects(_skos.broadMatch):
            self.add(s, _skos.broader, o)

            if narrower:
                self.add(o, _skos.narrowMatch, s)
                self.add(o, _skos.narrower, s)

        for s, o in self._g.subject_objects(_skos.narrowMatch):
            self.add(o, _skos.broadMatch, s)
            self.add(o, _skos.broader, s)

            if narrower:
                self.add(s, _skos.narrower, o)
            else:
                self.remove(s, _skos.narrowMatch, o)
