import os
import pathlib
import tempfile
import warnings

from sklearn import datasets
import pandas as pd
import urlpath

import kglab


def test_load_save_measure():
    """
Coverage:

* KnowledgeGraph() constructor
* KnowledgeGraph.load_rdf() from pathlib.Path, urlpath.URL
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
            assert measure.get_node_count() == 35
            assert measure.get_edge_count() == 62
    finally:
        os.unlink(tmp.name)
        tmp.close()


def test_load_parquet_gs():
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

    assert val == "Fantasy Fame Game"


def test_approx_pareto_front():
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

    assert round(df1.iloc[0]["rank"], 4) == 8.6747


def test_single_file_load_rdf():
    """
Coverage:

* KnowledgeGraph.load_rdf() load RDF from a single local file (str)
    """
    # create a KnowledgeGraph object
    kg = kglab.KnowledgeGraph()

    # load RDF from a file
    kg.load_rdf("dat/gorm.ttl", format="ttl")
    measure = kglab.Measure()

    measure.measure_graph(kg)
    edge_count = measure.get_edge_count()
    node_count = measure.get_node_count()

    assert edge_count == 25
    assert node_count == 15


def test_multiple_file_load_rdf():
    """
Coverage:

* KnowledgeGraph.load_rdf() load RDF from multiple files using a wildcard expression
    """
    # create a KnowledgeGraph object
    kg = kglab.KnowledgeGraph()

    # load RDF from a file1 into KG
    kg.load_rdf("dat/gorm.ttl", format="ttl")

    # load RDF from a file2 into KG
    kg.load_rdf("dat/nom.ttl", format="ttl")

    measure = kglab.Measure()
    measure.measure_graph(kg)
    sequential_edge_count = measure.get_edge_count()
    sequential_node_count = measure.get_node_count()

    # load RDF from all files (file1 and file2) matching the
    # expression into KG
    kg_multifile = kglab.KnowledgeGraph()
    kg_multifile.load_rdf("dat/*m.ttl", format="ttl")

    measure.reset()
    measure.measure_graph(kg_multifile)
    multifile_edge_count = measure.get_edge_count()
    multifile_node_count = measure.get_node_count()

    # ic(multifile_edge_count)
    # ic(multifile_node_count)
    assert multifile_edge_count == sequential_edge_count
    assert multifile_node_count == sequential_node_count


def test_multiple_file_load_jsonld():
    """
Coverage:

* KnowledgeGraph.load_jsonld() load jsonld from multiple files using a wildcard expression
    """
    # create a KnowledgeGraph object
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="unclosed file*")
        kg = kglab.KnowledgeGraph()

        # load json-ld from a file1 into KG
        kg.load_jsonld("dat/gorm.jsonld")

        # load json-ld from a file2 into KG
        kg.load_jsonld("dat/nom.jsonld")

        measure = kglab.Measure()
        measure.measure_graph(kg)
        sequential_edge_count = measure.get_edge_count()
        sequential_node_count = measure.get_node_count()
        # ic(sequential_edge_count)
        # ic(sequential_node_count)

        # load jsonld from all files (file1 and file2) matching the
        # expression into KG
        kg_multifile = kglab.KnowledgeGraph()
        kg_multifile.load_jsonld("dat/*m.jsonld")

        measure.reset()
        measure.measure_graph(kg_multifile)
        multifile_edge_count = measure.get_edge_count()
        multifile_node_count = measure.get_node_count()

        # ic(multifile_edge_count)
        # ic(multifile_node_count)
        assert multifile_edge_count == sequential_edge_count
        assert multifile_node_count == sequential_node_count


def test_multiple_file_load_parquet():
    """
Coverage:

* KnowledgeGraph.load_parquet() load jsonld from multiple files using a wildcard expression
    """
    # create a KnowledgeGraph object
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="unclosed file*")
        kg = kglab.KnowledgeGraph()

        # load parquet from a file1 into KG
        kg.load_parquet("dat/gorm.parquet")

        # load parquet from a file2 into KG
        kg.load_parquet("dat/nom.parquet")

        measure = kglab.Measure()
        measure.measure_graph(kg)
        sequential_edge_count = measure.get_edge_count()
        sequential_node_count = measure.get_node_count()
        # ic(sequential_edge_count)
        # ic(sequential_node_count)

        # load parquet from all files (file1 and file2) matching the
        # expression into KG
        kg_multifile = kglab.KnowledgeGraph()
        kg_multifile.load_parquet("dat/*m.parquet")

        measure.reset()
        measure.measure_graph(kg_multifile)
        multifile_edge_count = measure.get_edge_count()
        multifile_node_count = measure.get_node_count()

        # ic(multifile_edge_count)
        # ic(multifile_node_count)
        assert multifile_edge_count == sequential_edge_count
        assert multifile_node_count == sequential_node_count
