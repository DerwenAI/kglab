#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

######################################################################
## kglab - core classes

from kglab.decorators import multifile
from kglab.pkg_types import PathLike, IOPathLike, GraphLike, RDF_Node
from kglab.gpviz import GPViz
from kglab.util import get_gpu_count
from kglab.version import _check_version
_check_version()

import rdflib  # type: ignore  # pylint: disable=E0401
import rdflib.plugin  # type: ignore  # pylint: disable=E0401
import rdflib.plugins.parsers.notation3 as rdf_n3  # type: ignore  # pylint: disable=E0401
#rdflib.plugin.register("json-ld", rdflib.plugin.Parser, "rdflib_jsonld.parser", "JsonLDParser")
#rdflib.plugin.register("json-ld", rdflib.plugin.Serializer, "rdflib_jsonld.serializer", "JsonLDSerializer")

from icecream import ic  # type: ignore  # pylint: disable=E0401
import chocolate  # type: ignore  # pylint: disable=E0401
import codecs
import csvwlib  # type: ignore  # pylint: disable=E0401
import datetime
import dateutil.parser as dup  # pylint: disable=E0401
import io
import json
import owlrl  # type: ignore  # pylint: disable=E0401
import pandas as pd  # type: ignore  # pylint: disable=E0401
import pathlib
import pyshacl  # type: ignore  # pylint: disable=E0401
import pyvis  # type: ignore  # pylint: disable=E0401
import traceback
import typing
import urlpath  # type: ignore  # pylint: disable=E0401

if get_gpu_count() > 0:
    import cudf  # type: ignore  # pylint: disable=E0401


