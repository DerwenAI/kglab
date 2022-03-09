import pytest
from icecream import ic

import kglab
from rdflib import Namespace


@pytest.fixture(scope="module")
def kg_test():
    iri1 = "http://usefulinc.com/ns/doap#"
    prefix1 = "test1"

    kg = kglab.KnowledgeGraph()
    kg.add_ns(
        prefix = prefix1,
        iri = iri1
    )
    
    return kg


@pytest.fixture(scope="module")
def kg_test_data():
    kg = kglab.KnowledgeGraph(
        namespaces = { "doap": "http://usefulinc.com/ns/doap#" }
        )

    path = "gs://kglab-tutorial/foaf.parquet"
    kg.load_parquet(path)

    return kg


def test_add_ns(kg_test):
    """
Coverage:

* KnowledgeGraph.get_ns_dict()
* KnowledgeGraph.get_ns
    """
    assert len(kg_test.get_ns_dict()) == 30
    
    iri2  = "http://schema.org/"
    prefix2 = "test2"

    kg_test.add_ns(
        prefix = prefix2,
        iri = iri2
    )
    assert len(kg_test.get_ns_dict()) == 31
    
    namespace = kg_test.get_ns("test2")
    # ic(namespace)

    assert type(namespace) == Namespace
    assert namespace == "http://schema.org/"


def get_ns_dict(kg_test):
    """
Coverage:

* KnowledgeGraph.get_ns_dict()
    """
    assert len(kg_test.get_ns_dict()) == 30

    assert "test1" in kg_test.get_ns_dict().keys()
    for prfx in ("dct", "owl","prov",
      "rdf", "rdfs", "schema", "sh", "skos", "xsd"):
            assert prfx in kg_test.get_ns_dict().keys()
    

def test_describe_ns(kg_test_data):
    """
Coverage:

* KnowledgeGraph.describe_ns()
    """
    df = kg_test_data.describe_ns()

    assert len(df) == 29
    for prfx in kg_test_data._DEFAULT_NAMESPACES:
        assert prfx in list(df["prefix"])
