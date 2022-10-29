from .test_querying import kg_test_data

import kglab

from .__init__ import DAT_FILES_DIR

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
  LIMIT 2
"""

def test_gpviz(kg_test_data):
    try:
        kg_test_data.visualize_query(QUERY1)
    except:
        assert False
    
    assert True