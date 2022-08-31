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


def test_init_obs_matx(kg_test_data):
    kg_test_data.to_observation_matrix()