class KnowledgeGraph:
    """
This is the primary class used to represent RDF graphs, on which the other classes are dependent.
See <https://derwen.ai/docs/kgl/concepts/#knowledge-graph>

Core feature areas include:

  * namespace management (ontology, controlled vocabularies)
  * graph construction
  * serialization
  * SPARQL querying
  * SHACL validation
  * inference based on OWL-RL, RDFS, SKOS
    """

    _DEFAULT_NAMESPACES: dict = {
        "dct":    "http://purl.org/dc/terms/",
        "owl":    "http://www.w3.org/2002/07/owl#",
        "prov":   "http://www.w3.org/ns/prov#",
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
        use_gpus: bool = True,
        import_graph: typing.Optional[GraphLike] = None,
        namespaces: dict = None,
        ) -> None:
        """
Constructor for a `KnowledgeGraph` object.

    name:
optional, internal name for this graph

    base_uri:
the default [*base URI*](https://tools.ietf.org/html/rfc3986#section-5.1) for this RDF graph

    language:
the default [*language tag*](https://www.w3.org/TR/rdf11-concepts/#dfn-language-tag), e.g., used for [*language indexing*](https://www.w3.org/TR/json-ld11/#language-indexing)

    use_gpus:
optionally, use the NVidia GPU devices with [RAPIDS](https://rapids.ai/) if these libraries have been installed and the devices are available; defaults to `True`

    import_graph:
optionally, another existing RDF graph to be used as a starting point

    namespaces:
a dictionary of [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) (dict values) and their corresponding *prefix* strings (dict keys) to add as *controlled vocabularies* which are available for use in the RDF graph, binding each prefix to the given namespace
        """
        self.name = name
        self.base_uri = base_uri
        self.language = language

        # use NVidia GPU devices if available and the libraries
        # have been installed and the flag is not disabled
        if use_gpus and get_gpu_count() > 0:
            self.use_gpus = True
        else:
            self.use_gpus = False

        # import relations from another RDF graph, or start from blank
        if import_graph:
            self._g = import_graph
        else:
            self._g = rdflib.Graph()

        # initialize the namespaces
        self._ns: dict = {}

        for prefix, iri in self._DEFAULT_NAMESPACES.items():
            self.add_ns(prefix, iri)

        if namespaces:
            for prefix, iri in namespaces.items():
                self.add_ns(prefix, iri)


    def rdf_graph (
        self
        ) -> rdflib.Graph:
        """
Accessor for the RDF graph.

    returns:
the [`rdflib.Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=graph#graph) object
        """
        return self._g


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
        iri: str,
        override: bool = True,
        replace: bool = False,
        ) -> None:
        """
Adds another [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) among the *controlled vocabularies* available to use in the RDF graph, binding the `prefix` to the given namespace.

Since the RDFlib [`NamespaceManager`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.namespace.NamespaceManager) automagically converts all input bindings into [`URIRef`](https://www.w3.org/TR/rdf-concepts/#section-Graph-URIref) instead, we'll keep references to the namespaces – for later use.

    prefix:
a [namespace prefix](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-prefix); it's recommended to confirm prefix usage (based on convention) by searching on <http://prefix.cc/>

    iri:
URL to use for constructing the [namespace IRI](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-iri)

    override:
rebind, even if the given namespace is already bound with another prefix

    replace:
replace any existing prefix with the new namespace
        """
        if override and iri in self._ns.values():
            rev_ns = {
                str(v): k
                for k, v in self._ns.items()
            }

            bogus_prefix = rev_ns[iri]
            del self._ns[bogus_prefix]

        if replace or prefix not in self._ns:
            self._ns[prefix] = rdflib.Namespace(iri)

        self._g.namespace_manager.bind(
            prefix,
            self._ns[prefix],
            override=override,
            replace=replace,
        )


    def get_ns (
        self,
        prefix: str,
        ) -> rdflib.Namespace:
        """
Lookup a [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) among the *controlled vocabularies* available to use in the RDF graph.

    prefix:
a [namespace prefix](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-prefix)

    returns:
the RDFlib [`Namespace`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) for the *controlled vocabulary* referenced by `prefix`
        """
        return self._ns[prefix]


    def get_ns_dict (
        self
        ) -> dict:
        """
Generate a dictionary of the *namespaces* used in this RDF graph.

    returns:
a `dict` describing the namespaces in this RDF graph
        """
        ns_dict = {
            prefix: str(ns)
            for prefix, ns in self._ns.items()
        }

        nm = self._g.namespace_manager

        for prefix, uri in nm.namespaces():
            ns_dict[prefix] = str(uri)

        return ns_dict


    def describe_ns (
        self
        ) -> pd.DataFrame:
        """
Describe the *namespaces* used in this RDF graph.

    returns:
a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) describing the namespaces in this RDF graph; uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled
        """
        col_names: typing.List[str] = [ "prefix", "namespace" ]

        rows_list: typing.List[dict] = [
            {
                col_names[0]: prefix,
                col_names[1]: str(ns),
            }
            for prefix, ns in self.get_ns_dict().items()
        ]

        if self.use_gpus:
            df = cudf.DataFrame(rows_list, columns=col_names)
        else:
            df = pd.DataFrame(rows_list, columns=col_names)

        return df


    def get_context (
        self
        ) -> dict:
        """
Generates a [*JSON-LD context*](https://www.w3.org/TR/json-ld11/#the-context) used for
serializing the RDF graph as [JSON-LD](https://json-ld.org/).

    returns:
context needed for JSON-LD serialization
        """
        context: dict = self.get_ns_dict()
        context["@language"] = self.language

        if self.base_uri:
            context["@vocab"] = self.base_uri

        return context


    def encode_date (
        self,
        dt: str,
        tzinfos: dict,
        ) -> rdflib.Literal:
        """
Helper method to ensure that an input `datetime` value has a timezone that can be interpreted by [`rdflib.XSD.dateTime`](https://www.w3.org/TR/xmlschema-2/#dateTime).

    dt:
input datetime as a string

    tzinfos:
timezones as a dict, used by
[`dateutil.parser.parse()`](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse) as additional time zone names or aliases which may be present in the input `datetime` string

    returns:
[`rdflib.Literal`](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#literals) formatted as an XML Schema 2 `dateTime` value
        """
        date_tz = dup.parse(dt, tzinfos=tzinfos)
        return rdflib.Literal(date_tz, datatype=self.get_ns("xsd").dateTime)


    def add (
        self,
        s: RDF_Node,
        p: RDF_Node,
        o: RDF_Node,
        ) -> None:
        """
Wrapper for [`rdflib.Graph.add()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=add#rdflib.Graph.add) to add a relation *(subject, predicate, object)* to the RDF graph, if it doesn't already exist.
Uses the RDF Graph as its context.

To prepare for upcoming **kglab** features, **this is the preferred method for adding relations to an RDF graph.**

    s:
*subject* node;
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node); otherwise throws a `TypeError` exception

    p:
*predicate* relation;
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node); otherwise throws a `TypeError` exception

    o:
*object* node;
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node) or [`rdflib.term.Terminal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Literal); otherwise throws a `TypeError` exception
        """
        try:
            self._g.add((s, p, o,))
        except AssertionError as e:
            traceback.print_exc()
            ic(s)
            ic(p)
            ic(o)
            raise TypeError(str(e))


    def remove (
        self,
        s: RDF_Node,
        p: RDF_Node,
        o: RDF_Node,
        ) -> None:
        """
Wrapper for [`rdflib.Graph.remove()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=add#rdflib.Graph.remove) to remove a relation *(subject, predicate, object)* from the RDF graph, if it exist.
Uses the RDF Graph as its context.

To prepare for upcoming **kglab** features, **this is the preferred method for removing relations from an RDF graph.**

    s:
*subject* node;
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node); otherwise throws a `TypeError` exception

    p:
*predicate* relation;
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node); otherwise throws a `TypeError` exception

    o:
*object* node;
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node) or [`rdflib.term.Terminal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Literal); otherwise throws a `TypeError` exception
        """
        try:
            self._g.remove((s, p, o,))
        except AssertionError as e:
            traceback.print_exc()
            ic(s)
            ic(p)
            ic(o)
            raise TypeError(str(e))


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

    _RDF_FORMAT: typing.Tuple = (
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
    )

    _ERROR_ENCODE: str = "The text `encoding` value does not match anything in the Python codec registry"
    _ERROR_PATH: str = "The `path` file object must be a writable, bytes-like object"


    @classmethod
    def _check_format (
        cls,
        format: str,
        ) -> None:
        """
Semiprivate method to error-check that a `format` parameter corresponds to a known RDFlib serialization plugin;
otherwise this throws a `TypeError` exception
        """
        if format not in cls._RDF_FORMAT:
            try:
                rdflib.plugin.get(format, rdflib.serializer.Serializer)
            except Exception:
                raise TypeError("unknown format: {}".format(format))


    @classmethod
    def _check_encoding (
        cls,
        encoding: str,
        ) -> None:
        """
Semiprivate method to error-check that an `encoding` parameter is within the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo);
otherwise this throws a `LookupError` exception
        """
        try:
            codecs.lookup(encoding)
        except LookupError:
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


    @multifile()
    def load_rdf (
        self,
        path: IOPathLike,
        *,
        format: str = "ttl",
        base: str = None,
        **args: typing.Any,
        ) -> "KnowledgeGraph":
        """
Wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from the `path` source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.
Throws `TypeError` whenever a format parser plugin encounters a syntax error.

Note: this adds relations to an RDF graph, although it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); otherwise this throws a `TypeError` exception

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
logical URI to use as the document base; if not specified, the document location gets used

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        # error checking for the `format` parameter
        if format == "json-ld":
            raise TypeError("Use the load_jsonld() method instead")

        self._check_format(format)

        # substitute the `KnowledgeGraph.base_uri` as the document base, if used
        if not base and self.base_uri:
            base = self.base_uri

        try:
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
        except rdf_n3.BadSyntax as e:
            ic(path)
            raise TypeError(str(e))

        return self


    def load_rdf_text (
        self,
        data: typing.AnyStr,
        *,
        format: str = "ttl",
        base: str = None,
        **args: typing.Any,
        ) -> "KnowledgeGraph":
        """
Wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from a text.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    data:
text representation of RDF graph data

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
logical URI to use as the document base; if not specified, the document location gets used

    returns:
this `KnowledgeGraph` object – used for method chaining
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

        return self


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
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination.
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

    format:
serialization format, which defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
optional text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking for the `format` parameter
        if format == "json-ld":
            raise TypeError("Use the save_jsonld() method instead")

        self._check_format(format)

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # substitute the `KnowledgeGraph.base_uri` base set for the graph, if used
        if not base and self.base_uri:
            base = self.base_uri

        # error checking for a file-like object `path` parameter
        if hasattr(path, "write"):
            if hasattr(path, "encoding"):
                raise TypeError(self._ERROR_PATH)

            try:
                self._g.serialize(
                    destination=path,
                    format=format,
                    base=base,
                    encoding=encoding,
                    **args,
                    )
            except io.UnsupportedOperation:
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
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to a string.

    format:
serialization format, which defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
optional text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

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


    @multifile()
    def load_jsonld (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> "KnowledgeGraph":
        """
Wrapper for [`rdflib-jsonld.parser.JsonLDParser.parse()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/parser.py) which parses an RDF graph from a [JSON-LD](https://json-ld.org/) source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

    encoding:
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # error checking for a file-like object `path` parameter
        if hasattr(path, "read"):
            f = path
        else:
            f = open(path, "r", encoding=encoding)  # type: ignore

        # load JSON from file (to verify format and trap exceptions at
        # this level) then dump to string – which is expected by the
        # JSON-LD plugin for RDFlib
        self._g.parse(
            data=json.dumps(json.load(f)),  # type: ignore
            format="json-ld",
            encoding=encoding,
            **args,
        )

        return self


    def save_jsonld (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> None:
        """
Wrapper for [`rdflib-jsonld.serializer.JsonLDSerializer.serialize()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/serializer.py) which serializes the RDF graph to the `path` destination as [JSON-LD](https://json-ld.org/).
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

    encoding:
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking for a file-like object `path` parameter
        if hasattr(path, "write"):
            if hasattr(path, "encoding"):
                raise TypeError(self._ERROR_PATH)

            f = path
        else:
            f = open(self._get_filename(path), "wb") # type: ignore

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        f.write( # type: ignore
            self._g.serialize(
                format="json-ld",
                context=self.get_context(),
                indent=2,
                encoding=encoding,
                **args,
            )
        )


    _PARQUET_COL_NAMES: typing.List[str] = [
        "subject",
        "predicate",
        "object"
    ]

    @multifile()
    def load_parquet (
        self,
        path: IOPathLike,
        **kwargs: typing.Any,
        ) -> "KnowledgeGraph":
        """
Wrapper for [`pandas.read_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html?highlight=read_parquet#pandas.read_parquet) which parses an RDF graph represented as a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.
Uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled.

To prepare for upcoming **kglab** features, **this is the preferred method for deserializing an RDF graph.**

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; a file URL can also be a path to a directory that contains multiple partitioned files, including a bucket in cloud storage – based on [`fsspec`](https://github.com/intake/filesystem_spec)

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        if self.use_gpus:
            df = cudf.read_parquet(
                path,
                **chocolate.filter_args(kwargs, pd.read_parquet)
            ).to_pandas()

        else:
            df = pd.read_parquet(
                path,
                **chocolate.filter_args(kwargs, pd.read_parquet)
            )

        df.apply(
            lambda row: self._g.parse(data="{} {} {} .".format(row[0], row[1], row[2]), format="ttl"),
            axis=1,
        )

        return self


    def save_parquet (
        self,
        path: IOPathLike,
        *,
        compression: str = "snappy",
        storage_options: dict = None, # pylint: disable=W0613
        **kwargs: typing.Any,
        ) -> None:
        """
Wrapper for [`pandas.to_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html?highlight=to_parquet) which serializes an RDF graph to a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.
Uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled.

To prepare for upcoming **kglab** features, **this is the preferred method for serializing an RDF graph.**

    path:
must be a file name (str), path object to a local file reference, or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; accessing cloud storage is based on [`fsspec`](https://github.com/intake/filesystem_spec)

    compression:
name of the compression algorithm to use; defaults to `"snappy"`; can also be `"gzip"`, `"brotli"`, or `None` for no compression

    storage_options:
extra options parsed by [`fsspec`](https://github.com/intake/filesystem_spec) for cloud storage access; **NOT USED** until `pandas` 1.2.x becomes stable across platforms and also RAPIDS provides support
        """
        rows_list: typing.List[dict] = [
            {
                self._PARQUET_COL_NAMES[0]: s.n3(),
                self._PARQUET_COL_NAMES[1]: p.n3(),
                self._PARQUET_COL_NAMES[2]: o.n3(),
            }
            for s, p, o in self._g
        ]

        if self.use_gpus:
            df = cudf.DataFrame(rows_list, columns=self._PARQUET_COL_NAMES)
        else:
            df = pd.DataFrame(rows_list, columns=self._PARQUET_COL_NAMES)

        df.to_parquet(
            path,
            compression=compression,
            #storage_options=storage_options,
            **chocolate.filter_args(kwargs, df.to_parquet),
        )


    def load_csv (
        self,
        url: str,
        ) -> "KnowledgeGraph":
        """
Wrapper for [`csvwlib`](https://github.com/DerwenAI/csvwlib) which parses a CSV file from the `path` source, then converts to RDF and merges into this RDF graph.

    url:
must be a URL represented as a string

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        new_rdf = csvwlib.CSVWConverter.to_rdf(
            url,
            mode="minimal",
            format="ttl",
        )
        return self.load_rdf_text(new_rdf)


    def _walk_roam_graph (
        self,
        obj: dict,
        seen_uid: typing.Set[str] = None,
        ) -> str:
        """
Semiprivate method to traverse the Roam Research exported graph recursively, converting its objects into RDF representation.

    obj:
object to parse

    returns:
The `uid` identifier for the parsed object
        """
        if not seen_uid:
            seen_uid = set()

        roam_ns = str(self.get_ns("roam"))
        uid = obj["uid"]

        if uid not in seen_uid:
            seen_uid.add(uid)

            # create a node for this object
            node = rdflib.URIRef(roam_ns + uid)
            self.add(node, self.get_ns("rdf").type, self.get_ns("dct").Text)

            # represent title (complex object) or string description (simple object)
            if "title" in obj:
                descrip = obj["title"]
            elif "string" in obj:
                descrip = obj["string"]

            self.add(node, self.get_ns("skos").definition, rdflib.Literal(descrip))

            # represent the user who created/edited this object
            user_uid = obj[":edit/user"][":user/uid"]
            self.add(node, self.get_ns("dct").Creator, rdflib.URIRef(roam_ns + user_uid))

            # convert millisec timestamp to Unix epoch times (UTC) to datetime
            dt = datetime.datetime.utcfromtimestamp(round(obj["edit-time"] / 1000.0))
            self.add(node, self.get_ns("dct").Date, rdflib.Literal(dt.isoformat(), datatype=rdflib.XSD.dateTime))

            if "children" in obj:
                for child_obj in obj["children"]:
                    child_uid = self._walk_roam_graph(child_obj, seen_uid)
                    self.add(node, self.get_ns("dct").references, rdflib.URIRef(roam_ns + child_uid))

        return uid


    @multifile()
    def import_roam (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        ) -> typing.List[str]:
        """
Import a graph in JSON that has been exported from the [Roam Research](https://roamresearch.com/) note-taking tool, then convert its objects and attributes into RDF representation.

For more details about the exported data from Roam Research, see:

  * <https://roamstack.com/roam-data-outside-roam/>
  * <https://nesslabs.com/roam-research-input-output>
  * <https://davidbieber.com/snippets/2020-04-25-roam-json-export/>

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

    encoding:
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

    returns:
a list of identifiers for the top-level nodes added from the Roam Research graph
        """
        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # error checking for a file-like object `path` parameter
        if hasattr(path, "read"):
            f = path
        else:
            f = open(path, "r", encoding=encoding)  # type: ignore

        # add a `roam:` prefix for a pseudo-namespace to use here,
        # which applications may need to parameterize later?
        self.add_ns("roam", "https://roamresearch.com/ns/")

        uid_list: typing.List[str] = [
            self._walk_roam_graph(obj)
            for obj in json.load(f)  # type: ignore
            ]

        return uid_list


    def n3fy (
        self,
        node: RDF_Node,
        *,
        pythonify: bool = True,
        ) -> typing.Any:
        """
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize a node into a human-readable representation using N3 format.

    node:
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

    pythonify:
flag to force instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

    returns:
text (or Python objects) for the serialized node
        """
        if pythonify and isinstance(node, rdflib.term.Literal):
            serialized = node.toPython()
        else:
            serialized = node.n3(self._g.namespace_manager)

        return serialized


    def n3fy_row (
        self,
        row_dict: dict,
        *,
        pythonify: bool = True,
        ) -> dict:
        """
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize one row of a result set from a SPARQL query into a human-readable representation for each term using N3 format.

    row_dict:
one row of a SPARQL query results, as a `dict`

    pythonify:
flag to force instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

    returns:
a dictionary of serialized row bindings
        """
        bindings = {
            k: self.n3fy(v, pythonify=pythonify)
            for k, v in row_dict.items()
        }

        return bindings


    ######################################################################
    ## SPARQL queries

    def query (
        self,
        sparql: str,
        *,
        bindings: dict = None,
        ) -> typing.Iterable:
        """
Wrapper for [`rdflib.Graph.query()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=query#rdflib.Graph.query) to perform a SPARQL query on the RDF graph.

    sparql:
text for the SPARQL query

    bindings:
initial variable bindings

    yields:
[`rdflib.query.ResultRow`](https://rdflib.readthedocs.io/en/stable/_modules/rdflib/query.html?highlight=ResultRow#) named tuples, to iterate through the query result set
        """
        if not bindings:
            bindings = {}

        for row in self._g.query(
                sparql,
                initBindings=bindings,
            ):
            yield row


    def query_as_df (
        self,
        sparql: str,
        *,
        bindings: dict = None,
        simplify: bool = True,
        pythonify: bool = True,
        ) -> pd.DataFrame:
        """
Wrapper for [`rdflib.Graph.query()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=query#rdflib.Graph.query) to perform a SPARQL query on the RDF graph.

    sparql:
text for the SPARQL query

    bindings:
initial variable bindings

    simplify:
convert terms in each row of the result set into a readable representation for each term, using N3 format

    pythonify:
convert instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

    returns:
the query result set represented as a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html); uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled
        """
        if not bindings:
            bindings = {}

        row_iter = self._g.query(sparql, initBindings=bindings)

        if simplify:
            rows_list = [ self.n3fy_row(r.asdict(), pythonify=pythonify) for r in row_iter ]
        else:
            rows_list = [ r.asdict() for r in row_iter ]

        if self.use_gpus:
            df = cudf.DataFrame(rows_list)
        else:
            df = pd.DataFrame(rows_list)

        return df


    def visualize_query (
        self,
        sparql: str,
        *,
        notebook: bool = False,
        ) -> pyvis.network.Network:
        """
Visualize the given SPARQL query as a [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network)

    sparql:
input SPARQL query to be visualized

    notebook:
optional boolean flag, whether to initialize the PyVis graph to render within a notebook; defaults to `False`

    returns:
PyVis network object, to be rendered
        """
        return GPViz(sparql, self._ns).visualize_query(notebook=notebook)


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
        inplace:typing.Optional[bool] = True,
        abort_on_error: typing.Optional[bool] = None,
        **kwargs: typing.Any,
        ) -> typing.Tuple[bool, "KnowledgeGraph", str]:
        """
Wrapper for [`pyshacl.validate()`](https://github.com/RDFLib/pySHACL) for validating the RDF graph using rules expressed in the [SHACL](https://www.w3.org/TR/shacl/) (Shapes Constraint Language).

    shacl_graph:
text representation, file path, or URL of the SHACL *shapes graph* to use in validation

    shacl_graph_format:
RDF format, if the `shacl_graph` parameter is a text representation of the *shapes graph*

    ont_graph:
text representation, file path, or URL of an optional, extra ontology to mix into the RDF graph

    ont_graph_format
RDF format, if the `ont_graph` parameter is a text representation of the extra ontology

    advanced:
enable advanced SHACL features

    inference:
prior to validation, run OWL2 RL profile-based expansion of the RDF graph based on [OWL-RL](https://github.com/RDFLib/OWL-RL); values: `"rdfs"`, `"owlrl"`, `"both"`, `None`

    inplace:
when enabled, do not clone the RDF graph prior to inference/expansion, just manipulate it in-place

    abort_on_error:
abort validation on the first error

    returns:
a tuple of `conforms` (RDF graph passes the validation rules) + `report_graph` (report as a `KnowledgeGraph` object) + `report_text` (report formatted as text)
        """
        conforms, report_graph_data, report_text = pyshacl.validate(
            self._g,
            shacl_graph=shacl_graph,
            shacl_graph_format=shacl_graph_format,
            ont_graph=ont_graph,
            ont_graph_format=ont_graph_format,
            advanced=advanced,
            inference=inference,
            inplace=inplace,
            abort_on_error=abort_on_error,
            serialize_report_graph="ttl",
            **chocolate.filter_args(kwargs, pyshacl.validate),
            )

        g = rdflib.Graph()

        g.parse(
            data=report_graph_data,
            format="ttl",
            encoding="utf-8"
        )

        report_graph = KnowledgeGraph(
            name="SHACL report graph",
            namespaces=self.get_ns_dict(),
            import_graph=g,
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

        for s, _ in self._g.subject_objects(_rdfs.subClassOf):
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
