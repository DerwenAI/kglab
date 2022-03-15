import pytest
from os.path import abspath, dirname

import kglab


@pytest.fixture(scope="module")
def kg_test_data():
    # create a KnowledgeGraph object
    kg = kglab.KnowledgeGraph()

    # load RDF from a file
    kg.load_rdf("dat/gorm.ttl", format="ttl")
    
    return kg



def test_check_format(kg_test_data):
    # this should do nothing
    # supported data format
    kg_test_data._check_format("text/n3")
    
    try:
        # this should raise
        # format not supported and no no rdflib serializer exist
        kg_test_data._check_format("does_not_exist")
    except TypeError:
        assert True
    except Exception:
        assert False


def test_check_encoding(kg_test_data):
    kg_test_data._check_encoding("utf-8")
    kg_test_data._check_encoding("utf-16")
    kg_test_data._check_encoding("ascii")
    
    try:
        kg_test_data._check_encoding("not_supported")
    except LookupError:
        assert True


def test_get_filename(kg_test_data):
    # empy string
    test1 = kg_test_data._get_filename("")
    assert test1 is None

    # an address
    from urlpath import URL
    test2 = kg_test_data._get_filename(URL("gs://kglab-tutorial/foaf.parquet"))
    assert type(test2) == str
    assert test2 == "gs://kglab-tutorial/foaf.parquet"

    # a path object
    from pathlib import Path
    path = Path(dirname(dirname(abspath(__file__)))) / "dat/gorm.ttl"
    test3 = kg_test_data._get_filename(path)
    assert type(test3) == str
    assert test3.endswith("dat/gorm.ttl")

    # a non-supported type
    error = Exception()
    try:
        test4 = kg_test_data._get_filename(error)
    except TypeError:
        assert True
