# -*- coding: utf-8 -*-
#
"""
Axiomatic triples to be (possibly) added to the final graph.

**Requires**: `RDFLib`_, 4.0.0 and higher.

.. _RDFLib: https://github.com/RDFLib/rdflib

**License**: This software is available for use under the `W3C Software License`_.

.. _W3C Software License: http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231

**Organization**: `World Wide Web Consortium`_

.. _World Wide Web Consortium: http://www.w3.org

**Author**: `Ivan Herman`_

.. _Ivan Herman: http://www.w3.org/People/Ivan/

"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = 'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

import rdflib
from owlrl.RDFS import Seq, Bag, Alt, Statement, Property, XMLLiteral, List
from owlrl.RDFS import RDFNS as ns_rdf
from owlrl.RDFS import rdf_subject, rdf_predicate, rdf_object, rdf_type, value, first, rest, nil
from owlrl.RDFS import Resource, Class, subClassOf, subPropertyOf, comment, label, rdfs_domain, rdfs_range
from owlrl.RDFS import seeAlso, isDefinedBy, Literal, Container, ContainerMembershipProperty, member, Datatype

from rdflib.namespace     import XSD as ns_xsd
from .OWL import *

# Simple RDF axiomatic triples (typing of subject, predicate, first, rest, etc)
_Simple_RDF_axiomatic_triples = [
    (rdf_type, rdf_type, Property),
    (rdf_subject, rdf_type, Property),
    (rdf_predicate, rdf_type, Property),
    (rdf_object, rdf_type, Property),
    (first, rdf_type, Property),
    (rest, rdf_type, Property),
    (value, rdf_type, Property),
    (nil, rdf_type, List),
]

# RDFS axiomatic triples (domain and range, as well as class setting for a number of RDFS symbols)
_RDFS_axiomatic_triples = [
    (rdf_type, rdfs_domain, Resource),
    (rdfs_domain, rdfs_domain, Property),
    (rdfs_range, rdfs_domain, Property),
    (subPropertyOf, rdfs_domain, Property),
    (subClassOf, rdfs_domain, Class),
    (rdf_subject, rdfs_domain, Statement),
    (rdf_predicate, rdfs_domain, Statement),
    (rdf_object, rdfs_domain, Statement),
    (member, rdfs_domain, Resource),
    (first, rdfs_domain, List),
    (rest, rdfs_domain, List),
    (seeAlso, rdfs_domain, Resource),
    (isDefinedBy, rdfs_domain, Resource),
    (comment, rdfs_domain, Resource),
    (label, rdfs_domain, Resource),
    (value, rdfs_domain, Resource),
    (Property, rdf_type, Class),

    (rdf_type, rdfs_range, Class),
    (rdfs_domain, rdfs_range, Class),
    (rdfs_range, rdfs_range, Class),
    (subPropertyOf, rdfs_range, Property),
    (subClassOf, rdfs_range, Class),
    (rdf_subject, rdfs_range, Resource),
    (rdf_predicate, rdfs_range, Resource),
    (rdf_object, rdfs_range, Resource),
    (member, rdfs_range, Resource),
    (first, rdfs_range, Resource),
    (rest, rdfs_range, List),
    (seeAlso, rdfs_range, Resource),
    (isDefinedBy, rdfs_range, Resource),
    (comment, rdfs_range, Literal),
    (label, rdfs_range, Literal),
    (value, rdfs_range, Resource),

    (Alt, subClassOf, Container),
    (Bag, subClassOf, Container),
    (Seq, subClassOf, Container),
    (ContainerMembershipProperty, subClassOf, Property),

    (isDefinedBy, subPropertyOf, seeAlso),

    (XMLLiteral, rdf_type, Datatype),
    (XMLLiteral, subClassOf, Literal),
    (Datatype, subClassOf, Class),

    # rdfs valid triples; these would be inferred by the RDFS expansion, but it may make things
    # a bit faster to add these upfront
    (Resource, rdf_type, Class),
    (Class, rdf_type, Class),
    (Literal, rdf_type, Class),
    (XMLLiteral, rdf_type, Class),
    (Datatype, rdf_type, Class),
    (Seq, rdf_type, Class),
    (Bag, rdf_type, Class),
    (Alt, rdf_type, Class),
    (Container, rdf_type, Class),
    (List, rdf_type, Class),
    (ContainerMembershipProperty, rdf_type, Class),
    (Property, rdf_type, Class),
    (Statement, rdf_type, Class),

    (rdfs_domain, rdf_type, Property),
    (rdfs_range, rdf_type, Property),
    (subPropertyOf, rdf_type, Property),
    (subClassOf, rdf_type, Property),
    (member, rdf_type, Property),
    (seeAlso, rdf_type, Property),
    (isDefinedBy, rdf_type, Property),
    (comment, rdf_type, Property),
    (label, rdf_type, Property)
]

#: RDFS Axiomatic Triples all together
RDFS_Axiomatic_Triples    = _Simple_RDF_axiomatic_triples + _RDFS_axiomatic_triples

#: RDFS D-entailement triples, ie, possible subclassing of various datatypes
RDFS_D_Axiomatic_Triples_subclasses = [
    # See http://www.w3.org/TR/2004/REC-xmlschema-2-20041028/#built-in-datatypes
    (ns_xsd['decimal'], subClassOf, Literal),

    (ns_xsd['integer'], subClassOf, ns_xsd['decimal']),

    (ns_xsd['long'], subClassOf, ns_xsd['integer']),
    (ns_xsd['int'], subClassOf, ns_xsd['long']),
    (ns_xsd['short'], subClassOf, ns_xsd['int']),
    (ns_xsd['byte'], subClassOf, ns_xsd['short']),

    (ns_xsd['nonNegativeInteger'], subClassOf, ns_xsd['integer']),
    (ns_xsd['positiveInteger'], subClassOf, ns_xsd['nonNegativeInteger']),
    (ns_xsd['unsignedLong'], subClassOf, ns_xsd['nonNegativeInteger']),
    (ns_xsd['unsignedInt'], subClassOf, ns_xsd['unsignedLong']),
    (ns_xsd['unsignedShort'], subClassOf, ns_xsd['unsignedInt']),
    (ns_xsd['unsignedByte'], subClassOf, ns_xsd['unsignedShort']),

    (ns_xsd['nonPositiveInteger'], subClassOf, ns_xsd['integer']),
    (ns_xsd['negativeInteger'], subClassOf, ns_xsd['nonPositiveInteger']),

    (ns_xsd['normalizedString'], subClassOf, ns_xsd['string']),
    (ns_xsd['token'], subClassOf, ns_xsd['normalizedString']),
    (ns_xsd['language'], subClassOf, ns_xsd['token']),
    (ns_xsd['Name'], subClassOf, ns_xsd['token']),
    (ns_xsd['NMTOKEN'], subClassOf, ns_xsd['token']),

    (ns_xsd['NCName'], subClassOf, ns_xsd['Name']),

    (ns_xsd['dateTimeStamp'], subClassOf, ns_xsd['dateTime']),
]

#:
RDFS_D_Axiomatic_Triples_types = [
    (ns_xsd['integer'], rdf_type, Datatype),
    (ns_xsd['decimal'], rdf_type, Datatype),
    (ns_xsd['nonPositiveInteger'], rdf_type, Datatype),
    (ns_xsd['nonPositiveInteger'], rdf_type, Datatype),
    (ns_xsd['positiveInteger'], rdf_type, Datatype),
    (ns_xsd['positiveInteger'], rdf_type, Datatype),
    (ns_xsd['long'], rdf_type, Datatype),
    (ns_xsd['int'], rdf_type, Datatype),
    (ns_xsd['short'], rdf_type, Datatype),
    (ns_xsd['byte'], rdf_type, Datatype),
    (ns_xsd['unsignedLong'], rdf_type, Datatype),
    (ns_xsd['unsignedInt'], rdf_type, Datatype),
    (ns_xsd['unsignedShort'], rdf_type, Datatype),
    (ns_xsd['unsignedByte'], rdf_type, Datatype),
    (ns_xsd['float'], rdf_type, Datatype),
    (ns_xsd['double'], rdf_type, Datatype),
    (ns_xsd['string'], rdf_type, Datatype),
    (ns_xsd['normalizedString'], rdf_type, Datatype),
    (ns_xsd['token'], rdf_type, Datatype),
    (ns_xsd['language'], rdf_type, Datatype),
    (ns_xsd['Name'], rdf_type, Datatype),
    (ns_xsd['NCName'], rdf_type, Datatype),
    (ns_xsd['NMTOKEN'], rdf_type, Datatype),
    (ns_xsd['boolean'], rdf_type, Datatype),
    (ns_xsd['hexBinary'], rdf_type, Datatype),
    (ns_xsd['base64Binary'], rdf_type, Datatype),
    (ns_xsd['anyURI'], rdf_type, Datatype),
    (ns_xsd['dateTimeStamp'], rdf_type, Datatype),
    (ns_xsd['dateTime'], rdf_type, Datatype),
    (Literal, rdf_type, Datatype),
    (XMLLiteral, rdf_type, Datatype),
]

RDFS_D_Axiomatic_Triples = RDFS_D_Axiomatic_Triples_types + RDFS_D_Axiomatic_Triples_subclasses

# OWL Class axiomatic triples: definition of special classes
_OWL_axiomatic_triples_Classes = [
    (AllDifferent, rdf_type, Class),
    (AllDifferent, subClassOf, Resource),

    (AllDisjointClasses, rdf_type, Class),
    (AllDisjointClasses, subClassOf, Resource),

    (AllDisjointProperties, rdf_type, Class),
    (AllDisjointProperties, subClassOf, Resource),

    (Annotation, rdf_type, Class),
    (Annotation, subClassOf, Resource),

    (AnnotationProperty, rdf_type, Class),
    (AnnotationProperty, subClassOf, Property),

    (AsymmetricProperty, rdf_type, Class),
    (AsymmetricProperty, subClassOf, Property),

    (OWLClass, rdf_type, Class),
    (OWLClass, equivalentClass, Class),

#    (DataRange, type, Class),
#    (DataRange, equivalentClass, Datatype),

    (Datatype, rdf_type, Class),

    (DatatypeProperty, rdf_type, Class),
    (DatatypeProperty, subClassOf, Property),

    (DeprecatedClass, rdf_type, Class),
    (DeprecatedClass, subClassOf, Class),

    (DeprecatedProperty, rdf_type, Class),
    (DeprecatedProperty, subClassOf, Property),

    (FunctionalProperty, rdf_type, Class),
    (FunctionalProperty, subClassOf, Property),

    (InverseFunctionalProperty, rdf_type, Class),
    (InverseFunctionalProperty, subClassOf, Property),

    (IrreflexiveProperty, rdf_type, Class),
    (IrreflexiveProperty, subClassOf, Property),

    (Literal, rdf_type, Datatype),

#    (NamedIndividual, type, Class),
#    (NamedIndividual, equivalentClass, Resource),

    (NegativePropertyAssertion, rdf_type, Class),
    (NegativePropertyAssertion, subClassOf, Resource),

    (Nothing, rdf_type, Class),
    (Nothing, subClassOf, Thing ),

    (ObjectProperty, rdf_type, Class),
    (ObjectProperty, equivalentClass, Property),

    (Ontology, rdf_type, Class),
    (Ontology, subClassOf, Resource),

    (OntologyProperty, rdf_type, Class),
    (OntologyProperty, subClassOf, Property),

    (Property, rdf_type, Class),

    (ReflexiveProperty, rdf_type, Class),
    (ReflexiveProperty, subClassOf, Property),

    (Restriction, rdf_type, Class),
    (Restriction, subClassOf, Class),


    (SymmetricProperty, rdf_type, Class),
    (SymmetricProperty, subClassOf, Property),

    (Thing, rdf_type, Class),
    (Thing, subClassOf, Resource),

    (TransitiveProperty, rdf_type, Class),
    (TransitiveProperty, subClassOf, Property),

    # OWL valid triples; some of these would be inferred by the OWL RL expansion, but it may make things
    # a bit faster to add these upfront
    (AllDisjointProperties, rdf_type, OWLClass),
    (AllDisjointClasses, rdf_type, OWLClass),
    (AllDisjointProperties, rdf_type, OWLClass),
    (Annotation, rdf_type, OWLClass),
    (AsymmetricProperty, rdf_type, OWLClass),
    (Axiom, rdf_type, OWLClass),
    (DataRange, rdf_type, OWLClass),
    (Datatype, rdf_type, OWLClass),
    (DatatypeProperty, rdf_type, OWLClass),
    (DeprecatedClass, rdf_type, OWLClass),
    (DeprecatedClass, subClassOf, OWLClass),
    (DeprecatedProperty, rdf_type, OWLClass),
    (FunctionalProperty, rdf_type, OWLClass),
    (InverseFunctionalProperty, rdf_type, OWLClass),
    (IrreflexiveProperty, rdf_type, OWLClass),
    (NamedIndividual, rdf_type, OWLClass),
    (NegativePropertyAssertion, rdf_type, OWLClass),
    (Nothing, rdf_type, OWLClass),
    (ObjectProperty, rdf_type, OWLClass),
    (Ontology, rdf_type, OWLClass),
    (OntologyProperty, rdf_type, OWLClass),
    (Property, rdf_type, OWLClass),
    (ReflexiveProperty, rdf_type, OWLClass),
    (Restriction, rdf_type, OWLClass),
    (Restriction, subClassOf, OWLClass),
#    (SelfRestriction, type, OWLClass),
    (SymmetricProperty, rdf_type, OWLClass),
    (Thing, rdf_type, OWLClass),
    (TransitiveProperty, rdf_type, OWLClass),
]

#: OWL Property axiomatic triples: definition of domains and ranges
_OWL_axiomatic_triples_Properties = [
    (allValuesFrom, rdf_type, Property),
    (allValuesFrom, rdfs_domain, Restriction),
    (allValuesFrom, rdfs_range, Class),

    (assertionProperty, rdf_type, Property),
    (assertionProperty, rdfs_domain, NegativePropertyAssertion),
    (assertionProperty, rdfs_range, Property),

    (backwardCompatibleWith, rdf_type, OntologyProperty),
    (backwardCompatibleWith, rdf_type, AnnotationProperty),
    (backwardCompatibleWith, rdfs_domain, Ontology),
    (backwardCompatibleWith, rdfs_range, Ontology),

#    (bottomDataProperty, type, DatatypeProperty),

#    (bottomObjectProperty, type, ObjectProperty),

#    (cardinality, type, Property),
#    (cardinality, domain, Restriction),
#    (cardinality, range, ns_xsd["nonNegativeInteger"]),

    (comment, rdf_type, AnnotationProperty),
    (comment, rdfs_domain, Resource),
    (comment, rdfs_range, Literal),

    (complementOf, rdf_type, Property),
    (complementOf, rdfs_domain, Class),
    (complementOf, rdfs_range, Class),

#    (datatypeComplementOf, type, Property),
#    (datatypeComplementOf, domain, Datatype),
#    (datatypeComplementOf, range, Datatype),

    (deprecated, rdf_type, AnnotationProperty),
    (deprecated, rdfs_domain, Resource),
    (deprecated, rdfs_range, Resource),

    (differentFrom, rdf_type, Property),
    (differentFrom, rdfs_domain, Resource),
    (differentFrom, rdfs_range, Resource),

#    (disjointUnionOf, type, Property),
#    (disjointUnionOf, domain, Class),
#    (disjointUnionOf, range, List),

    (disjointWith, rdf_type, Property),
    (disjointWith, rdfs_domain, Class),
    (disjointWith, rdfs_range, Class),

    (distinctMembers, rdf_type, Property),
    (distinctMembers, rdfs_domain, AllDifferent),
    (distinctMembers, rdfs_range, List),

    (equivalentClass, rdf_type, Property),
    (equivalentClass, rdfs_domain, Class),
    (equivalentClass, rdfs_range, Class),

    (equivalentProperty, rdf_type, Property),
    (equivalentProperty, rdfs_domain, Property),
    (equivalentProperty, rdfs_range, Property),

    (hasKey, rdf_type, Property),
    (hasKey, rdfs_domain, Class),
    (hasKey, rdfs_range, List),

    (hasValue, rdf_type, Property),
    (hasValue, rdfs_domain, Restriction),
    (hasValue, rdfs_range, Resource),

    (imports, rdf_type, OntologyProperty),
    (imports, rdfs_domain, Ontology),
    (imports, rdfs_range, Ontology),

    (incompatibleWith, rdf_type, OntologyProperty),
    (incompatibleWith, rdf_type, AnnotationProperty),
    (incompatibleWith, rdfs_domain, Ontology),
    (incompatibleWith, rdfs_range, Ontology),

    (intersectionOf, rdf_type, Property),
    (intersectionOf, rdfs_domain, Class),
    (intersectionOf, rdfs_range, List),

    (inverseOf, rdf_type, Property),
    (inverseOf, rdfs_domain, Property),
    (inverseOf, rdfs_range, Property),

    (isDefinedBy, rdf_type, AnnotationProperty),
    (isDefinedBy, rdfs_domain, Resource),
    (isDefinedBy, rdfs_range, Resource),

    (label, rdf_type, AnnotationProperty),
    (label, rdfs_domain, Resource),
    (label, rdfs_range, Literal),

    (maxCardinality, rdf_type, Property),
    (maxCardinality, rdfs_domain, Restriction),
    (maxCardinality, rdfs_range, ns_xsd["nonNegativeInteger"]),

    (maxQualifiedCardinality, rdf_type, Property),
    (maxQualifiedCardinality, rdfs_domain, Restriction),
    (maxQualifiedCardinality, rdfs_range, ns_xsd["nonNegativeInteger"]),

    (members, rdf_type, Property),
    (members, rdfs_domain, Resource),
    (members, rdfs_range, List),

#    (minCardinality, type, Property),
#    (minCardinality, domain, Restriction),
#    (minCardinality, range, ns_xsd["nonNegativeInteger"]),

#    (minQualifiedCardinality, type, Property),
#    (minQualifiedCardinality, domain, Restriction),
#    (minQualifiedCardinality, range, ns_xsd["nonNegativeInteger"]),

#    (annotatedTarget, type, Property),
#    (annotatedTarget, domain, Resource),
#    (annotatedTarget, range, Resource),

    (onClass, rdf_type, Property),
    (onClass, rdfs_domain, Restriction),
    (onClass, rdfs_range, Class),

#    (onDataRange, type, Property),
#    (onDataRange, domain, Restriction),
#    (onDataRange, range, Datatype),

    (onDatatype, rdf_type, Property),
    (onDatatype, rdfs_domain, Datatype),
    (onDatatype, rdfs_range, Datatype),

    (oneOf, rdf_type, Property),
    (oneOf, rdfs_domain, Class),
    (oneOf, rdfs_range, List),

    (onProperty, rdf_type, Property),
    (onProperty, rdfs_domain, Restriction),
    (onProperty, rdfs_range, Property),

#    (onProperties, type, Property),
#    (onProperties, domain, Restriction),
#    (onProperties, range, List),

#    (annotatedProperty, type, Property),
#    (annotatedProperty, domain, Resource),
#    (annotatedProperty, range, Property),

    (priorVersion, rdf_type, OntologyProperty),
    (priorVersion, rdf_type, AnnotationProperty),
    (priorVersion, rdfs_domain, Ontology),
    (priorVersion, rdfs_range, Ontology),

    (propertyChainAxiom, rdf_type, Property),
    (propertyChainAxiom, rdfs_domain, Property),
    (propertyChainAxiom, rdfs_range, List),

#    (propertyDisjointWith, type, Property),
#    (propertyDisjointWith, domain, Property),
#    (propertyDisjointWith, range, Property),
#
#    (qualifiedCardinality, type, Property),
#    (qualifiedCardinality, domain, Restriction),
#    (qualifiedCardinality, range, ns_xsd["nonNegativeInteger"]),

    (sameAs, rdf_type, Property),
    (sameAs, rdfs_domain, Resource),
    (sameAs, rdfs_range, Resource),

    (seeAlso, rdf_type, AnnotationProperty),
    (seeAlso, rdfs_domain, Resource),
    (seeAlso, rdfs_range, Resource),

    (someValuesFrom, rdf_type, Property),
    (someValuesFrom, rdfs_domain, Restriction),
    (someValuesFrom, rdfs_range, Class),

    (sourceIndividual, rdf_type, Property),
    (sourceIndividual, rdfs_domain, NegativePropertyAssertion),
    (sourceIndividual, rdfs_range, Resource),
#
#    (annotatedSource, type, Property),
#    (annotatedSource, domain, Resource),
#    (annotatedSource, range, Resource),
#
    (targetIndividual, rdf_type, Property),
    (targetIndividual, rdfs_domain, NegativePropertyAssertion),
    (targetIndividual, rdfs_range, Resource),

    (targetValue, rdf_type, Property),
    (targetValue, rdfs_domain, NegativePropertyAssertion),
    (targetValue, rdfs_range, Literal),

#    (topDataProperty, type, DatatypeProperty),
#    (topDataProperty, domain, Resource),
#    (topDataProperty, range, Literal),
#
#    (topObjectProperty, type, ObjectProperty),
#    (topObjectProperty, domain, Resource),
#    (topObjectProperty, range, Resource),

    (unionOf, rdf_type, Property),
    (unionOf, rdfs_domain, Class),
    (unionOf, rdfs_range, List),

    (versionInfo, rdf_type, AnnotationProperty),
    (versionInfo, rdfs_domain, Resource),
    (versionInfo, rdfs_range, Resource),

    (versionIRI, rdf_type, AnnotationProperty),
    (versionIRI, rdfs_domain, Resource),
    (versionIRI, rdfs_range, Resource),

    (withRestrictions, rdf_type, Property),
    (withRestrictions, rdfs_domain, Datatype),
    (withRestrictions, rdfs_range, List),

    # some OWL valid triples; these would be inferred by the OWL RL expansion, but it may make things
    # a bit faster to add these upfront
    (allValuesFrom, rdfs_range, OWLClass),
    (complementOf, rdfs_domain, OWLClass),
    (complementOf, rdfs_range, OWLClass),

#    (datatypeComplementOf, domain, DataRange),
#    (datatypeComplementOf, range, DataRange),
    (disjointUnionOf, rdfs_domain, OWLClass),
    (disjointWith, rdfs_domain, OWLClass),
    (disjointWith, rdfs_range, OWLClass),
    (equivalentClass, rdfs_domain, OWLClass),
    (equivalentClass, rdfs_range, OWLClass),
    (hasKey, rdfs_domain, OWLClass),
    (intersectionOf, rdfs_domain, OWLClass),
    (onClass, rdfs_range, OWLClass),
#    (onDataRange, range, DataRange),
    (onDatatype, rdfs_domain, DataRange),
    (onDatatype, rdfs_range, DataRange),
    (oneOf, rdfs_domain, OWLClass),
    (someValuesFrom, rdfs_range, OWLClass),
    (unionOf, rdfs_range, OWLClass),
#    (withRestrictions, domain, DataRange)
]

#: OWL RL axiomatic triples: combination of the RDFS triples plus the OWL specific ones
OWLRL_Axiomatic_Triples   = _OWL_axiomatic_triples_Classes   + _OWL_axiomatic_triples_Properties

# Note that this is not used anywhere. But I encoded it once and I did not want to remove it...:-)
_OWL_axiomatic_triples_Facets = [
    # langPattern
    (ns_xsd['length'], rdf_type, Property),
    (ns_xsd['maxExclusive'], rdf_type, Property),
    (ns_xsd['maxInclusive'], rdf_type, Property),
    (ns_xsd['maxLength'], rdf_type, Property),
    (ns_xsd['minExclusive'], rdf_type, Property),
    (ns_xsd['minInclusive'], rdf_type, Property),
    (ns_xsd['minLength'], rdf_type, Property),
    (ns_xsd['pattern'], rdf_type, Property),

    (ns_xsd['length'], rdfs_domain, Resource),
    (ns_xsd['maxExclusive'], rdfs_domain, Resource),
    (ns_xsd['maxInclusive'], rdfs_domain, Resource),
    (ns_xsd['maxLength'], rdfs_domain, Resource),
    (ns_xsd['minExclusive'], rdfs_domain, Resource),
    (ns_xsd['minInclusive'], rdfs_domain, Resource),
    (ns_xsd['minLength'], rdfs_domain, Resource),
    (ns_xsd['pattern'], rdfs_domain, Resource),
    (ns_xsd['length'], rdfs_domain, Resource),

    (ns_xsd['maxExclusive'], rdfs_range, Literal),
    (ns_xsd['maxInclusive'], rdfs_range, Literal),
    (ns_xsd['maxLength'], rdfs_range, Literal),
    (ns_xsd['minExclusive'], rdfs_range, Literal),
    (ns_xsd['minInclusive'], rdfs_range, Literal),
    (ns_xsd['minLength'], rdfs_range, Literal),
    (ns_xsd['pattern'], rdfs_range, Literal),
]

#: OWL D-entailment triples (additionally to the RDFS ones), ie, possible subclassing of various extra datatypes
_OWL_D_Axiomatic_Triples_types = [
    (ns_rdf['PlainLiteral'], rdf_type, Datatype)
]

#:
OWL_D_Axiomatic_Triples_subclasses = [
    (ns_xsd['string'], subClassOf, ns_rdf['PlainLiteral']),
    (ns_xsd['normalizedString'], subClassOf, ns_rdf['PlainLiteral']),
    (ns_xsd['token'], subClassOf, ns_rdf['PlainLiteral']),
    (ns_xsd['Name'], subClassOf, ns_rdf['PlainLiteral']),
    (ns_xsd['NCName'], subClassOf, ns_rdf['PlainLiteral']),
    (ns_xsd['NMTOKEN'], subClassOf, ns_rdf['PlainLiteral'])
]

#:
OWLRL_Datatypes_Disjointness = [
    (ns_xsd["anyURI"], disjointWith, ns_xsd['base64Binary']),
    (ns_xsd["anyURI"], disjointWith, ns_xsd['boolean']),
    (ns_xsd["anyURI"], disjointWith, ns_xsd['dateTime']),
    (ns_xsd["anyURI"], disjointWith, ns_xsd['decimal']),
    (ns_xsd["anyURI"], disjointWith, ns_xsd['double']),
    (ns_xsd["anyURI"], disjointWith, ns_xsd['float']),
    (ns_xsd["anyURI"], disjointWith, ns_xsd['hexBinary']),
    (ns_xsd["anyURI"], disjointWith, ns_xsd['string']),
    (ns_xsd["anyURI"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["anyURI"], disjointWith, XMLLiteral),

    (ns_xsd["base64Binary"], disjointWith, ns_xsd['boolean']),
    (ns_xsd["base64Binary"], disjointWith, ns_xsd['dateTime']),
    (ns_xsd["base64Binary"], disjointWith, ns_xsd['decimal']),
    (ns_xsd["base64Binary"], disjointWith, ns_xsd['double']),
    (ns_xsd["base64Binary"], disjointWith, ns_xsd['float']),
    (ns_xsd["base64Binary"], disjointWith, ns_xsd['hexBinary']),
    (ns_xsd["base64Binary"], disjointWith, ns_xsd['string']),
    (ns_xsd["base64Binary"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["base64Binary"], disjointWith, XMLLiteral),

    (ns_xsd["boolean"], disjointWith, ns_xsd['dateTime']),
    (ns_xsd["boolean"], disjointWith, ns_xsd['decimal']),
    (ns_xsd["boolean"], disjointWith, ns_xsd['double']),
    (ns_xsd["boolean"], disjointWith, ns_xsd['float']),
    (ns_xsd["boolean"], disjointWith, ns_xsd['hexBinary']),
    (ns_xsd["boolean"], disjointWith, ns_xsd['string']),
    (ns_xsd["boolean"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["boolean"], disjointWith, XMLLiteral),

    (ns_xsd["dateTime"], disjointWith, ns_xsd['decimal']),
    (ns_xsd["dateTime"], disjointWith, ns_xsd['double']),
    (ns_xsd["dateTime"], disjointWith, ns_xsd['float']),
    (ns_xsd["dateTime"], disjointWith, ns_xsd['hexBinary']),
    (ns_xsd["dateTime"], disjointWith, ns_xsd['string']),
    (ns_xsd["dateTime"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["dateTime"], disjointWith, XMLLiteral),

    (ns_xsd["decimal"], disjointWith, ns_xsd['double']),
    (ns_xsd["decimal"], disjointWith, ns_xsd['float']),
    (ns_xsd["decimal"], disjointWith, ns_xsd['hexBinary']),
    (ns_xsd["decimal"], disjointWith, ns_xsd['string']),
    (ns_xsd["decimal"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["decimal"], disjointWith, XMLLiteral),

    (ns_xsd["double"], disjointWith, ns_xsd['float']),
    (ns_xsd["double"], disjointWith, ns_xsd['hexBinary']),
    (ns_xsd["double"], disjointWith, ns_xsd['string']),
    (ns_xsd["double"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["double"], disjointWith, XMLLiteral),

    (ns_xsd["float"], disjointWith, ns_xsd['hexBinary']),
    (ns_xsd["float"], disjointWith, ns_xsd['string']),
    (ns_xsd["float"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["float"], disjointWith, XMLLiteral),

    (ns_xsd["hexBinary"], disjointWith, ns_xsd['string']),
    (ns_xsd["hexBinary"], disjointWith, ns_rdf['PlainLiteral']),
    (ns_xsd["hexBinary"], disjointWith, XMLLiteral),

    (ns_xsd["string"], disjointWith, XMLLiteral),
]

#: OWL RL D Axiomatic triples: combination of the RDFS ones, plus some extra statements on ranges and domains, plus
#: some OWL specific datatypes
OWLRL_D_Axiomatic_Triples = RDFS_D_Axiomatic_Triples + _OWL_D_Axiomatic_Triples_types + \
                            OWL_D_Axiomatic_Triples_subclasses + OWLRL_Datatypes_Disjointness



