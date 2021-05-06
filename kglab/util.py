#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

######################################################################
## utilities

import pyvis.network  # type: ignore # pylint: disable=E0401
import rdflib
from rdflib.paths import Path    # type: ignore # pylint: disable=E0401
from rdflib.plugins.sparql import prepareQuery # type: ignore # pylint: disable=E0401
from rdflib.term import Identifier, Variable, URIRef, BNode, Literal # type: ignore # pylint: disable=E0401
from rdflib import Namespace, XSD, RDF, RDFS, OWL # type: ignore # pylint: disable=E0401
import math
import numpy as np  # type: ignore  # pylint: disable=E0401
import pandas as pd  # type: ignore  # pylint: disable=E0401


def get_gpu_count () -> int:
    """
Special handling for detecting GPU availability: an approach
recommended by the NVidia RAPIDS engineering team, since `nvml`
bindings are difficult for Python libraries to keep updated.

    returns:
count of available GPUs
    """
    try:
        import pynvml  # type: ignore  # pylint: disable=E0401
        pynvml.nvmlInit()

        gpu_count = pynvml.nvmlDeviceGetCount()
    except Exception: # pylint: disable=W0703
        gpu_count = 0

    return gpu_count


if get_gpu_count() > 0:
    import cudf  # type: ignore # pylint: disable=E0401



def calc_quantile_bins (
    num_rows: int
) -> np.ndarray:
    """
Calculate the bins to use for a quantile stripe, using [`numpy.linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)

    num_rows:
number of rows in the target dataframe

    returns:
the calculated bins, as a [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
    """
    granularity = max(round(math.log(num_rows) * 4), 1)
    return np.linspace(0, 1, num=granularity, endpoint=True)


def stripe_column (
    values: list,
    bins: int,
    *,
    use_gpus: bool = False,
) -> np.ndarray:
    """
Stripe a column in a dataframe, by interpolating quantiles into a set of discrete indexes.

    values:
list of values to stripe

    bins:
quantile bins; see [`calc_quantile_bins()`](#calc_quantile_bins-function)

    use_gpus:
optionally, use the NVidia GPU devices with the [RAPIDS libraries](https://rapids.ai/) if these libraries have been installed and the devices are available; defaults to `False`

    returns:
the striped column values, as a [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html); uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled
    """
    if use_gpus:
        s = cudf.Series(values)
    else:
        s = pd.Series(values)

    q = s.quantile(bins, interpolation="nearest")

    try:
        stripe = np.digitize(values, q) - 1
        return stripe
    except ValueError as e:
        # should never happen?
        print("ValueError:", str(e), values, s, q, bins)
        raise


def root_mean_square (
    values: list
) -> float:
    """
Calculate the [*root mean square*](https://mathworld.wolfram.com/Root-Mean-Square.html) of the values in the given list.

    values:
list of values to use in the RMS calculation

    returns:
RMS metric as a float
    """
    s = sum(map(lambda x: float(x)**2.0, values))
    n = float(len(values))
    return math.sqrt(s / n)


######################################################################
# taken from https://github.com/pebbie/sparqlgpviz
# visualize basic graph pattern of a sparql query
# modified to only use rdflib and pyvis
# by : Peb Ruswono Aryan (https://github.com/pebbie)

_BLANKNODES = []
defaultNS = {"rdf": str(RDF), "rdfs": str(
    RDFS), "owl": str(OWL), "xsd": str(XSD)}
# colorcet glasbey_category10 first 16 colors https://colorcet.holoviz.org/user_guide/Categorical.html
defaultColors = ['#1f77b3', '#ff7e0e', '#2ba02b', '#d62628', '#9367bc', '#8c564b', '#e277c1',
                 '#7e7e7e', '#bcbc21', '#16bdcf', '#3a0182', '#004201', '#0fffa8', '#5d003f', '#bcbcff', '#d8afa1']


def _gpviz_get_values (
        alg, 
        vals
    ):
    for obj in alg:
        k = list(obj.keys())[0]
        v = obj[k]
        lname = str(k)
        if lname in vals:
            vals[lname].append(v)
        else:
            vals[lname] = [v]


def _gpviz_find_triples (
        alg, 
        vals
    ):
    # parse based on name attribute of the current parse tree node (alg)
    result = []
    if isinstance(alg, list):
        akg = alg
    else:
        akg = [alg]

    for al in akg:
        if hasattr(al, 'name'):
            pass
        ak = dict(al).keys()
        for key in ak:
            if key in ['PV', 'var', '_vars', 'datasetClause', 'expr', 'op', 'A', 'lazy', 'service_string']:
                continue
            elif key == 'res' and isinstance(al[key], list):
                # values()
                _gpviz_get_values(al[key], vals)
                continue
            elif key == 'value':
                for var in al['var']:
                    vals[str(var)] = []
                for value in al[key]:
                    if isinstance(value, list):
                        for var in al['var']:
                            tmpval = value.pop(0)
                            vals[str(var)].append(tmpval)
                    else:
                        vals[str(var)].append(value)
                continue
            elif key == 'term':
                continue
            elif key == 'triples':
                result += [al.triples]
                continue

            result += _gpviz_find_triples(al[key], vals)
    return result


