#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kglab
import urlpath
import unittest


class TestKG (unittest.TestCase):
    def setUp (self):
        """load an example KG"""
        self.kg = kglab.KnowledgeGraph()

        path = urlpath.URL("http://bigasterisk.com/foaf.rdf")
        self.kg.load_rdf(path, format="xml")


    def test_measure (self):
        measure = kglab.Measure()
        measure.measure_graph(self.kg)
        self.assertTrue(measure.node_count == 35)


if __name__ == "__main__":
    unittest.main()
