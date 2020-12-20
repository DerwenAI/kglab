# -*- coding: utf-8 -*-
#
"""
This module is a brute force implementation of the 'finite' version of `RDFS semantics`_ and of `OWL 2 RL`_ on the top
of RDFLib (with some caveats, see below). Some extensions to these are also implemented.

.. _RDFS semantics: http://www.w3.org/TR/rdf-mt/
.. _OWL 2 RL: http://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules

Brute force means that, in all cases, simple forward chaining rules are used to extend (recursively) the incoming graph
with all triples that the rule sets permit (ie, the "deductive closure" of the graph is computed).
There is an extra options whether the axiomatic triples are added to the graph (prior to the forward chaining step).
These, typically set the domain and range for properties or define some core classes.
In the case of RDFS, the implementation uses a 'finite' version of the axiomatic triples only (as proposed, for example,
by Herman ter Horst). This means that it adds only those :code:`rdf:_i` type predicates that do appear in the original graph,
thereby keeping this step finite. For OWL 2 RL, OWL 2 does not define axiomatic triples formally; but they can be
deduced from the `OWL 2 RDF Based Semantics`_ document and are listed in Appendix 6 (though informally).

.. _OWL 2 RDF Based Semantics: http://www.w3.org/TR/owl2-rdf-based-semantics/

.. note:: This implementation adds only those triples that refer to OWL terms that are meaningful for the OWL 2 RL case.


Package Entry Points
====================

The main entry point to the package is via the :class:`.DeductiveClosure` class. This class should be
initialized to control the parameters of the deductive closure; the forward chaining is done via the
L{expand<DeductiveClosure.expand>} method.
The simplest way to use the package from an RDFLib application is as follows::

    graph = Graph()                                 # creation of an RDFLib graph
    ...
    ...                                             # normal RDFLib application, eg, parsing RDF data
    ...
    DeductiveClosure(OWLRL_Semantics).expand(graph) # calculate an OWL 2 RL deductive closure of graph
                                                    # without axiomatic triples

The first argument of the :class:`.DeductiveClosure` initialization can be replaced by other classes, providing different
types of deductive closure; other arguments are also possible. For example::

 DeductiveClosure(OWLRL_Extension, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)

This will calculate the deductive closure including RDFS and some extensions to OWL 2 RL, and with all possible axiomatic
triples added to the graph (this is about the maximum the package can do…)

The same instance of :class:`.DeductiveClosure` can be used for several graph expansions. In other words, the
expand function does not change any state.

For convenience, a second entry point to the package is provided in the form of a function called
:func:`.convert_graph`, that expects a directory with various options, including a file name. The function
parses the file, creates the expanded graph, and serializes the result into RDF/XML or Turtle. This function is
particularly useful as an entry point for a CGI call (where the HTML form parameters are in a directory) and is easy to
use with a command line interface. The package distribution contains an example for both.

There are major closure type (ie, semantic closure possibilities); these can be controlled through the appropriate
parameters of the :class:`.DeductiveClosure` class:

    * using the :class:`.RDFS_Semantics` class, implementing the `RDFS semantics`_.

    .. _RDFS semantics: http://www.w3.org/TR/rdf-mt/

    * using the :class:`.OWLRL.OWLRL_Semantics` class, implementing the `OWL 2 RL`_.

    .. _OWL 2 RL: http://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules

    * using :class:`.CombinedClosure.RDFS_OWLRL_Semantics` class, implementing a combined semantics of `RDFS semantics`_ and `OWL 2 RL`_.

    .. _RDFS semantics: http://www.w3.org/TR/rdf-mt/
    .. _OWL 2 RL: http://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules

In all three cases there are other dimensions that can control the exact closure being generated:

    * for convenience, the so called axiomatic triples (see, eg, the `axiomatic triples in RDFS`_ are, by default, I{not} added to the graph closure to reduce the number of generated triples. These can be controlled through a separate initialization argument.

    .. _axiomatic triples in RDFS: http://www.w3.org/TR/rdf-mt/#rdfs_interp

    * similarly, the axiomatic triples for D-entailment are separated.

Some Technical/implementation aspects
=====================================

The core processing is done in the in the :class:`.Closure.Core` class, which is subclassed by the
:class:`.RDFSClosure.RDFS_Semantics` and the :class:`.OWLRL.OWLRL_Semantics` classes (these two are then, on their turn,
subclassed by the :class:`.CombinedClosure.RDFS_OWLRL_Semantics` class). The core implements the core functionality of
cycling through the rules, whereas the rules themselves are defined and implemented in the subclasses. There are also
methods that are executed only once either at the beginning or at the end of the full processing cycle. Adding axiomatic
triples is handled separately, which allows a finer user control over these features.

Literals must be handled separately. Indeed, the functionality relies on 'extended' RDF graphs, that allows literals
to be in a subject position, too. Because RDFLib does not allow that, processing begins by exchanging all literals in
the graph for bnodes (identical literals get the same associated bnode). Processing occurs on these bnodes; at the end
of the process all these bnodes are replaced by their corresponding literals if possible (if the bnode occurs in a
subject position, that triple is removed from the resulting graph). Details of this processing is handled in the
separate :class:`.Literals.LiteralProxies` class.

The OWL specification includes references to datatypes that are not in the core RDFS specification, consequently not
directly implemented by RDFLib. These are added in a separate module of the package.


Problems with Literals with datatypes
-------------------------------------

The current distribution of RDFLib is fairly poor in handling datatypes, particularly in checking whether a lexical form
of a literal is "proper" as for its declared datatype. A typical example is::
  "-1234"^^xsd:nonNegativeInteger
which should not be accepted as valid literal. Because the requirements of OWL 2 RL are much stricter in this respect,
an alternative set of datatype handling (essentially, conversions) had to be implemented (see the :py:mod:`.XsdDatatypes`
module).

The :class:`.DeductiveClosure` class has an additional instance variable whether
the default RDFLib conversion routines should be exchanged against the new ones. If this flag is set to True and
instance creation (this is the default), then the conversion routines are set back to the originals once the expansion
is complete, thereby avoiding to influence older application that may not work properly with the new set of conversion
routines.

If the user wants to use these alternative lexical conversions everywhere in the application, then
the :py:meth:`.DeductiveClosure.use_improved_datatypes_conversions` method can be invoked.
That method changes the conversion routines and, from that point on, all usage of :class:`.DeductiveClosure` instances
will use the improved conversion methods without resetting them. Ie, the code structure can be something like::

    DeductiveClosure().use_improved_datatypes_conversions()
    ... RDFLib application
    DeductiveClosure().expand(graph)
    ...

The default situation can be set back using the
:py:meth:`.DeductiveClosure.use_rdflib_datatypes_conversions` call.

It is, however, not *required* to use these methods at all. I.e., the user can use::

    DeductiveClosure(improved_datatypes=False).expand(graph)

which will result in a proper graph expansion except for the datatype specific comparisons which will be incomplete.


**Requires**:
    * `RDFLib`_, 4.0.0 and higher.

    .. _RDFLib: https://github.com/RDFLib/rdflib

    * `rdflib_jsonld`_

    .. _rdflib_jsonld: https://github.com/RDFLib/rdflib-jsonld

**License**: This software is available for use under the `W3C Software License`_

.. _W3C Software License: http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231

**Organization**: `World Wide Web Consortium`_

.. _World Wide Web Consortium: http://www.w3.org

**Author**: `Ivan Herman`_

.. _Ivan Herman: http://www.w3.org/People/Ivan/

"""

