# -*- coding: utf-8 -*-
#
"""
The generic superclasses for various rule based semantics and the possible extensions.

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
from rdflib import BNode
from rdflib import Literal as rdflibLiteral
from rdflib import Namespace

# noinspection PyPep8Naming
from owlrl.RDFS import RDFNS as ns_rdf
from owlrl.RDFS import rdf_type

debugGlobal = False
offlineGeneration = False


######################################################################################################
# noinspection PyMethodMayBeStatic,PyPep8Naming,PyPep8Naming
class Core:
    """
    Core of the semantics management, dealing with the RDFS and other Semantic triples. The only
    reason to have it in a separate class is for an easier maintainability.

    This is a common superclass only. In the present module, it is subclassed by
    a :class:`.RDFSClosure.RDFS_Semantics` class and a :class:`.OWLRL.OWLRL_Semantics` classes.
    There are some methods that are implemented in the subclasses only, ie, this class cannot be used by itself!

    :param graph: The RDF graph to be extended.
    :type graph: :class:`rdflib.Graph`

    :param axioms: Whether axioms should be added or not.
    :type axioms: bool

    :param daxioms: Whether datatype axioms should be added or not.
    :type daxioms: bool

    :param rdfs: Whether RDFS inference is also done (used in subclassed only).
    :type rdfs: bool

    :var IMaxNum: Maximal index of :code:`rdf:_i` occurrence in the graph.
    :type IMaxNum: int

    :var graph: The real graph.
    :type graph: :class:`rdflib.Graph`

    :var axioms: Whether axioms should be added or not.
    :type axioms: bool

    :var daxioms: Whether datatype axioms should be added or not.
    :type daxioms: bool

    :var added_triples: Triples added to the graph, conceptually, during one processing cycle.
    :type added_triples: set of triples

    :var error_messages: Error messages (typically inconsistency messages in OWL RL) found during processing. These
        are added to the final graph at the very end as separate BNodes with error messages.
    :type error_messages: list of str

    :var rdfs: Whether RDFS inference is also done (used in subclassed only).
    :type rdfs: bool
    """
    # noinspection PyUnusedLocal
    def __init__(self, graph, axioms, daxioms, rdfs=False):
        """
        The parameter descriptions here are from the old documentation.

        @param graph: the RDF graph to be extended
        @type graph: rdflib.Graph
        @param axioms: whether axioms should be added or not
        @type axioms: boolean
        @param daxioms: whether datatype axioms should be added or not
        @type daxioms: boolean
        @param rdfs: whether RDFS inference is also done (used in subclassed only)
        @type rdfs: boolean
        """
        self._debug = debugGlobal

        # Calculate the maximum 'n' value for the '_i' type predicates (see Horst's paper)
        n = 1
        maxnum = 0
        cont = True
        while cont:
            cont = False
            predicate = ns_rdf[("_%d" % n)]
            for (s, p, o) in graph.triples((None, predicate, None)):
                # there is at least one if we got here
                maxnum = n
                n += 1
                cont = True
        self.IMaxNum = maxnum

        self.graph = graph
        self.axioms = axioms
        self.daxioms = daxioms
        
        self.rdfs = rdfs

        self.error_messages = []
        self.empty_stored_triples()

    def add_error(self, message):
        """
        Add an error message

        :param message: Error message.
        :type message: str
        """
        if message not in self.error_messages:
            self.error_messages.append(message)

    def pre_process(self):
        """
        Do some pre-processing step. This method before anything else in the closure. By default, this method is empty,
        subclasses can add content to it by overriding it.
        """
        pass

    def post_process(self):
        """
        Do some post-processing step. This method when all processing is done, but before handling possible
        errors (ie, the method can add its own error messages). By default, this method is empty, subclasses
        can add content to it by overriding it.
        """
        pass

    def rules(self, t, cycle_num):
        """
        The core processing cycles through every tuple in the graph and dispatches it to the various methods
        implementing a specific group of rules. By default, this method raises an exception; indeed, subclasses
        *must* add content to by overriding it.

        :param t: One triple on which to apply the rules.
        :type t: tuple

        :param cycle_num: Which cycle are we in, starting with 1. This value is forwarded to all local rules; it is
            also used locally to collect the bnodes in the graph.
        :type cycle_num: int
        """
        raise Exception("This method should not be called directly; subclasses should override it")

    def add_axioms(self):
        """
        Add axioms.

        This is only a placeholder and raises an exception by default; subclasses *must* fill this with real content
        """
        raise Exception("This method should not be called directly; subclasses should override it")

    def add_d_axioms(self):
        """
        Add d axioms.

        This is only a placeholder and raises an exception by default; subclasses I{must} fill this with real content
        """
        raise Exception("This method should not be called directly; subclasses should override it")

    def one_time_rules(self):
        """
        This is only a placeholder; subclasses should fill this with real content. By default, it is just an empty call.
        This set of rules is invoked only once and not in a cycle.
        """
        pass

    # noinspection PyAttributeOutsideInit
    def empty_stored_triples(self):
        """
        Empty the internal store for triples.
        """
        self.added_triples = set()
        
    def flush_stored_triples(self):
        """
        Send the stored triples to the graph, and empty the container.
        """
        for t in self.added_triples:
            self.graph.add(t)
        self.empty_stored_triples()

    def store_triple(self, t):
        """
        In contrast to its name, this does not yet add anything to the graph itself, it just stores the tuple in an
        internal set (:code:`Core.added_triples`). (It is important for this to be a set: some of the rules in the various
        closures may generate the same tuples several times.) Before adding the tuple to the set, the method checks
        whether the tuple is in the final graph already (if yes, it is not added to the set).

        The set itself is emptied at the start of every processing cycle; the triples are then effectively added to the
        graph at the end of such a cycle. If the set is actually empty at that point, this means that the cycle has not
        added any new triple, and the full processing can stop.

        :param t: The triple to be added to the graph, unless it is already there
        :type t: tuple (s,p,o)
        """
        (s, p, o) = t
        if not isinstance(p, rdflibLiteral) and t not in self.graph:
            if self._debug or offlineGeneration:
                print(t)
            self.added_triples.add(t)

    # noinspection PyAttributeOutsideInit
    def closure(self):
        """
        Generate the closure the graph. This is the real 'core'.

        The processing rules store new triples via the separate method :func:`.Core.store_triple` which stores
        them in the :code:`added_triples` array. If that array is empty at the end of a cycle,
        it means that the whole process can be stopped.

        If required, the relevant axiomatic triples are added to the graph before processing in cycles. Similarly
        the exchange of literals against bnodes is also done in this step (and restored after all cycles are over).
        """
        self.pre_process()

        # Handling the axiomatic triples. In general, this means adding all tuples in the list that
        # forwarded, and those include RDF or RDFS. In both cases the relevant parts of the container axioms should also
        # be added.
        if self.axioms:
            self.add_axioms()

        # Add the datatype axioms, if needed (note that this makes use of the literal proxies, the order of the call
        # is important!
        if self.daxioms:
            self.add_d_axioms()

        self.flush_stored_triples()

        # Get first the 'one-time rules', ie, those that do not need an extra round in cycles down the line
        self.one_time_rules()
        self.flush_stored_triples()

        # Go cyclically through all rules until no change happens
        new_cycle = True
        cycle_num = 0
        while new_cycle:
            # yes, there was a change, let us go again
            cycle_num += 1

            # DEBUG: print the cycle number out
            if self._debug:
                print("----- Cycle #:%d" % cycle_num)

            # go through all rules, and collect the replies (to see whether any change has been done)
            # the new triples to be added are collected separately not to interfere with
            # the current graph yet
            self.empty_stored_triples()

            # Execute all the rules; these might fill up the added triples array
            for t in self.graph:
                self.rules(t, cycle_num)

            # Add the tuples to the graph (if necessary, that is). If any new triple has been generated, a new cycle
            # will be necessary...
            new_cycle = len(self.added_triples) > 0

            for t in self.added_triples:
                self.graph.add(t)

        self.post_process()
        self.flush_stored_triples()

        # Add possible error messages
        if self.error_messages:
            # I am not sure this is the right vocabulary to use for this purpose, but I haven't found anything!
            # I could, of course, come up with my own, but I am not sure that would be kosher...
            ERRNS = Namespace("http://www.daml.org/2002/03/agents/agent-ont#")
            self.graph.bind("err","http://www.daml.org/2002/03/agents/agent-ont#")
            for m in self.error_messages:
                message = BNode()
                self.graph.add((message, rdf_type, ERRNS['ErrorMessage']))
                self.graph.add((message, ERRNS['error'], rdflibLiteral(m)))
