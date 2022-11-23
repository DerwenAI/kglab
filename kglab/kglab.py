"""
Main class definitions for `kglab`

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

## Python standard libraries
import traceback
import typing

### third-parties libraries
from icecream import ic  # type: ignore
import dateutil.parser as dup
import pandas as pd  # type: ignore

import rdflib  # type: ignore
import rdflib.plugin  # type: ignore

## kglab - core classes
from .pkg_types import GraphLike, RDF_Node
from .util import get_gpu_count
from .version import _check_version
from .query.sparql import SparqlQueryable
from .query.mixin import QueryingMixin
from .serde import SerdeMixin
from .standards import ShaclOwlRdfSkosMixin


## pre-constructor set-up
_check_version()

if get_gpu_count() > 0:
    import cudf  # type: ignore


class KnowledgeGraph(QueryingMixin, SerdeMixin, ShaclOwlRdfSkosMixin):
    """
This is the primary class used to represent RDF graphs, on which the other classes are dependent.
See <https://derwen.ai/docs/kgl/concepts/#knowledge-graph>

Core feature areas include:

  * namespace management: ontology, controlled vocabularies
  * graph construction
  * serialization-deserilization (see `serde` module)
  * SPARQL querying (see `query.mixin` module)
  * SHACL validation (see `standards` module)
  * inference based on OWL-RL, RDFS, SKOS (see `standards` module)
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
        base_uri: typing.Optional[str] = None,
        language: str = "en",
        store: typing.Optional[str] = None,
        use_gpus: bool = True,
        import_graph: typing.Optional[GraphLike] = None,
        namespaces: typing.Optional[dict] = None,
        ) -> None:
        """
Constructor for a `KnowledgeGraph` object.

    name:
optional, internal name for this graph

    base_uri:
the default [*base URI*](https://tools.ietf.org/html/rfc3986#section-5.1) for this RDF graph

    language:
the default [*language tag*](https://www.w3.org/TR/rdf11-concepts/#dfn-language-tag), e.g., used for [*language indexing*](https://www.w3.org/TR/json-ld11/#language-indexing)

    store:
optionally, string representing an `rdflib.Store` plugin to use.

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
        self.store = store

        # use NVidia GPU devices if available and the libraries
        # have been installed and the flag is not disabled
        if use_gpus is not None and get_gpu_count() > 0:
            self.use_gpus = True
        else:
            self.use_gpus = False

        # import relations from another RDF graph, or start from blank
        if import_graph is not None:
            self._g = import_graph
        else:
            self._g = self.build_blank_graph() # pylint: disable=E1101

        # initialize the namespaces
        self._ns: dict = {}

        for prefix, iri in self._DEFAULT_NAMESPACES.items():
            self.add_ns(prefix, iri) # pylint: disable=E1101

        if namespaces:
            for prefix, iri in namespaces.items():
                self.add_ns(prefix, iri) # pylint: disable=E1101

        # backwards compatibility for class refactoring
        self.sparql = SparqlQueryable(self)


    def build_blank_graph (
        self,
        ) -> rdflib.Graph:
        """
Build a new `rdflib.Graph` object, based on storage plugin configuration.
        """
        if self.store is not None:
            g = rdflib.Graph(store=self.store)
        else:
            g = rdflib.Graph()

        return g


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

        self._g.namespace_manager.bind( # type: ignore
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

        nm = self._g.namespace_manager  # type: ignore

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
        return rdflib.Literal(date_tz, datatype=self.get_ns("xsd").dateTime) # pylint: disable=E1101


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
            self._g.add((s, p, o,))  # type: ignore
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
            self._g.remove((s, p, o,)) # type: ignore
        except AssertionError as e:
            traceback.print_exc()
            ic(s)
            ic(p)
            ic(o)
            raise TypeError(str(e))


    def graph_factory(self, name, graph):
        """
Utility function to generate graphs from mixins

        name:
name of the graph

        graph:
initial graph
        """
        return KnowledgeGraph(
            name=name,
            namespaces=self.get_ns_dict(),
            import_graph=graph,
        )
