import pytest
import numpy as np
from networkx.exception import NetworkXNoPath

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

    dist = subgraph.get_distances(subgraph.to_adjacency())
    np.testing.assert_allclose(
        dist[0,:6],
        [0, 2.44948974, 2.44948974, 2.44948974, 2.44948974, 2.44948974]
    )

def test_shortest_path(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)

    try:
        subgraph.get_shortest_path(2, 6)
        assert False
    except NetworkXNoPath:
        pass
    
    dist = subgraph.get_shortest_path(0, 2)
    assert dist == [0, 2]

    try:
        dist = subgraph.get_shortest_path(0, 7)
        assert False
    except NetworkXNoPath:
        pass

def test_describe(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    print(subgraph.describe())
    

    