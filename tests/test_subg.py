import pytest
import networkx as nx

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

def test_build_df_no_cuda(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    subgraph.kg.use_gpus = False

    df = subgraph.build_df()
    results = list(df.itertuples(index=False, name=None))
    
    expected = ((254, 3), (254,4), (255, 1), (255, 2), (255, 6))
    assert all(r == e for r in results[-1:-5] for e in expected)

def test_build_nx_graph(kg_test_data):
    subgraph = SubgraphMatrix(kg=kg_test_data, sparql=QUERY1)
    subgraph.kg.use_gpus = False

    nxg = nx.DiGraph()
    subgraph.build_nx_graph(nxg)
    
    assert nxg.number_of_nodes() == 256 and nxg.number_of_edges() == 1078
