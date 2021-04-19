#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for KnowledgeGraph class."""
import sys ; sys.path.insert(0, "../kglab/kglab")

from icecream import ic
import kglab


def test_single_file_load_rdf ():
    """
load rdf from a single file
    """

    # create a KnowledgeGraph object
    kg = kglab.KnowledgeGraph()

    # load RDF from a file
    kg.load_rdf("../dat/gorm.ttl", format="ttl")
    measure = kglab.Measure()

    measure.measure_graph(kg)
    edge_count = measure.get_edge_count()
    node_count = measure.get_node_count()

    assert edge_count == 25
    assert node_count == 15

def test_multiple_file_load_rdf():
    """
load rdf from a multiple files using wildcard expression
    """

    # create a KnowledgeGraph object
    kg = kglab.KnowledgeGraph()

    # load RDF from a file1 into kg
    kg.load_rdf("../dat/gorm.ttl", format="ttl")

    # load RDF from a file2 into kg
    kg.load_rdf("../dat/nom.ttl", format="ttl")

    measure = kglab.Measure()
    measure.measure_graph(kg)
    sequential_edge_count = measure.get_edge_count()
    sequential_node_count = measure.get_node_count()


    kg_multifile = kglab.KnowledgeGraph()

    # load RDF from all files(file1 and file2) matching the expression into kg
    kg_multifile.load_rdf("../dat/*m.ttl", format="ttl")

    measure.reset()
    measure.measure_graph(kg_multifile)
    multifile_edge_count = measure.get_edge_count()
    multifile_node_count = measure.get_node_count()

    # ic(multifile_edge_count)
    # ic(multifile_node_count)
    assert multifile_edge_count == sequential_edge_count
    assert multifile_node_count == sequential_node_count

