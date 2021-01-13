#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kglab
import os
import pathlib
import tempfile
import urlpath
import unittest
import warnings


class TestKG (unittest.TestCase):
    def test_load_save_measure (self):
        tmp = tempfile.NamedTemporaryFile(mode="w+b", delete=False)

        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="unclosed file*")

                # load RDF from urlpath.URL
                kg = kglab.KnowledgeGraph()
                path = urlpath.URL("https://storage.googleapis.com/kglab-tutorial/foaf.rdf")
                kg.load_rdf(path, format="xml")
                tmp.close()

                # save RDF to local file reference
                kg.save_rdf(tmp.name)
                tmp.close()

                # load RDF from pathlib.Path
                kg = kglab.KnowledgeGraph()
                path = pathlib.Path(tmp.name)
                kg.load_rdf(path)
                tmp.close()

                # save JSON-LD to local file reference
                kg.save_jsonld(tmp.name)
                tmp.close()

                # load JSON-LD from pathlib.Path
                kg = kglab.KnowledgeGraph()
                path = pathlib.Path(tmp.name)
                kg.load_jsonld(path)

                # measure graph
                measure = kglab.Measure()
                measure.measure_graph(kg)

                # verify
                self.assertTrue(measure.get_node_count() == 35)
        finally:
            os.unlink(tmp.name)
            tmp.close()


    def test_load_parquet_gs (self):
        kg = kglab.KnowledgeGraph(
            namespaces = { "doap": "http://usefulinc.com/ns/doap#" }
            )

        path = "gs://kglab-tutorial/foaf.parquet"
        kg.load_parquet(path)

        sparql = """
            SELECT ?x ?name
            WHERE {
                ?x rdf:type doap:Project .
                ?x doap:name ?name
            }
        """

        for row in kg.query(sparql):
            self.assertTrue(str(row.name) == "Fantasy Fame Game")


if __name__ == "__main__":
    unittest.main()
