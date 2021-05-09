#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import copy
import pyvis  # type: ignore # pylint: disable=E0401
import rdflib.paths  # type: ignore # pylint: disable=E0401
import rdflib.plugins.sparql  # type: ignore # pylint: disable=E0401
import rdflib.term  # type: ignore # pylint: disable=E0401
import typing


class GPViz:
    """
Visualize the basic graph pattern of a SPARQL query.
Modified to limit dependencies to RDFlib and PyVis.

Peb Ruswono Aryan <https://github.com/pebbie>
source from <https://github.com/pebbie/sparqlgpviz>
    """
    _IGNORE_KEYS = [
        "PV",
        "var",
        "_vars",
        "datasetClause",
        "expr",
        "op",
        "A",
        "lazy",
        "service_string",
        "term",
    ]

    # colorcet glasbey_category10 first 16 colors
    # https://colorcet.holoviz.org/user_guide/Categorical.html
    _DEFAULT_COLORS = [
        "#1f77b3",
        "#ff7e0e",
        "#2ba02b",
        "#d62628",
        "#9367bc",
        "#8c564b",
        "#e277c1",
        "#7e7e7e",
        "#bcbc21",
        "#16bdcf",
        "#3a0182",
        "#004201",
        "#0fffa8",
        "#5d003f",
        "#bcbcff",
        "#d8afa1",
    ]


    def __init__ (
        self,
        sparql: str,
        namespaces: typing.Dict[str, str],
        ) -> None:
        """
Constructor for GPViz, built from a SPARQL query and a set of namespaces.

    sparql:
input SPARQL query to be visualized

    namespaces:
the namespaces for the corresponding RDF graph
        """
        self.namespaces: typing.Dict[str, str] = copy.deepcopy(namespaces)
        pq = rdflib.plugins.sparql.prepareQuery(sparql, initNs=self.namespaces)

        for prefix, uri in pq.prologue.namespace_manager.namespaces():
            if prefix not in self.namespaces:
                self.namespaces[prefix] = str(uri)

        self.blank_nodes: typing.List[str] = []
        self.values: typing.Dict[str, list] = collections.defaultdict(list)
        self.triples: list = self._find_triples(pq.algebra)


    def _set_values (
        self,
        alg,
        ) -> None:
        """
        """
        for obj in alg:
            k = list(obj.keys())[0]
            v = obj[k]
            lname = str(k)
            self.values[lname].append(v)


    def _find_triples_node (
        self,
        al: typing.Any,
        key: str,
        result: list,
        ) -> None:
        """
        """
        if key not in self._IGNORE_KEYS:
            if key == "res" and isinstance(al[key], list):
                self._set_values(al[key])
            elif key == "value":
                for var_item in al:
                    var = var_item["var"]
                    self.values[str(var)] = []

                    value = var_item["value"]

                    if isinstance(value, list):
                        for var in al["var"]:
                            tmpval = value.pop(0)
                            self.values[str(var)].append(tmpval)
                    else:
                        self.values[str(var)].append(value)
            elif key == "triples":
                result.extend([ al.triples ])
            else:
                result.extend(self._find_triples(al[key]))


    def _find_triples (
        self,
        alg: typing.Any,
        ) -> list:
        """
    Parse based on name attribute of the current parse tree node (alg)
        """
        result: list = []

        if isinstance(alg, list):
            akg = alg
        else:
            akg = [alg]

        for al in akg:
            for key in dict(al).keys():
                self._find_triples_node(al, key, result)

        return result


    def _get_prefix (
        self,
        uri: rdflib.term.URIRef,
        ) -> typing.Optional[str]:
        """
        """
        for k, v in sorted(self.namespaces.items(), key=lambda x: len(x[1]), reverse=True):
            if uri.startswith(str(v)):
                return k

        return None


    def _get_local_name (
        self,
        uri: rdflib.term.URIRef,
        ) -> str:
        """
        """
        prefix = self._get_prefix(uri)

        if prefix is not None:
            return prefix + ":" + str(uri).replace(self.namespaces[prefix], "")

        return str(uri)


    def _get_label (
        self,
        term: rdflib.term.Identifier,
        ) -> str:
        """
        """
        tname = str(term)

        if isinstance(term, rdflib.term.Variable):
            tname = "?" + tname
        elif isinstance(term, rdflib.term.URIRef):
            tname = self._get_local_name(term)
        elif isinstance(term, rdflib.term.BNode):
            if tname not in self.blank_nodes:
                self.blank_nodes.append(tname)

            tname = "_:bn" + str(self.blank_nodes.index(tname) + 1)
        elif isinstance(term, rdflib.paths.Path):
            if hasattr(term, "arg"):
                aname = self._get_local_name(str(term.arg))
                tname = tname.replace(str(term.arg), aname)
            elif hasattr(term, "args"):
                for arg in term.args:
                    tname = tname.replace(str(arg), self._get_local_name(arg))
            elif hasattr(term, "path"):
                aname = self._get_local_name(str(term.path))
                tname = tname.replace(str(term.path), aname)

            tname = tname[5:-1]

        return tname


    @classmethod
    def _get_node_attr (
        cls,
        term: rdflib.term.Identifier,
        ) -> typing.Dict[str, typing.Any]:
        """
        """
        node_attr: typing.Dict[str, typing.Any] = {
            "shape": "ellipse",
        }

        if isinstance(term, rdflib.term.Variable):
            node_attr["style"] = "dashed"
        elif isinstance(term, rdflib.term.BNode):
            node_attr["style"] = "dotted"
        elif isinstance(term, rdflib.term.Literal):
            node_attr["shape"] = "box"

        if "style" in node_attr:
            if node_attr["style"] == "dashed":
                node_attr["shapeProperties"] = { "borderDashes": [5, 5] }
            elif node_attr["style"] == "dotted":
                node_attr["shapeProperties"] = { "borderDashes": [2, 2] }

        return node_attr


    def _render_triples (
        self,
        pyvis_graph: pyvis.network.Network,
        ) -> None:
        """
        """
        for graph_id, triples in enumerate(self.triples):
            for s, p, o in triples:
                # get term labels
                sname = self._get_label(s)
                pname = self._get_label(p)
                oname = self._get_label(o)

                # customize edge attribute
                edge_args: typing.Dict[str, typing.Any] = {
                    "color": self._DEFAULT_COLORS[graph_id + 1],
                    "label": pname,
                    "arrows": { "to": {"enabled": True} },
                }

                if isinstance(p, rdflib.term.Variable):
                    edge_args["style"] = "dashed"
                    edge_args["dashes"] = [5, 5]

                # customize node attribute
                snode_args = self._get_node_attr(s)
                onode_args = self._get_node_attr(o)

                clr: typing.Dict[str, typing.Any] = {
                    "border": self._DEFAULT_COLORS[graph_id + 1],
                    "background": "white",
                }

                snode_args["color"] = clr
                onode_args["color"] = clr

                # add triple
                pyvis_graph.add_node(sname, **snode_args)
                pyvis_graph.add_node(oname, **onode_args)
                pyvis_graph.add_edge(sname, oname, **edge_args)


    def _render_value_labels (
        self,
        pyvis_graph: pyvis.network.Network,
        ) -> None:
        """
        """
        for var in self.values:
            lname = str(var)
            varname = "?" + lname

            for value in self.values[lname]:
                valname = self._get_label(value)

                edge_args = {
                    "style": "dashed",
                    "dashes": [5, 5],
                    "dir": "none",
                    "arrows": { "to": {"enabled": False} },
                }

                pyvis_graph.add_edge(valname, varname, **edge_args)
                pyvis_graph.nodes[valname]["shape"] = "box"


    def visualize_query (
        self,
        *,
        notebook: bool = False,
        ) -> pyvis.network.Network:
        """
Visualize the query as a PyVis network.

        returns:
PyVis graph to be rendered
        """
        pyvis_graph = pyvis.network.Network(notebook=notebook)

        self._render_triples(pyvis_graph)
        self._render_value_labels(pyvis_graph)

        return pyvis_graph
