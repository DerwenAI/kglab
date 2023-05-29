
from icecream import ic
import pytest
import rdflib

import kglab

NS_KEYS = [
    "dct",
    "owl",
    "prov",
    "rdf",
    "rdfs",
    "schema",
    "sh",
    "skos",
    "xsd",
]


@pytest.fixture(scope="module")
def kg_test ():
    iri1 = "http://usefulinc.com/ns/doap#"
    prefix1 = "test1"

    kg = kglab.KnowledgeGraph()

    kg.add_ns(
        prefix = prefix1,
        iri = iri1
    )
    
    return kg


@pytest.fixture(scope="module")
def kg_test_data ():
    kg = kglab.KnowledgeGraph(
        namespaces = { "doap": "http://usefulinc.com/ns/doap#" }
    )

    path = "dat/foaf.parquet"

    kg.load_parquet(path)

    return kg


def test_add_ns(kg_test):
    """
Coverage:

* KnowledgeGraph.get_ns_dict()
* KnowledgeGraph.add_ns()
    """
    ns_dict = kg_test.get_ns_dict()
    obs_ns_keys = set(ns_dict.keys())

    exp_ns_keys = set(NS_KEYS + ["test1", "xml"])
    assert exp_ns_keys.issubset(obs_ns_keys)

    iri2  = "http://schema.org/"
    prefix2 = "test2"

    kg_test.add_ns(
        prefix = prefix2,
        iri = iri2
    )

    assert prefix2 in set(kg_test.get_ns_dict().keys())

    namespace = kg_test.get_ns("test2")
    # ic(namespace)

    assert type(namespace) == rdflib.Namespace
    assert namespace == "http://schema.org/"


def test_get_ns_dict (kg_test):
    """
Coverage:

* KnowledgeGraph.get_ns_dict()
    """
    ns_set = set([ "dct", "owl", "prov", "rdf", "rdfs", "sh", "skos", "xsd", "xml" ])
    observed = set(kg_test.get_ns_dict().keys())

    assert len(observed.intersection(ns_set)) == 9
    assert "test1" in kg_test.get_ns_dict().keys()

    for key in NS_KEYS:
        if key != "schema":
            assert key in kg_test.get_ns_dict().keys()
