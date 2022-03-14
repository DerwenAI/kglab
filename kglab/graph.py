#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Storage plugin for RDFlib

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

from dataclasses import dataclass
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

        self.digest: typing.Optional[ hashes.Hash ] = None
        self.counter: int = 0


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
        context:str,  # pylint: disable=W0613
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
        ic("add", triple)

        s, p, o = triple  # pylint: disable=W0612

        # update digest
        if self.digest:
            self.digest.update(str(s).encode("utf-8"))
            self.digest.update(str(p).encode("utf-8"))
            self.digest.update(str(o).encode("utf-8"))
            self.counter += 1


    def remove (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple_pattern: typing.Tuple,
        *,
        context: str = None,  # pylint: disable=W0613
        ) -> None:
        """
Remove the set of triples matching the pattern from the store.
        """
        ic("remove", triple_pattern)
        s, p, o = triple_pattern  # pylint: disable=W0612


    def triples (  # type: ignore # pylint: disable=R0201,W0221
        self,
        triple_pattern: typing.Tuple,
        *,
        context: str = None,  # pylint: disable=W0613
        ) -> typing.Generator:
        """
A generator over all the triples matching the pattern.

    triple_pattern:
Can include any objects for used for comparing against nodes in the store, for example, REGEXTerm, URIRef, Literal, BNode, Variable, Graph, QuotedGraph, Date? DateRange?

    context:
A conjunctive query can be indicated by either providing a value of None, or a specific context can be queries by passing a Graph instance (if store is context aware).  (currently IGNORED)
        """
        ic("triples", triple_pattern)
        yield (None, None, None,), []

        #for part_act in self._ring.values():
        #    ds = ray.get(part_act.triples.remote(triple_pattern, context=context))  # pylint: disable=E1101

        #    for s, p, o in ds.iter_rows():
        #        triple = (rdflib.URIRef(s), rdflib.URIRef(p), rdflib.URIRef(o),)
        #        yield triple, self.__contexts()


    def __len__ (  # type: ignore # pylint: disable=W0221,W0222
        self,
        *,
        context: str = None,  # pylint: disable=W0613
        ) -> int:
        """
Number of statements in the store. This should only account for
non-quoted (asserted) statements if the context is not specified,
otherwise it should return the number of statements in the formula or
context given.

    context:
a graph instance to query or None
        """
        ic("len", context)
        count = 0

        #for part_act in self._ring.values():
        #    count += ray.get(part_act.count_edges.remote())  # pylint: disable=E1101

        return count


    def __contexts (  # pylint: disable=R0201
        self
        ) -> typing.Iterable:
        """
A no-op.
        """
        # best way to return an empty generator
        l: list = []
        return (c for c in l)


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
