#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

"""
SPARQL query abstractions.
"""

import re
import typing

import pandas as pd  # type: ignore  # pylint: disable=E0401
import pyvis  # type: ignore  # pylint: disable=E0401
import rdflib  # type: ignore  # pylint: disable=E0401

from ..pkg_types import RDF_Node
from ..gpviz import GPViz
from ..util import get_gpu_count

from .base import Queryable


## pre-constructor set-up
if get_gpu_count() > 0:
    import cudf  # type: ignore  # pylint: disable=E0401


class SparqlQueryable (Queryable):
    """
SPARQL implementation for Queryable abstract class.
    """

    def __init__ (
        self,
        kg: typing.Any,
        ) -> None:
        """
Constructor.
        """
        self.kg = kg


    ######################################################################
    ## SPARQL queries

    def query (  # pylint: disable=W0221
        self,
        query: str,
        *,
        bindings: dict = None,
        ) -> typing.Iterable:
        """
Wrapper for [`rdflib.Graph.query()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=query#rdflib.Graph.query) to perform a SPARQL query on the RDF graph.

    query:
text for the SPARQL query

    bindings:
initial variable bindings

    yields:
[`rdflib.query.ResultRow`](https://rdflib.readthedocs.io/en/stable/_modules/rdflib/query.html?highlight=ResultRow#) named tuples, to iterate through the query result set
        """
        if not bindings:
            bindings = {}

        for row in self.kg._g.query(  # pylint: disable=W0212
                query,
                initBindings=bindings,
            ):
            yield row


    def query_as_df (  # pylint: disable=W0221
        self,
        query: str,
        *,
        bindings: dict = None,
        simplify: bool = True,
        pythonify: bool = True,
        ) -> pd.DataFrame:
        """
Wrapper for [`rdflib.Graph.query()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=query#rdflib.Graph.query) to perform a SPARQL query on the RDF graph.

    query:
text for the SPARQL query

    bindings:
initial variable bindings

    simplify:
convert terms in each row of the result set into a readable representation for each term, using N3 format

    pythonify:
convert instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

    returns:
the query result set represented as a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html); uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled
        """
        if not bindings:
            bindings = {}

        row_iter = self.kg._g.query(query, initBindings=bindings)  # pylint: disable=W0212

        if simplify:
            rows_list = [ self.n3fy_row(r.asdict(), pythonify=pythonify) for r in row_iter ]
        else:
            rows_list = [ r.asdict() for r in row_iter ]

        if self.kg.use_gpus:
            df = cudf.DataFrame(rows_list)
        else:
            df = pd.DataFrame(rows_list)

        return df


    def n3fy (
        self,
        node: RDF_Node,
        *,
        pythonify: bool = True,
        ) -> typing.Any:
        """
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize a node into a human-readable representation using N3 format.

    node:
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

    pythonify:
flag to force instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

    returns:
text (or Python objects) for the serialized node
        """
        if pythonify and isinstance(node, rdflib.term.Literal):
            serialized = node.toPython()
        else:
            serialized = node.n3(self.kg._g.namespace_manager)  # type: ignore  # pylint: disable=W0212

        return serialized


    def n3fy_row (
        self,
        row_dict: dict,
        *,
        pythonify: bool = True,
        ) -> dict:
        """
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize one row of a result set from a SPARQL query into a human-readable representation for each term using N3 format.

    row_dict:
one row of a SPARQL query results, as a `dict`

    pythonify:
flag to force instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

    returns:
a dictionary of serialized row bindings
        """
        bindings = {
            k: self.n3fy(v, pythonify=pythonify)
            for k, v in row_dict.items()
        }

        return bindings


    @classmethod
    def unbind_sparql (
        cls,
        query: str,
        bindings: dict,
        *,
        preamble: str = "",
        ) -> str:
        """
Substitute the _binding variables_ into the text of a SPARQL query,
to obviate the need for binding variables specified separately.
This can be helpful for debugging, or for some query engines that
may not have full SPARQL support yet.

    query:
text for the SPARQL query

    bindings:
variable bindings

    returns:
a string of the expanded SPARQL query
        """
        sparql_meta, sparql_body = re.split(r"\s*WHERE\s*\{", query, maxsplit=1)

        for var in sorted(bindings.keys(), key=lambda x: len(x), reverse=True):  # pylint: disable=W0108
            pattern = re.compile(r"(\?" + var + r")(\W)")
            bind_val = "<" + str(bindings[var]) + ">\\2"
            sparql_body = re.sub(pattern, bind_val, sparql_body)

        return "".join([preamble, sparql_meta, " WHERE {", sparql_body]).strip()


    def visualize (
        self,
        query: str,
        *,
        notebook: bool = False,
        ) -> pyvis.network.Network:
        """
Visualize the given SPARQL query as a [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network)

    query:
input SPARQL query to be visualized

    notebook:
optional boolean flag, whether to initialize the PyVis graph to render within a notebook; defaults to `False`

    returns:
PyVis network object, to be rendered
        """
        return GPViz(query, self.kg._ns).visualize_query(notebook=notebook)  # pylint: disable=W0212
