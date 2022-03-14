#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Storage plugin for RDFlib

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

from dataclasses import dataclass
import inspect
import typing

from cryptography.hazmat.primitives import hashes  # type: ignore  # pylint: disable=E0401
from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611
import chocolate  # type: ignore  # pylint: disable=E0401

from rdflib.store import Store  # type: ignore # pylint: disable=E0401
import rdflib  # type: ignore  # pylint: disable=E0401


@dataclass(frozen=True)
class NodeRef:
    """
Represent a reference to a Node within this store.
    """
    id: int
    node_name: str
    node_id: int


class PropertyStore (Store):
    """
A subclass of `rdflib.Store` to use as a plugin, integrating the W3C stack.
    """

    def __init__ (
        self,
        configuration: typing.Optional[str] = None,
        identifier: typing.Optional[str] = None,
        ) -> None:
        """
Instance constructor.
        """
        super().__init__(configuration)
        self.identifier = identifier
        self.__namespace: dict = {}
        self.__prefix: dict = {}

        self._tuples: list = []
        self.digest: typing.Optional[ hashes.Hash ] = None


######################################################################
## rdflib.Store implementation

    @classmethod
    def get_lpg (
        cls,
        graph: rdflib.Graph,
        ) -> "PropertyStore":
        """
An accessor method to extract the PropertyGraph from an RDF graph,
which is a private member of rdflib.Graph.
        """
        return graph._Graph__store  # type: ignore # pylint: disable=W0212


    def add (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple: typing.Tuple,
        context: typing.Optional[ rdflib.term.URIRef ] = None,  # pylint: disable=W0613
        *,
        quoted: bool = False,  # pylint: disable=W0613
        ) -> None:
        """
Adds the given statement to a specific context or to the model.

The quoted argument is interpreted by formula-aware stores to indicate
this statement is quoted/hypothetical.

It should be an error to not specify a context and have the quoted
argument be `True`.

It should also be an error for the quoted argument to be `True` when
the store is not formula-aware.
        """
        s, p, o = triple  # pylint: disable=W0612

        if context is None:
            c = None
        else:
            c = str(context.identifier)  # type: ignore

        _tuple = ( str(s), str(p), str(o), c, )
        self._tuples.append(_tuple)

        # update digest
        if self.digest is not None:
            self.digest.update(inspect.currentframe().f_code.co_name.encode("utf-8"))  # type: ignore
            self.digest.update(str(s).encode("utf-8"))
            self.digest.update(str(p).encode("utf-8"))
            self.digest.update(str(o).encode("utf-8"))

            if c is not None:
                self.digest.update(c.encode("utf-8"))


    def remove (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple_pattern: typing.Tuple,
        *,
        context: typing.Optional[ rdflib.term.URIRef ] = None,  # pylint: disable=W0613
        ) -> None:
        """
Remove the set of triples matching the pattern from the store.
        """
        try:
            s, p, o = triple_pattern  # pylint: disable=W0612

            if context is None:
                c = None
            else:
                c = str(context.identifier)  # type: ignore

            _tuple = ( s, p, o, c, )
            idx = self._tuples.index(_tuple)
            del self._tuples[idx]

            # update digest
            if self.digest is not None:
                self.digest.update(inspect.currentframe().f_code.co_name.encode("utf-8"))  # type: ignore
                self.digest.update(str(s).encode("utf-8"))
                self.digest.update(str(p).encode("utf-8"))
                self.digest.update(str(o).encode("utf-8"))

                if c is not None:
                    self.digest.update(c.encode("utf-8"))
        except ValueError as ex:  # pylint: disable=W0612
            # triple does not exist
            idx = -1


    def triples (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple_pattern: typing.Tuple,
        *,
        context: typing.Optional[ rdflib.term.URIRef ] = None,  # pylint: disable=W0613
        ) -> typing.Generator:
        """
A generator over all the triples matching the pattern.

    triple_pattern:
Can include any objects for used for comparing against nodes in the store, for example, REGEXTerm, URIRef, Literal, BNode, Variable, Graph, QuotedGraph, Date? DateRange?

    context:
A conjunctive query can be indicated by either providing a value of None, or a specific context can be queries by passing a Graph instance (if store is context aware).
        """
        s, p, o = triple_pattern  # pylint: disable=W0612

        if s is not None:
            s = str(s)

        if p is not None:
            p = str(p)

        if o is not None:
            o = str(o)

        if context is None:
            c = None
        else:
            c = str(context.identifier)  # type: ignore

        _tuple = ( s, p, o, c, )

        for src, rel, dst, ctx in self._tuples:
            if (s is None) or (s == src):
                if (p is None) or (p == rel):
                    if (o is None) or (o == dst):
                        if (c is None) or (c == ctx):
                            triple_result = (src, rel, dst,)
                            yield triple_result, self.__contexts()


    def __len__ (  # type: ignore # pylint: disable=W0221,W0222
        self,
        *,
        context: typing.Optional[ rdflib.term.URIRef ] = None,  # pylint: disable=W0613
        ) -> int:
        """
Number of statements in the store. This should only account for
non-quoted (asserted) statements if the context is not specified,
otherwise it should return the number of statements in the formula or
context given.

    context:
a graph instance to query or None
        """
        if context is None:
            return len(self._tuples)

        c = str(context.identifier)  # type: ignore
        count = 0

        for _, _, _, ctx in self._tuples:
            if c == ctx:
                count += 1

        return count


    def __contexts (  # pylint: disable=R0201
        self
        ) -> typing.Iterable:
        """
Returns the set of contexts
        """
        return { ctx for _, _, _, ctx in self._tuples }


    def bind (
        self,
        prefix: str,
        namespace: str,
        ) -> None:
        """
Bar.
        """
        self.__prefix[namespace] = prefix
        self.__namespace[prefix] = namespace


    def namespace (
        self,
        prefix: str,
        ) -> str:
        """
Bar.
        """
        return self.__namespace.get(prefix, None)


    def prefix (
        self,
        namespace: str,
        ) -> str:
        """
Bar.
        """
        return self.__prefix.get(namespace, None)


    def namespaces (
        self
        ) -> typing.Iterable:
        """
Bar.
        """
        for prefix, namespace in self.__namespace.items():
            yield prefix, namespace


    def query (  # pylint: disable=W0235
        self,
        query: str,
        initNs: dict,
        initBindings: dict,
        queryGraph: typing.Any,
        **kwargs: typing.Any,
        ) -> None:
        """
queryGraph is None, a URIRef or '__UNION__'

If None the graph is specified in the query-string/object

If URIRef it specifies the graph to query,

If  '__UNION__' the union of all named graphs should be queried

This is used by ConjunctiveGraphs
Values other than None obviously only makes sense for context-aware stores.)
        """
        super().query(
            query,
            initNs,
            initBindings,
            queryGraph,
            **chocolate.filter_args(kwargs, super().query),
        )


    def update (  # pylint: disable=W0235
        self,
        update: str,
        initNs: dict,
        initBindings: dict,
        queryGraph: typing.Any,
        **kwargs: typing.Any,
        ) -> None:
        """
queryGraph is None, a URIRef or '__UNION__'

If None the graph is specified in the query-string/object

If URIRef it specifies the graph to query,

If  '__UNION__' the union of all named graphs should be queried

This is used by ConjunctiveGraphs
Values other than None obviously only makes sense for context-aware stores.)
        """
        super().update(
            update,
            initNs,
            initBindings,
            queryGraph,
            **chocolate.filter_args(kwargs, super().update),
        )
