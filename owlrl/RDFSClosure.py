# -*- coding: utf-8 -*-
#
"""
This module is brute force implementation of the RDFS semantics on the top of RDFLib (with some caveats, see in the
introductory text).


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

import rdflib
from itertools import product

from owlrl.RDFS import Property, rdf_type
from owlrl.RDFS import Resource, Class, subClassOf, subPropertyOf, rdfs_domain, rdfs_range
from owlrl.RDFS import Literal, ContainerMembershipProperty, member, Datatype
# noinspection PyPep8Naming
from owlrl.RDFS import RDFNS as ns_rdf

from owlrl.Closure import Core
from owlrl.AxiomaticTriples import RDFS_Axiomatic_Triples, RDFS_D_Axiomatic_Triples


######################################################################################################

# RDFS Semantics class
# noinspection PyPep8Naming
class RDFS_Semantics(Core):
    """
    RDFS Semantics class, ie, implementation of the RDFS closure graph.

    .. note:: Note that the module does *not* implement the so called Datatype entailment rules, simply because the
        underlying RDFLib does not implement the datatypes (ie, RDFLib will not make the literal "1.00" and "1.00000"
        identical, although even with all the ambiguities on datatypes, this I{should} be made equal...).

        Also, the so-called extensional entailment rules (Section 7.3.1 in the RDF Semantics document) have not been
        implemented either.

    The comments and references to the various rule follow the names as used in the `RDF Semantics document`_.

    .. _RDF Semantics document: http://www.w3.org/TR/rdf-mt/

    :param graph: The RDF graph to be extended.
    :type graph: :class:`rdflib.Graph`

    :param axioms: Whether (non-datatype) axiomatic triples should be added or not.
    :type axioms: bool

    :param daxioms: Whether datatype axiomatic triples should be added or not.
    :type daxioms: bool

    :param rdfs: Whether RDFS inference is also done (used in subclassed only).
    :type rdfs: bool
    """
    def __init__(self, graph, axioms, daxioms, rdfs):
        """
        @param graph: the RDF graph to be extended
        @type graph: rdflib.Graph
        @param axioms: whether (non-datatype) axiomatic triples should be added or not
        @type axioms: bool
        @param daxioms: whether datatype axiomatic triples should be added or not
        @type daxioms: bool
        @param rdfs: whether RDFS inference is also done (used in subclassed only)
        @type rdfs: boolean
        """
        Core.__init__(self, graph, axioms, daxioms, rdfs)

    def add_axioms(self):
        """
        Add axioms
        """
        for t in RDFS_Axiomatic_Triples:
            self.graph.add(t)
        for i in range(1, self.IMaxNum + 1):
            ci = ns_rdf[("_%d" % i)]
            self.graph.add((ci, rdf_type, Property))
            self.graph.add((ci, rdfs_domain, Resource))
            self.graph.add((ci, rdfs_range, Resource))
            self.graph.add((ci, rdf_type, ContainerMembershipProperty))

    def add_d_axioms(self):
        """
        This is not really complete, because it just uses the comparison possibilities that RDFLib provides.
        """
        # #1
        literals = (lt for lt in self._literals() if lt.datatype is not None)
        for lt in literals:
            self.graph.add((lt, rdf_type, lt.datatype))

        for t in RDFS_D_Axiomatic_Triples:
            self.graph.add(t)

    # noinspection PyBroadException
    def one_time_rules(self):
        """
        Some of the rules in the rule set are axiomatic in nature, meaning that they really have to be added only
        once, there is no reason to add these in a cycle. These are performed by this method that is invoked only once
        at the beginning of the process.

        In this case this is related to a 'hidden' same as rules on literals with identical values (though different
        lexical values).
        """
        # There is also a hidden sameAs rule in RDF Semantics: if a literal appears in a triple, and another one has
        # the same value, then the triple should be duplicated with the other value.
        literals = self._literals()
        items = ((lt1, lt2) for lt1, lt2 in product(literals, literals) if lt1.value == lt2.value)
        for lt1, lt2 in items:
            # In OWL, this line is simply stating a sameAs for the
            # corresponding literals, and then let the usual rules take
            # effect. In RDFS this is not possible, so the sameAs rule is,
            # essentially replicated...
            for (s, p, o) in self.graph.triples((None, None, lt1)):
                self.graph.add((s, p, lt2))

    def rules(self, t, cycle_num):
        """
            Go through the RDFS entailment rules rdf1, rdfs4-rdfs12, by extending the graph.

            :param t: A triple (in the form of a tuple).
            :type t: tuple

            :param cycle_num: Which cycle are we in, starting with 1. Can be used for some (though minor) optimization.
            :type cycle_num: int
        """
        s, p, o = t
        # rdf1
        self.store_triple((p, rdf_type, Property))
        # rdfs4a
        if cycle_num == 1:
            self.store_triple((s, rdf_type, Resource))
        # rdfs4b
        if cycle_num == 1:
            self.store_triple((o, rdf_type, Resource))
        if p == rdfs_domain:
            # rdfs2
            for uuu, Y, yyy in self.graph.triples((None, s, None)):
                self.store_triple((uuu, rdf_type, o))
        if p == rdfs_range:
            # rdfs3
            for uuu, Y, vvv in self.graph.triples((None, s, None)):
                self.store_triple((vvv, rdf_type, o))
        if p == subPropertyOf:
            # rdfs5
            for Z, Y, xxx in self.graph.triples((o, subPropertyOf, None)):
                self.store_triple((s, subPropertyOf, xxx))
            # rdfs7
            for zzz, Z, www in self.graph.triples((None, s, None)):
                self.store_triple((zzz, o, www))
        if p == rdf_type and o == Property:
            # rdfs6
            self.store_triple((s, subPropertyOf, s))
        if p == rdf_type and o == Class:
            # rdfs8
            self.store_triple((s, subClassOf, Resource))
            # rdfs10
            self.store_triple((s, subClassOf, s))
        if p == subClassOf:
            # rdfs9
            for vvv, Y, Z in self.graph.triples((None, rdf_type, s)):
                self.store_triple((vvv, rdf_type, o))
            # rdfs11
            for Z, Y, xxx in self.graph.triples((o, subClassOf, None)):
                self.store_triple((s, subClassOf, xxx))
        if p == rdf_type and o == ContainerMembershipProperty:
            # rdfs12
            self.store_triple((s, subPropertyOf, member))
        if p == rdf_type and o == Datatype:
            self.store_triple((s, subClassOf, Literal))

    def _literals(self):
        """
        Get all literals defined in the graph.
        """
        return set(o for s, p, o in self.graph if isinstance(o, rdflib.Literal))