# Examples: LangString is disjoint from String
__version__ = '5.2.1'
__author__ = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = 'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

import sys
import io
if sys.version_info < (3, 4, ):
    raise RuntimeError("This version of owl-rl cannot be used in python < 3.4")
# noinspection PyPackageRequirements,PyPackageRequirements,PyPackageRequirements
import rdflib

from rdflib import Literal as rdflibLiteral
# noinspection PyPep8Naming
from rdflib import Graph

from . import DatatypeHandling, Closure
from .OWLRLExtras import OWLRL_Extension, OWLRL_Extension_Trimming
from .OWLRL import OWLRL_Semantics
from .RDFSClosure import RDFS_Semantics
from .CombinedClosure import RDFS_OWLRL_Semantics
from .OWL import imports

################################################################################################################
RDFXML = "xml"
TURTLE = "turtle"
JSON   = "json"
AUTO   = "auto"
RDFA   = "rdfa"

NONE = "none"
RDF  = "rdf"
RDFS = "rdfs"
OWL  = "owl"
FULL = "full"

try:
    from rdflib_jsonld.parser import JsonLDParser
    from rdflib_jsonld.serializer import JsonLDSerializer
    from rdflib.plugin import register, Serializer, Parser
    register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')
    register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')
    json_ld_available = True
