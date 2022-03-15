import pytest

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
    
    kg.load_rdf(DAT_FILES_DIR / "tmp.ttl")
    
    yield kg
    
    del kg

#
# standard queries
#
# list recipes with ingredient x, y, z
QUERY1 = """
SELECT ?recipe ?definition
  WHERE {
    ?recipe rdf:type wtm:Recipe .
    ?recipe skos:definition ?definition .
    ?recipe wtm:hasIngredient ind:ChickenEgg .
    ?recipe wtm:hasIngredient ind:AllPurposeFlour .
    ?recipe wtm:hasIngredient ind:Salt .
    ?recipe wtm:hasIngredient ind:VanillaExtract
  }
"""
# list ingredients for recipe
QUERY2 = """
SELECT ?definition ?ingredient
  WHERE {
    <https://www.food.com/recipe/135405> rdf:type wtm:Recipe .
    <https://www.food.com/recipe/135405> skos:definition ?definition .
    <https://www.food.com/recipe/135405> wtm:hasIngredient ?ingredient
  }
"""

# TODO: add more queries

def test_query_base(kg_test_data):
    results = list(kg_test_data.query(QUERY1))
    assert len(results) == 14
    
    results = list(kg_test_data.query(QUERY2))
    assert len(results) == 7


def test_query_as_df(kg_test_data):
    results = kg_test_data.query_as_df(QUERY1)
    assert len(results) == 14

    results = kg_test_data.query_as_df(QUERY2)
    assert len(results) == 7


def test_visualize_query(kg_test_data):
    viz = kg_test_data.visualize_query(QUERY1)

    nodes = [
        "?recipe",
        "ind:AllPurposeFlour",
        "ind:ChickenEgg",
        "ind:Salt",
        "ind:VanillaExtract",
        "wtm:Recipe",
        "?definition"
    ]
    assert all(n in nodes for n in viz.node_ids) 
    assert len(viz.edges) == 6


def test_n3fy_base(kg_test_data):
    import rdflib
    
    n3fy_literal = kg_test_data.n3fy(rdflib.term.Literal("english shortbread"))
    assert n3fy_literal == "english shortbread"
    assert type(n3fy_literal) is str
    
    n3fy_node = kg_test_data.n3fy(rdflib.term.URIRef("https://www.food.com/recipe/97832"))
    assert n3fy_node == "<https://www.food.com/recipe/97832>"


def test_n3fy_row(kg_test_data):
    first_result = list(kg_test_data.query(QUERY1))[0]
    results = {}
    results["recipe"] = first_result[0]
    results["definition"] = first_result[1]
    
    serialized = kg_test_data.n3fy_row(results)
    
    assert serialized["recipe"] == "<https://www.food.com/recipe/123656>"
    assert serialized["definition"] == "french vanilla crepes"


def test_validate_shacl():
    pass


def test_walk_roam_graph():
    pass