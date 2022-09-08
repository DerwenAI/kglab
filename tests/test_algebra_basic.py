import pytest
import numpy as np

import kglab
from kglab.subg import SubgraphMatrix

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
    
    kg.load_rdf(DAT_FILES_DIR / "tmp.ttl")
    
    yield kg
    
    del kg


def get_items(s):
    s_coo = s.tocoo()
    return set(zip(s_coo.row, s_coo.col))


QUERY1 = """
SELECT ?subject ?object
WHERE {
    ?subject rdf:type wtm:Recipe .
    ?subject wtm:hasIngredient ?object .
}
"""

def test_adj_mtx(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    n_array = subgraph.to_adjacency()
    np.testing.assert_allclose(
        n_array[:3,:6],
        np.array(
            [[0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
        ),
        rtol=1e-5, atol=0
    )


def test_incidence(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    n_array = subgraph.to_incidence()
    np.testing.assert_allclose(
        n_array[:3,:6],
        np.array(
            [[1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0]]
        ),
        rtol=1e-5, atol=0
    )

def test_laplacian(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    n_array = subgraph.to_laplacian()
    np.testing.assert_allclose(
        n_array[:3,:6],
        np.array(
            [[6, -1, -1, -1, -1, -1],
            [-1, 190, 0, 0, 0, 0],
            [-1, 0, 147, 0, 0, 0]]
        ),
        rtol=1e-5, atol=0
    )

def test_scipy_sparse(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    n_array = subgraph.to_scipy_sparse()
    assert n_array.getformat() == "csr"

    set_ = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (12, 1), (12, 2),
            (12, 3), (12, 4), (12, 8), (12, 11), (12, 13), (14, 2), )
    not_set_ = ((8, 8), (10, 6), (10, 10), (8, 1), (249, 2))
    assert all(i in get_items(n_array) for i in set_)
    assert all(i not in get_items(n_array) for i in not_set_)

def test_get_numbers(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    subgraph.check_attributes()
    
    assert subgraph._get_n_nodes() == 256
    assert subgraph._get_n_edges() == 1078
    assert subgraph.nx_graph.number_of_nodes() == 256
    assert subgraph.nx_graph.number_of_edges() == 1078