except:
    json_ld_available = False


################################################################################################################

# noinspection PyShadowingBuiltins
def __parse_input(iformat, inp, graph):
    """Parse the input into the graph, possibly checking the suffix for the format.

    @param iformat: input format; can be one of L{AUTO}, L{TURTLE}, or L{RDFXML}. L{AUTO} means that the suffix of the
    file name or URI will decide: '.ttl' means Turtle, RDF/XML otherwise.
    @param inp: input file; anything that RDFLib accepts in that position (URI, file name, file object). If '-',
    standard input is used.
    @param graph: the RDFLib Graph instance to parse into.
    """
    if iformat == AUTO:
        if inp == "-":
            format = "turtle"
        else:
            if inp.endswith('.ttl') or inp.endswith('.n3'):
                format = "turtle"
            elif json_ld_available and (inp.endswith('.json') or inp.endswith('.jsonld')):
                format = "json-ld"
            elif inp.endswith('.html'):
                format = "rdfa1.1"
            else:
                format = "xml"
    elif iformat == TURTLE:
        format = "n3"
    elif iformat == RDFA:
        format = "rdfa1.1"
    elif iformat == RDFXML:
        format = "xml"
    elif iformat == JSON:
        if json_ld_available:
            format = "json-ld"
        else:
            raise Exception("JSON-LD parser is not available")
    else:
        raise Exception("Unknown input syntax")

    if inp == "-":
        # standard input is used
        import sys
        source = sys.stdin
    else:
        source = inp
    graph.parse(source, format=format)


def interpret_owl_imports(iformat, graph):
    """
    Interpret the owl import statements. Essentially, recursively merge with all the objects in the owl import
    statement, and remove the corresponding triples from the graph.

    This method can be used by an application prior to expansion. It is *not* done by the the :class:`.DeductiveClosure`
    class.

    :param iformat: Input format; can be one of :code:`AUTO`, :code:`TURTLE`, or :code:`RDFXML`. :code:`AUTO` means that
    the suffix of the file name or URI will decide: '.ttl' means Turtle, RDF/XML otherwise.
    :type iformat: str

    :param graph: The RDFLib Graph instance to parse into.
    :type graph: :class:`RDFLib.Graph`
    """
    while True:
        # 1. collect the import statements:
        all_imports = [t for t in graph.triples((None, imports, None))]
        if len(all_imports) == 0:
            # no import statement whatsoever, we can go on...
            return
        # 2. remove all the import statements from the graph
        for t in all_imports:
            graph.remove(t)
        # 3. get all the imported vocabularies and import them
        for (s, p, uri) in all_imports:
            # this is not 100% kosher. The expected object for an import statement is a URI. However,
            # on local usage, a string would also make sense, so I do that one, too
            if isinstance(uri, rdflibLiteral):
                __parse_input(iformat, str(uri), graph)
            else:
                __parse_input(iformat, uri, graph)
            # 4. start all over again to see if import statements have been imported


