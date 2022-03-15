import pytest
import responses

import kglab

from .__init__ import DAT_FILES_DIR


@pytest.fixture()
def kg_test_data():
    namespaces = {
    "nom":  "http://example.org/#",
    "wtm":  "http://purl.org/heals/food/",
    "ind":  "http://purl.org/heals/ingredient/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    }

    kg = kglab.KnowledgeGraph(
        name = "A recipe KG example based on Food.com",
        base_uri = "https://www.food.com/recipe/",
        namespaces = namespaces,
        )
    
    yield kg
    
    del kg

#
# standard query
#
QUERY = """
SELECT (COUNT(*) as ?Triples) WHERE { ?s ?p ?o}
"""

def test_load_rdf(kg_test_data):
    kg_test_data.load_rdf(DAT_FILES_DIR / "tmp.ttl")
    
    df = kg_test_data.query_as_df(QUERY)
    assert df.values[0][0] == 1891
    
    measure = kglab.Measure()
    measure.measure_graph(kg_test_data)

    assert measure.get_node_count() == 286
    assert measure.get_edge_count() == 1891
    
    #assert False, "Node and edges count is different from load_jsonld"


def test_load_jsonld(kg_test_data):
    kg_test_data.load_jsonld(DAT_FILES_DIR / "tmp.jsonld")

    df = kg_test_data.query_as_df(QUERY)
    assert df.values[0][0] == 1798

    measure = kglab.Measure()
    measure.measure_graph(kg_test_data)

    assert measure.get_node_count() == 257
    assert measure.get_edge_count() == 1798

    #assert False, "Node and edges count is different from load_rdf"


def test_load_parquet(kg_test_data):
    kg_test_data.load_parquet(DAT_FILES_DIR / "tmp.parquet")

    df = kg_test_data.query_as_df(QUERY)
    assert df.values[0][0] == 1798

    measure = kglab.Measure()
    measure.measure_graph(kg_test_data)

    assert measure.get_node_count() == 257
    assert measure.get_edge_count() == 1798


@pytest.mark.skip(reason="the library used for CSV conversion does not use https and requires multiple requests")
@responses.activate
def test_load_csv(kg_test_data):
    import pandas as pd

    local_path = DAT_FILES_DIR / "tree-ops.csv"
    remote_path = "http://w3c.github.io/csvw/tests/tree-ops.csv"
    
    with open(local_path, "rb") as f:
        responses.add(
            responses.HEAD,
            remote_path,
            status=200,
            stream=True,
        )
        responses.add(
            responses.GET,
            "http://w3c.github.io/.well-known/csvm",
            status=404,
            stream=True,
        )
        responses.add(
            responses.GET,
            "http://w3c.github.io/csvw/tests/tree-ops.csv-metadata.json",
            status=404,
            stream=True,
        )
        responses.add(
            responses.GET,
            "http://w3c.github.io/csvw/tests/csv-metadata.json",
            status=404,
            stream=True,
        )
        responses.add(
            responses.GET,
            remote_path,
            body=f,
            status=200,
            content_type="text/csv",
            stream=True,
        )

        kg_test_data.load_csv(remote_path)
        df = pd.read_csv(local_path)
        
        print(len(df.values))
        
        query_df = kg_test_data.query_as_df(QUERY)
        # assert

        measure = kglab.Measure()
        measure.measure_graph(kg_test_data)

        # assert
        assert measure.get_edge_count() == query_df.values[0][0]


def test_import_roam(kg_test_data):
    """
Coverage:

* KnowledgeGraph.import_roam() import JSON from Roam Research export
    """
    import warnings

    # create a KnowledgeGraph object
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="unclosed file*")

        # load JSON export into KG
        path = DAT_FILES_DIR / "roam.json"
        kg_test_data.import_roam(path)

        measure = kglab.Measure()
        measure.measure_graph(kg_test_data)

        node_count =  measure.get_node_count()
        edge_count =  measure.get_edge_count()

        # ic(node_count)
        # ic(edge_count)
        assert node_count == 46
        assert edge_count == 217