def _gpviz_get_prefix(
        namespaces : dict, 
        uri : rdflib.term.URIRef
    ) -> str:
    for k, v in sorted(namespaces.items(), key=lambda x: len(x[1]), reverse=True):
        if uri.startswith(str(v)):
            return k
    return None


def _gpviz_get_local_name(
        namespaces : dict, 
        uri : rdflib.term.URIRef
    ) -> str:
    pref = _gpviz_get_prefix(namespaces, uri)
    return pref+':'+str(uri).replace(namespaces[pref], '') if pref is not None else str(uri)


def _gpviz_get_label(
        namespaces : dict, 
        term : rdflib.term.Identifier
    ) -> str:
    tname = str(term)
    if isinstance(term, Variable):
        tname = '?' + tname
    elif isinstance(term, URIRef):
        tname = _gpviz_get_local_name(namespaces, term)
    elif isinstance(term, BNode):
        if tname not in _BLANKNODES:
            _BLANKNODES.append(tname)
        tname = '_:bn' + str(_BLANKNODES.index(tname)+1)
    elif isinstance(term, Path):
        # print(term.n3())
        if hasattr(term, 'arg'):
            aname = _gpviz_get_local_name(namespaces, str(term.arg))
            tname = tname.replace(str(term.arg), aname)
        elif hasattr(term, 'args'):
            for arg in term.args:
                tname = tname.replace(str(arg), _gpviz_get_local_name(namespaces, arg))
        elif hasattr(term, 'path'):
            aname = _gpviz_get_local_name(namespaces, str(term.path))
            tname = tname.replace(str(term.path), aname)
        tname = tname[5:-1]
    return tname


def build_pyvis_sparql(
        sparql : str, 
        namespaces : dict = dict(defaultNS), 
        notebook: bool = False
    ) -> pyvis.network.Network:
    def _get_node_attr(term, termlabel):
        n = {}
        n['shape'] = 'ellipse'
        if isinstance(term, Variable):
            n['style'] = 'dashed'
        elif isinstance(term, BNode):
            n['style'] = 'dotted'
        elif isinstance(term, Literal):
            n['shape'] = 'box'
        if 'style' in n:
            if n['style'] == 'dashed':
                n['shapeProperties'] = {'borderDashes': [5, 5]}
            elif n['style'] == 'dotted':
                n['shapeProperties'] = {'borderDashes': [2, 2]}

        return n

    pq = prepareQuery(
        sparql, initNs=namespaces)

    for prefix, nsURI in [n for n in pq.prologue.namespace_manager.namespaces()]:
        if prefix not in namespaces:
            namespaces[prefix] = str(nsURI)

    G = pyvis.network.Network(notebook=notebook)

    values = {}
    tris = _gpviz_find_triples(pq.algebra, values)

    if tris is not None:
        for gid, trisgrp in enumerate(tris):
            for s, p, o in trisgrp:
                # get term labels
                sname = _gpviz_get_label(namespaces, s)
                pname = _gpviz_get_label(namespaces, p)
                oname = _gpviz_get_label(namespaces, o)

                # customize edge attribute
                edge_args = {}
                edge_args['color'] = defaultColors[gid+1]
                edge_args['label'] = pname
                edge_args['arrows'] = {'to': {'enabled': True}}

                if isinstance(p, Variable):
                    edge_args['style'] = 'dashed'
                    edge_args['dashes'] = [5, 5]

                # customize node attribute
                snode_args = _get_node_attr(s, sname)
                onode_args = _get_node_attr(o, oname)

                clr = {'border': defaultColors[gid+1], 'background': 'white'}

                snode_args['color'] = clr
                onode_args['color'] = clr

                # add triple
                G.add_node(sname, **snode_args)
                G.add_node(oname, **onode_args)
                G.add_edge(sname, oname, **edge_args)

    if len(values.keys()) > 0:
        for var in values:
            lname = str(var)
            varname = '?' + lname
            for value in values[lname]:
                valname = _gpviz_get_label(namespaces, value)

                edge_args = {}
                edge_args['style'] = 'dashed'
                edge_args['dashes'] = [5, 5]
                edge_args['dir'] = 'none'
                edge_args['arrows'] = {'to': {'enabled': False}}

                G.add_edge(valname, varname, **edge_args)

                G.nodes[valname]['shape'] = 'box'

    return G