def return_closure_class(owl_closure, rdfs_closure, owl_extras, trimming=False):
    """
    Return the right semantic extension class based on three possible choices (this method is here to help potential
    users, the result can be fed into a :class:`DeductiveClosure` instance at initialization).

    :param owl_closure: Whether OWL 2 RL deductive closure should be calculated.
    :type owl_closure: bool

    :param rdfs_closure: Whether RDFS deductive closure should be calculated. In case :code:`owl_closure==True`, this
        parameter should also be used in the initialization of :class:`DeductiveClosure`.
    :type rdfs_closure: bool

    :param owl_extras: Whether the extra possibilities (rational datatype, etc) should be added to an OWL 2 RL
        deductive closure. This parameter has no effect in case :code:`owl_closure==False`.
    :type owl_extras: bool

    :param trimming: Whether extra trimming is done on the OWL RL + Extension output.
    :type trimming: bool

    :return: Deductive class reference or None.
    :rtype: :class:`.DeductiveClosure` or None
    """
    if owl_closure:
        if owl_extras:
            if trimming:
                return OWLRL_Extension_Trimming
            else:
                return OWLRL_Extension
        else:
            if rdfs_closure:
                return RDFS_OWLRL_Semantics
            else:
                return OWLRL_Semantics
    elif rdfs_closure:
        return RDFS_Semantics
    else:
        return None


# noinspection PyCallingNonCallable
class DeductiveClosure:
    """
    Entry point to generate the deductive closure of a graph. The exact choice deductive
    closure is controlled by a class reference. The important initialization parameter is the :code:`closure_class`, a Class
    object referring to a subclass of :class:`.Closure.Core`. Although this package includes a number of such subclasses
    :class:`.OWLRL_Semantics`, :class:`.RDFS_Semantics`, :class:`.RDFS_OWLRL_Semantics`, and :class:`.OWLRL_Extension`, the user can use his/her
    own if additional rules are implemented.

    Note that :code:`owl:imports` statements are *not* interpreted in this class, that has to be done beforehand on the graph
    that is to be expanded.

    :param closure_class: A closure class reference.
    :type closure_class: subclass of :class:`.Closure.Core`

    :param improved_datatypes: Whether the improved set of lexical-to-Python conversions should be used for datatype handling. See the introduction for more details. Default: True.
    :type improved_datatypes: bool

    :param rdfs_closure: Whether the RDFS closure should also be executed. Default: False.
    :type rdfs_closure: bool

    :param axiomatic_triples: Whether relevant axiomatic triples are added before chaining, except for datatype axiomatic triples. Default: False.
    :type axiomatic_triples: bool

    :param datatype_axioms: Whether further datatype axiomatic triples are added to the output. Default: false.
    :type datatype_axioms: bool

    :var improved_datatype_generic: Whether the improved set of lexical-to-Python conversions should be used for datatype handling *in general*, I.e., not only for a particular instance and not only for inference purposes. Default: False.
    :type improved_Datatype_generic: bool
    """

    # This is the original set of param definitions in the class definition
    #
    # @ivar rdfs_closure: Whether the RDFS closure should also be executed. Default: False.
    # @type rdfs_closure: boolean
    # @ivar axiomatic_triples: Whether relevant axiomatic triples are added before chaining, except for datatype axiomatic
    # triples. Default: False.
    # @type axiomatic_triples: boolean
    # @ivar datatype_axioms: Whether further datatype axiomatic triples are added to the output. Default: false.
    # @type datatype_axioms: boolean
    # @ivar closure_class: the class instance used to expand the graph
    # @type closure_class: L{Closure.Core}
    # @cvar improved_datatype_generic: Whether the improved set of lexical-to-Python conversions should be used for
    # datatype handling I{in general}, ie, not only for a particular instance and not only for inference purposes.
    # Default: False.
    # @type improved_datatype_generic: boolean

    improved_datatype_generic = False

    def __init__(self, closure_class, improved_datatypes=True, rdfs_closure=False, axiomatic_triples=False,
                 datatype_axioms=False):
        # This is the original set of param definitions in the __init__
        #
        # @param closure_class: a closure class reference.
        # @type closure_class: subclass of L{Closure.Core}
        # @param rdfs_closure: whether RDFS rules are executed or not
        # @type rdfs_closure: boolean
        # @param axiomatic_triples: Whether relevant axiomatic triples are added before chaining, except for datatype
        # axiomatic triples. Default: False.
        # @type axiomatic_triples: boolean
        # @param datatype_axioms: Whether further datatype axiomatic triples are added to the output. Default: false.
        # @type datatype_axioms: boolean
        # @param improved_datatypes: Whether the improved set of lexical-to-Python conversions should be used for
        # datatype handling. See the introduction for more details. Default: True.
        # @type improved_datatypes: boolean

        if closure_class is None:
            self.closure_class = None
        else:
            if not isinstance(closure_class, type):
                raise ValueError("The closure type argument must be a class reference")
            else:
                self.closure_class = closure_class
        self.axiomatic_triples = axiomatic_triples
        self.datatype_axioms = datatype_axioms
        self.rdfs_closure = rdfs_closure
        self.improved_datatypes = improved_datatypes

    def expand(self, graph):
        """
        Expand the graph using forward chaining, and with the relevant closure type.

        :param graph: The RDF graph.
        :type graph: :class:`rdflib.Graph`
        """
        if (not DeductiveClosure.improved_datatype_generic) and self.improved_datatypes:
            DatatypeHandling.use_Alt_lexical_conversions()

        if self.closure_class is not None:
            self.closure_class(graph, self.axiomatic_triples, self.datatype_axioms, self.rdfs_closure).closure()

        if (not DeductiveClosure.improved_datatype_generic) and self.improved_datatypes:
            DatatypeHandling.use_RDFLib_lexical_conversions()

    @staticmethod
    def use_improved_datatypes_conversions():
        """
        Switch the system to use the improved datatype conversion routines.
        """
        DeductiveClosure.improved_datatype_generic = True
        DatatypeHandling.use_Alt_lexical_conversions()

    @staticmethod
    def use_rdflib_datatypes_conversions():
        """
        Switch the system to use the generic (RDFLib) datatype conversion routines
        """
        DeductiveClosure.improved_datatype_generic = False
        DatatypeHandling.use_RDFLib_lexical_conversions()

