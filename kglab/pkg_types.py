#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

"""
Shared type definitions.
"""

import pathlib
import typing

import pandas as pd  # type: ignore  # pylint: disable=E0401
import rdflib  # type: ignore  # pylint: disable=E0401
import apeye.url


PathLike = typing.Union[ str, pathlib.Path, apeye.url.URL ]
IOPathLike = typing.Union[ PathLike, typing.IO ]

RDF_Node = typing.Union[ rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode ]
RDF_Triple = typing.Tuple[ RDF_Node, RDF_Node, RDF_Node ]
NodeLike = typing.Union[ typing.Optional[str], RDF_Node ]

ConjunctiveLike = typing.Union[ rdflib.ConjunctiveGraph, rdflib.Dataset ]
GraphLike = typing.Union[ ConjunctiveLike, rdflib.Graph ]

SPARQL_Bindings = typing.Tuple[ str, dict ]

Census_Item = typing.Union[ str, RDF_Node ]
Census_Dyad_Tally = typing.Tuple[ pd.DataFrame, dict ]
