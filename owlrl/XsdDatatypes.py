# -*- coding: utf-8 -*-
#
"""
Lists of XSD datatypes and their mutual relationships

**Requires**: `RDFLib`_, 4.0.0 and higher.

.. _RDFLib: https://github.com/RDFLib/rdflib

**License**: This software is available for use under the `W3C Software License`_.

.. _W3C Software License: http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231

**Organization**: `World Wide Web Consortium`_

.. _World Wide Web Consortium: http://www.w3.org

**Author**: `Ivan Herman`_

.. _Ivan Herman: http://www.w3.org/People/Ivan/

"""
__author__ = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = 'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

# noinspection PyPep8Naming
from .RDFS import RDFNS as ns_rdf
from .RDFS import Literal
from .RDFS import XMLLiteral
from .RDFS import HTMLLiteral
from .RDFS import LangString

import rdflib
# noinspection PyPep8Naming
from rdflib.namespace import XSD as ns_xsd

#: The basic XSD types used everywhere; this means not the complete set of day/month types
_Common_XSD_Datatypes = [
    ns_xsd['integer'], ns_xsd['decimal'], ns_xsd['nonNegativeInteger'], ns_xsd['nonPositiveInteger'],
    ns_xsd['negativeInteger'], ns_xsd['positiveInteger'], ns_xsd['long'], ns_xsd['int'], ns_xsd['short'],
    ns_xsd['byte'], ns_xsd['unsignedLong'], ns_xsd['unsignedInt'], ns_xsd['unsignedShort'],
    ns_xsd['unsignedByte'], ns_xsd['float'], ns_xsd['double'], ns_xsd['string'], ns_xsd['normalizedString'],
    ns_xsd['token'], ns_xsd['language'], ns_xsd['Name'], ns_xsd['NCName'], ns_xsd['NMTOKEN'],
    ns_xsd['boolean'], ns_xsd['hexBinary'], ns_xsd['base64Binary'], ns_xsd['anyURI'],
    ns_xsd['dateTimeStamp'], ns_xsd['dateTime'], ns_xsd['time'], ns_xsd['date'],
    Literal, XMLLiteral, HTMLLiteral, LangString
]

#: RDFS Datatypes: the basic ones plus the complete set of day/month ones
RDFS_Datatypes = _Common_XSD_Datatypes + [ns_xsd['gYearMonth'], ns_xsd['gMonthDay'], ns_xsd['gYear'],
                                          ns_xsd['gDay'], ns_xsd['gMonth']]

#: OWL RL Datatypes: the basic ones plus plain literal
OWL_RL_Datatypes = _Common_XSD_Datatypes + [ns_rdf['PlainLiteral']]

#: XSD Datatype subsumptions
_Common_Datatype_Subsumptions = {
    ns_xsd['dateTimeStamp']: [ns_xsd['dateTime']],
    ns_xsd['integer']: [ns_xsd['decimal']],
    ns_xsd['long']: [ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['int']: [ns_xsd['long'], ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['short']: [ns_xsd['int'], ns_xsd['long'], ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['byte']: [ns_xsd['short'], ns_xsd['int'], ns_xsd['long'], ns_xsd['integer'], ns_xsd['decimal']],

    ns_xsd['nonNegativeInteger']: [ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['positiveInteger']: [ns_xsd['nonNegativeInteger'], ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['unsignedLong']: [ns_xsd['nonNegativeInteger'], ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['unsignedInt']: [ns_xsd['unsignedLong'], ns_xsd['nonNegativeInteger'], ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['unsignedShort']: [ns_xsd['unsignedInt'], ns_xsd['unsignedLong'], ns_xsd['nonNegativeInteger'],
                              ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['unsignedByte']: [ns_xsd['unsignedShort'], ns_xsd['unsignedInt'], ns_xsd['unsignedLong'],
                             ns_xsd['nonNegativeInteger'], ns_xsd['integer'], ns_xsd['decimal']],

    ns_xsd['nonPositiveInteger']: [ns_xsd['integer'], ns_xsd['decimal']],
    ns_xsd['negativeInteger']: [ns_xsd['nonPositiveInteger'], ns_xsd['integer'], ns_xsd['decimal']],

    ns_xsd['normalizedString']: [ns_xsd["string"]],
    ns_xsd['token']: [ns_xsd['normalizedString'], ns_xsd["string"]],
    ns_xsd['language']: [ns_xsd['token'], ns_xsd['normalizedString'], ns_xsd["string"]],
    ns_xsd['Name']: [ns_xsd['token'], ns_xsd['normalizedString'], ns_xsd["string"]],
    ns_xsd['NCName']: [ns_xsd['Name'], ns_xsd['token'], ns_xsd['normalizedString'], ns_xsd["string"]],
    ns_xsd['NMTOKEN']: [ns_xsd['Name'], ns_xsd['token'], ns_xsd['normalizedString'], ns_xsd["string"]],
}

#: RDFS Datatype subsumptions: at the moment, there is no extra to XSD
RDFS_Datatype_Subsumptions = _Common_Datatype_Subsumptions

#: OWL Datatype subsumptions: at the moment, there is no extra to XSD
OWL_Datatype_Subsumptions = _Common_Datatype_Subsumptions
