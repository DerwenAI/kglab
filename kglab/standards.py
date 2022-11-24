"""
Mixin class to provide SHACL- OWL- and RDF-related functionalities for `KnowledgeGraph`

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

## Python standard libraries
import typing

### third-parties libraries
import chocolate  # type: ignore
import owlrl  # type: ignore
import pyshacl  # type: ignore

## kglab - core classes
from .pkg_types import GraphLike
from .util import Mixin


class ShaclOwlRdfSkosMixin (Mixin):
    """
Provide methods for SHACL- OWL- and RDF-related operations.
    """
    _g: typing.Optional[GraphLike]

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
        ) -> typing.Tuple[bool, "KnowledgeGraph", str]: # type: ignore
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

        report_graph = self.graph_factory(
            name="SHACL report graph",
            graph=g,
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

        for s, o in self._g.subject_objects(_rdfs.subPropertyOf): # type: ignore
            super_props.setdefault(s, set())

            for sub_prop in self._g.transitive_objects(s, _rdfs.subPropertyOf): # type: ignore
                if sub_prop != s:
                    super_props[s].add(sub_prop)

        # add super-property relationships
        for p, sup_prop_list in super_props.items():
            for s, o in self._g.subject_objects(p): # type: ignore
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

        for s, _ in self._g.subject_objects(_rdfs.subClassOf): # type: ignore
            super_classes.setdefault(s, set())

            for sup_class in self._g.transitive_objects(s, _rdfs.subClassOf): # type: ignore
                if sup_class != s:
                    super_classes[s].add(sup_class)

        # set the superclass type information for subclass instances
        for s, sup_class_list in super_classes.items():
            for sub_inst in self._g.subjects(self.get_ns("rdf").type, s): # type: ignore
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

        for s, o in self._g.subject_objects(_skos.related): # type: ignore
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

        for s, o in self._g.subject_objects(_skos.hasTopConcept): # type: ignore
            self.add(o, _skos.topConceptOf, s)

        for s, o in self._g.subject_objects(_skos.topConceptOf): # type: ignore
            self.add(o, _skos.hasTopConcept, s)

        for s, o in self._g.subject_objects(_skos.topConceptOf): # type: ignore
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
            for s, o in self._g.subject_objects(_skos.broader): # type: ignore
                self.add(o, _skos.narrower, s)

        for s, o in self._g.subject_objects(_skos.narrower): # type: ignore
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

        for concept in self._g.subjects(self.get_ns("rdf").type, _skos.Concept): # type: ignore
            for broader_concept in self._g.transitive_objects(concept, _skos.broader): # type: ignore
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

        for s, o in self._g.subject_objects(_skos.relatedMatch): # type: ignore
            self.add(o, _skos.relatedMatch, s)

            if related:
                self.add(s, _skos.related, o)
                self.add(o, _skos.related, s)

        for s, o in self._g.subject_objects(_skos.closeMatch): # type: ignore
            self.add(o, _skos.closeMatch, s)

        for s, o in self._g.subject_objects(_skos.exactMatch): # type: ignore
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

        for s, o in self._g.subject_objects(_skos.broadMatch): # type: ignore
            self.add(s, _skos.broader, o)

            if narrower:
                self.add(o, _skos.narrowMatch, s)
                self.add(o, _skos.narrower, s)

        for s, o in self._g.subject_objects(_skos.narrowMatch): # type: ignore
            self.add(o, _skos.broadMatch, s)
            self.add(o, _skos.broader, s)

            if narrower:
                self.add(s, _skos.narrower, o)
            else:
                self.remove(s, _skos.narrowMatch, o)
