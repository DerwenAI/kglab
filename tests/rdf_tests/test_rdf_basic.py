from os.path import abspath, dirname
import sys
from pathlib import Path

project_dir = Path(dirname(dirname(dirname(abspath(__file__)))))
sys.path.insert(0, str(project_dir))
tests_dir = project_dir / "tests"
sys.path.insert(0, str(tests_dir))
DATA_DIR = project_dir / "tests" / "rdf_tests" / "dat"

import kglab
from icecream import ic

from rdf_tests.rdflib_tools import read_manifest


def parse_manifest(dir_, file_):
    """ Retrieve tests manifest """
    manifest_file = DATA_DIR / dir_ / file_
    ic(manifest_file)

    yield read_manifest(manifest_file)

def clean_filepath(filepath):
    """ Clean paths loaded from RDF manifest """
    return str(Path(str(filepath))).replace("file:", "")
    

def run_test(t):
    namespaces = {
        "xmlns:rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "xmlns:xs": "http://www.w3.org/2001/XMLSchema#",
        "xmlns": "http://www.w3.org/2005/sparql-results#"
    }

    kg = kglab.KnowledgeGraph(
        name = "RDF Tests Graph",
        base_uri = "http://example/",
        namespaces = namespaces,
    )

    #
    # load test data in the graph
    #
    kg.load_rdf(t.data)
    
    # for s, p, o in kg._g: print(s,p,o)

    #
    # load test SPARQL query
    #
    sparql = None
    action_path = clean_filepath(t.action)
    with open(action_path, mode="r") as f:
        sparql = f.read()

    # for row in kg.query(sparql): ic(row)  

    #
    # read the expected results as dictionary
    #
    results_path = clean_filepath(t.result)
    import xmltodict
    results_dct = xmltodict.parse(
        open(results_path, mode="rb").read()
    )

    # ic(results_dct["sparql"]["results"])

    #
    # for now we just test the length of the results to spot major anomalies
    #
    assertion = len(list(kg.query(sparql))) == len(results_dct["sparql"]["results"])
    print(f"{t.name} resulted in {assertion}\n\n")


def test_rdf_runner(rdf_basic=True, oxigraph=True):
    if rdf_basic is True:
        dir_, file_ = "basic", "manifest.ttl"
        generator = parse_manifest(dir_, file_)
        for loop in generator:
            for e, type_, test in loop:
                try:
                    print(f"Running {dir_}/{test.name}")
                    run_test(test)
                except Exception as e:
                    print(f"ERROR: {test.name} resulted in {str(e)}\n\n")

    if oxigraph is True:
        dir_, file_ = "oxigraph-tests/sparql", "manifest.ttl"
        generator = parse_manifest(dir_, file_)
        for loop in generator:
            for e, type_, test in loop:
                try:
                    print(f"Running {dir_}/{test.name}")
                    run_test(test)
                except Exception as e:
                    print(f"ERROR: {test.name} resulted in {str(e)}\n\n")
        
            
                
        