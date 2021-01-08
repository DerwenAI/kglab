#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kglab
import urlpath
import unittest


class TestKG (unittest.TestCase):
    def test_measure (self):
        kg = kglab.KnowledgeGraph()
        path = urlpath.URL("https://storage.googleapis.com/kglab-tutorial/foaf.rdf")
        kg.load_rdf(path, format="xml")

        measure = kglab.Measure()
        measure.measure_graph(kg)
        self.assertTrue(measure.node_count == 35)


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
