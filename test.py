#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn import datasets
import kglab
import os
import pandas as pd
import pathlib
import tempfile
import urlpath
import unittest
import warnings


class TestKG (unittest.TestCase):
    def test_load_save_measure (self):
        """
Coverage:

    * KnowledgeGraph() constructor
    * KnowledgeGraph.load_rdf()
    * KnowledgeGraph.safe_rdf()
    * KnowledgeGraph.load_jsonld()
    * KnowledgeGraph.save_jsonld()

    * Measure() constructor
    * Measure.measure_graph()
    * Measure.get_node_count()
        """
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
                self.assertTrue(measure.get_edge_count() == 62)
        finally:
            os.unlink(tmp.name)
            tmp.close()


    def test_load_parquet_gs (self):
        """
Coverage:

    * KnowledgeGraph() constructor
    * KnowledgeGraph.load_parquet()
    * KnowledgeGraph.query_as_df()
    * KnowledgeGraph.query()
    * KnowledgeGraph.n3fy_row()
    * KnowledgeGraph.n3fy()
        """
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

        df = kg.query_as_df(sparql)

        # handle `cuDF` dataframes (GPUs enabled)
        if not isinstance(df, pd.DataFrame):
            df = df.to_pandas()

        row = df.iloc[0]
        val = row["name"]

        self.assertTrue(val == "Fantasy Fame Game")


    def test_approx_pareto_front (self):
        """
Coverage:

    * stripe_column()
    * calc_quantile_bins()
    * root_mean_square()
        """
        # load Iris dataset as a pandas.DataFrame
        iris = datasets.load_iris()
        df1 = pd.DataFrame(iris.data, columns=iris.feature_names)

        # normalize by column
        df2 = df1.apply(lambda x: x/x.max(), axis=0)
        bins = kglab.calc_quantile_bins(len(df2.index))

        # stripe each column to approximate a pareto front
        stripes = [ kglab.stripe_column(values, bins) for _, values in df2.items() ]
        df3 = pd.DataFrame(stripes).T

        # rank based on RMS of striped indices per row
        df1["rank"] = df3.apply(kglab.root_mean_square, axis=1)

        self.assertTrue(round(df1.iloc[0]["rank"], 4) == 8.6747)


if __name__ == "__main__":
    unittest.main()
