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
    from kglab.subg import SubgraphMatrix
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
    from kglab.subg import SubgraphMatrix
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