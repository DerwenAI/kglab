"""
OWL and OWL2 terms. Note that the set of terms is *complete*, I.e., it includes *all* OWL 2 terms, regardless of
whether the term is used in OWL 2 RL or not.

**Requires**: `RDFLib`_, 4.0.0 and higher.

.. _RDFLib: https://github.com/RDFLib/rdflib

**License**: This software is available for use under the `W3C Software License`_.

.. _W3C Software License: http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231

**Organization**: `World Wide Web Consortium`_

.. _World Wide Web Consortium: http://www.w3.org

**Author**: `Ivan Herman`_

.. _Ivan Herman: http://www.w3.org/People/Ivan/
"""


import rdflib
from rdflib	import Namespace


# The OWL namespace as used for RDFLib
OWLNS = Namespace("http://www.w3.org/2002/07/owl#")

annotatedSource = OWLNS["annotatedSource"]
annotatedTarget = OWLNS["annotatedTarget"]
annotatedProperty = OWLNS["annotatedProperty"]
allValuesFrom = OWLNS["allValuesFrom"]
assertionProperty = OWLNS["assertionProperty"]
backwardCompatibleWith = OWLNS["backwardCompatibleWith"]
cardinality = OWLNS["cardinality"]
complementOf = OWLNS["complementOf"]
BottomDataProperty = OWLNS["BottomDataProperty"]
BottomObjectProperty = OWLNS["BottomObjectProperty"]
datatypeComplementOf = OWLNS["datatypeComplementOf"]
deprecated = OWLNS["deprecated"]
differentFrom = OWLNS["differentFrom"]
disjointUnionOf = OWLNS["disjointUnionOf"]
disjointClasses = OWLNS["disjointClasses"]
disjointWith = OWLNS["disjointWith"]
distinctMembers = OWLNS["distinctMembers"]
equivalentClass = OWLNS["equivalentClass"]
equivalentProperty = OWLNS["equivalentProperty"]
hasKey = OWLNS["hasKey"]
hasValue = OWLNS["hasValue"]
hasSelf = OWLNS["hasSelf"]
imports = OWLNS["imports"]
incompatibleWith = OWLNS["incompatibleWith"]
intersectionOf = OWLNS["intersectionOf"]
inverseOf = OWLNS["inverseOf"]
maxCardinality = OWLNS["maxCardinality"]
maxQualifiedCardinality = OWLNS["maxQualifiedCardinality"]
members = OWLNS["members"]
minCardinality = OWLNS["minCardinality"]
minQualifiedCardinality = OWLNS["minQualifiedCardinality"]
onClass = OWLNS["onClass"]
onDataRange = OWLNS["onDataRange"]
onDatatype = OWLNS["onDatatype"]
oneOf = OWLNS["oneOf"]
onProperty = OWLNS["onProperty"]
onProperties = OWLNS["onProperties"]
OWLpredicate = OWLNS["predicate"]
priorVersion = OWLNS["priorVersion"]
propertyChainAxiom = OWLNS["propertyChainAxiom"]
propertyDisjointWith = OWLNS["propertyDisjointWith"]
qualifiedCardinality = OWLNS["qualifiedCardinality"]
sameAs = OWLNS["sameAs"]
someValuesFrom = OWLNS["someValuesFrom"]
sourceIndividual = OWLNS["sourceIndividual"]
OWLsubject = OWLNS["subject"]
targetIndividual = OWLNS["targetIndividual"]
targetValue = OWLNS["targetValue"]
TopDataProperty = OWLNS["TopDataProperty"]
TopObjectProperty = OWLNS["TopObjectProperty"]
unionOf = OWLNS["unionOf"]
versionInfo = OWLNS["versionInfo"]
versionIRI = OWLNS["versionIRI"]
withRestrictions = OWLNS["withRestrictions"]

AllDisjointProperties = OWLNS["AllDisjointProperties"]
AllDifferent = OWLNS["AllDifferent"]
AllDisjointClasses = OWLNS["AllDisjointClasses"]
Annotation = OWLNS["Annotation"]
AnnotationProperty = OWLNS["AnnotationProperty"]
AsymmetricProperty = OWLNS["AsymmetricProperty"]
Axiom = OWLNS["Axiom"]
OWLClass = OWLNS["Class"]
DataRange = OWLNS["DataRange"]
DatatypeProperty = OWLNS["DatatypeProperty"]
DeprecatedClass = OWLNS["DeprecatedClass"]
DeprecatedProperty = OWLNS["DeprecatedProperty"]
FunctionalProperty = OWLNS["FunctionalProperty"]
InverseFunctionalProperty = OWLNS["InverseFunctionalProperty"]
IrreflexiveProperty = OWLNS["IrreflexiveProperty"]
NamedIndividual = OWLNS["NamedIndividual"]
NegativePropertyAssertion = OWLNS["NegativePropertyAssertion"]
Nothing = OWLNS["Nothing"]
ObjectProperty = OWLNS["ObjectProperty"]
Ontology = OWLNS["Ontology"]
OntologyProperty = OWLNS["OntologyProperty"]
ReflexiveProperty = OWLNS["ReflexiveProperty"]
Restriction = OWLNS["Restriction"]
Thing = OWLNS["Thing"]
SelfRestriction = OWLNS["SelfRestriction"]
SymmetricProperty = OWLNS["SymmetricProperty"]
TransitiveProperty = OWLNS["TransitiveProperty"]
