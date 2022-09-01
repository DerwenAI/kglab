"""
Main class definitions for `kglab`

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

## Python standard libraries
import traceback
import typing

### third-parties libraries
from icecream import ic  # type: ignore
import chocolate  # type: ignore
import dateutil.parser as dup
import owlrl  # type: ignore
import pandas as pd  # type: ignore
import pyshacl  # type: ignore

import rdflib  # type: ignore
import rdflib.plugin  # type: ignore

## kglab - core classes
from kglab.decorators import multifile
from kglab.pkg_types import GraphLike, RDF_Node
from kglab.gpviz import GPViz
from kglab.util import get_gpu_count
from kglab.version import _check_version
import kglab.query.sparql
from kglab.query.mixin import QueryingMixin
from kglab.serde import SerdeMixin


## pre-constructor set-up
_check_version()

if get_gpu_count() > 0:
    import cudf  # type: ignore


class KnowledgeGraph(QueryingMixin, SerdeMixin):
    """
This is the primary class used to represent RDF graphs, on which the other classes are dependent.
See <https://derwen.ai/docs/kgl/concepts/#knowledge-graph>

Core feature areas include:

  * namespace management (ontology, controlled vocabularies)
  * graph construction
  * serialization-deserilization (see mixin)
  * SPARQL querying (see mixin)
  * SHACL validation
  * inference based on OWL-RL, RDFS, SKOS

Authored by: Paco Nathan
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
        store: str = None,
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
            self._g = self.build_blank_graph()

        # initialize the namespaces
        self._ns: dict = {}

        for prefix, iri in self._DEFAULT_NAMESPACES.items():
            self.add_ns(prefix, iri)

        if namespaces:
            for prefix, iri in namespaces.items():
                self.add_ns(prefix, iri)

        # backwards compatibility for class refactoring
        self.sparql = kglab.query.sparql.SparqlQueryable(self)


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
        abort_on_first: typing.Optional[bool] = None,
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

    abort_on_first:
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
            abort_on_first=abort_on_first,
            serialize_report_graph="ttl",
            **chocolate.filter_args(kwargs, pyshacl.validate),
            )

        g = self.build_blank_graph()

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
