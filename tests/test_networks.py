import pytest
import numpy as np

import kglab
from kglab.subg import SubgraphMatrix, Subgraph

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

#
# A query that defines a subgraph as subject -> object
#
QUERY1 = """
SELECT ?subject ?object
WHERE {
    ?subject rdf:type wtm:Recipe .
    ?subject wtm:hasIngredient ?object .
}
"""

def test_distances_mtx(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)

    dist = subgraph.get_distances(subgraph.to_scipy_sparse())
    np.testing.assert_allclose(
        dist[0,:6],
        [0, 1, 1, 1, 1, 1]
    )

    