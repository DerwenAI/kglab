#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## shared type definitions

import pandas as pd  # type: ignore
import pathlib
import rdflib  # type: ignore
import typing

PathLike = typing.Union[str, pathlib.Path]

RDF_Node = typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
RDF_Triple = typing.Tuple[RDF_Node, RDF_Node, RDF_Node]
NodeLike = typing.Union[typing.Optional[str], RDF_Node]

ConjunctiveLike = typing.Union[rdflib.ConjunctiveGraph, rdflib.Dataset]
GraphLike = typing.Union[ConjunctiveLike, rdflib.Graph]

SPARQL_Bindings = typing.Tuple[str, dict]

Census_Item = typing.Union[str, RDF_Node]
Census_Dyad_Tally = typing.Tuple[pd.DataFrame, dict]
