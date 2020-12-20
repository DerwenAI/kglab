"""
RDF(S) terms. Note that the set of terms is *complete*, i.e., it includes *all* OWL 2 terms, regardless of whether the
term is used in OWL 2 RL or not.

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
from rdflib				import Namespace

RDFNS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFSNS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# RDF Classes
Seq = RDFNS["Seq"]
Bag = RDFNS["Bag"]
Alt = RDFNS["Alt"]
Statement = RDFNS["Statement"]
Property = RDFNS["Property"]
XMLLiteral = RDFNS["XMLLiteral"]
HTMLLiteral = RDFNS["HTML"]
LangString = RDFNS["LangString"]
List = RDFNS["List"]

# RDF Properties
rdf_subject = RDFNS["subject"]
rdf_predicate = RDFNS["predicate"]
rdf_object = RDFNS["object"]
rdf_type = RDFNS["type"]
value = RDFNS["value"]
first = RDFNS["first"]
rest = RDFNS["rest"]
# and _n where n is a non-negative integer

# RDF Resources
nil = RDFNS["nil"]

Resource = RDFSNS["Resource"]
Class = RDFSNS["Class"]
subClassOf = RDFSNS["subClassOf"]
subPropertyOf = RDFSNS["subPropertyOf"]
comment = RDFSNS["comment"]
label = RDFSNS["label"]
rdfs_domain = RDFSNS["domain"]
rdfs_range = RDFSNS["range"]
seeAlso = RDFSNS["seeAlso"]
isDefinedBy = RDFSNS["isDefinedBy"]
Literal = RDFSNS["Literal"]
Container = RDFSNS["Container"]
ContainerMembershipProperty = RDFSNS["ContainerMembershipProperty"]
member = RDFSNS["member"]
Datatype = RDFSNS["Datatype"]