###############################################################################################################


# noinspection PyPep8Naming,PyBroadException,PyBroadException,PyBroadException
def convert_graph(options, closureClass=None):
    """
    Entry point for external scripts (CGI or command line) to parse an RDF file(s), possibly execute OWL and/or RDFS
    closures, and serialize back the result in some format.

    Note that this entry point can be used requiring no entailment at all;
    because both the input and the output format for the package can be RDF/XML or Turtle, such usage would
    simply mean a format conversion.

    If OWL 2 RL processing is required, that also means that the :code:`owl:imports` statements are interpreted. I.e.,
    ontologies can be spread over several files. Note, however, that the output of the process would then include all
    imported ontologies, too.

    :param options: Object with specific attributes.
    :type options: object

    :param options.sources: List of uris or file names for the source data; for each one if the name ends with 'ttl', it
        is considered to be turtle, RDF/XML otherwise (this can be overwritten by the options.iformat, though)
    :type options.sources: list

    :param options.text: Direct Turtle encoding of a graph as a text string (useful, eg, for a CGI call using a text
        field).
    :type options.text: str

    :param options.owlClosure: Can be yes or no.
    :type options.owlClosure: bool

    :param options.rdfsClosure: Can be yes or no.
    :type options.rdfsClosure: bool

    :param options.owlExtras: Can be yes or no; whether the extra rules beyond OWL 2 RL are used or not.
    :type options.owlExtras: bool

    :param options.axioms: Whether relevant axiomatic triples are added before chaining (can be a boolean, or the
        strings "yes" or "no").
    :type options.axioms: bool

    :param options.daxioms: Further datatype axiomatic triples are added to the output (can be a boolean, or the strings
        "yes" or "no").
    :type options.daxioms: bool

    :param options.format: Output format, can be "turtle" or "rdfxml".
    :type options.format: str

    :param options.iformat: Input format, can be "turtle", "rdfa", "json", "rdfxml", or "auto". "auto" means that the
        suffix of the file is considered: '.ttl'. '.html', 'json' or '.jsonld' respectively with 'xml' as a fallback.
    :type options.iformat: str

    :param options.trimming: Whether the extension to OWLRL should also include trimming.
    :type options.trimming: bool

    :param closureClass: Explicit class reference. If set, this overrides the various different other options to be
        used as an extension.
    :type closureClass: TODO(edmond.chuc@csiro.au): What class is this supposed to be?
    """

    # Original parameter definitions from old documentation.
    #
    # @param options: object with specific attributes, namely:
    #   - options.sources: list of uris or file names for the source data; for each one if the name ends with 'ttl', it is
    #     considered to be turtle, RDF/XML otherwise (this can be overwritten by the options.iformat, though)
    #   - options.text: direct Turtle encoding of a graph as a text string (useful, eg, for a CGI call using a text field)
    #   - options.owlClosure: can be yes or no
    #   - options.rdfsClosure: can be yes or no
    #   - options.owlExtras: can be yes or no; whether the extra rules beyond OWL 2 RL are used or not.
    #   - options.axioms: whether relevant axiomatic triples are added before chaining (can be a boolean, or the strings
    #     "yes" or "no")
    #   - options.daxioms: further datatype axiomatic triples are added to the output (can be a boolean, or the strings
    #     "yes" or "no")
    #   - options.format: output format, can be "turtle" or "rdfxml"
    #   - options.iformat: input format, can be "turtle", "rdfa", "json", "rdfxml", or "auto". "auto" means that the
    #     suffix of the file is considered: '.ttl'. '.html', 'json' or '.jsonld' respectively with 'xml' as a fallback
    #   - options.trimming: whether the extension to OWLRL should also include trimming
    # @param closureClass: explicit class reference. If set, this overrides the various different other options to be
    #     used as an extension.

    def __check_yes_or_true(opt):
        return opt is True or opt == "yes" or opt == "Yes" or opt == "True" or opt == "true"

    import warnings

    warnings.filterwarnings("ignore")
    if len(options.sources) == 0 and (options.text is None or len(options.text.strip()) == 0):
        raise Exception("No graph specified either via a URI or text")

    graph = Graph()

    # Just to be sure that this attribute does not create issues with older versions of the service...
    # the try statement should be removed, eventually...
    iformat = AUTO
    try:
        iformat = options.iformat
    except:
        # exception can be raised if that attribute is not used at all, true for older versions
        pass

    # similar measure with the possible usage of the 'source' options
    try:
        if options.source is not None:
            options.sources.append(options.source)
    except:
        # exception can be raised if that attribute is not used at all, true for newer versions
        pass

    # Get the sources first. Note that a possible error is filtered out, namely to process the same file twice. This is
    # done by turning the input arguments into a set...
    for inp in set(options.sources):
        __parse_input(iformat, inp, graph)

    # add the possible extra text (ie, the text input on the HTML page)
    if options.text is not None:
        graph.parse(io.StringIO(options.text), format="n3")

    # Get all the options right
    # noinspection PyPep8Naming
    owlClosure = __check_yes_or_true(options.owlClosure)
    # noinspection PyPep8Naming
    rdfsClosure = __check_yes_or_true(options.rdfsClosure)
    # noinspection PyPep8Naming
    owlExtras = __check_yes_or_true(options.owlExtras)
    try:
        trimming = __check_yes_or_true(options.trimming)
    except:
        trimming = False
    axioms = __check_yes_or_true(options.axioms)
    daxioms = __check_yes_or_true(options.daxioms)

    if owlClosure:
        interpret_owl_imports(iformat, graph)

    # adds to the 'beauty' of the output
    graph.bind("owl", "http://www.w3.org/2002/07/owl#")
    graph.bind("xsd", "http://www.w3.org/2001/XMLSchema#")

    # @@@@ some smarter choice should be used later to decide what the closure class is!!! That should
    # also control the import management. Eg, if the superclass includes OWL...
    if closureClass is not None:
        closure_class = closureClass
    else:
        closure_class = return_closure_class(owlClosure, rdfsClosure, owlExtras, trimming)

    DeductiveClosure(closure_class, improved_datatypes=True, rdfs_closure=rdfsClosure, axiomatic_triples=axioms,
                     datatype_axioms=daxioms).expand(graph)

    if options.format == TURTLE:
        return graph.serialize(format="turtle")
    elif options.format == JSON:
        if json_ld_available:
            return graph.serialize(format="json-ld")
        else:
            raise Exception("JSON-LD serializer is not available")
    else:
        return graph.serialize(format="pretty-xml")
