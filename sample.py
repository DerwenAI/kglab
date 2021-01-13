#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kglab

# create a KnowledgeGraph object
kg = kglab.KnowledgeGraph()

# load RDF from a URL
kg.load_rdf("https://storage.googleapis.com/kglab-tutorial/foaf.rdf", format="xml")

# measure the graph
measure = kglab.Measure()
measure.measure_graph(kg)

print("edges: {}\n".format(measure.get_edge_count()))
print("nodes: {}\n".format(measure.get_node_count()))

# serialize as a string in "Turtle" TTL format
ttl = kg.save_rdf_text()
print("```")
print(ttl[:999])
print("```")
