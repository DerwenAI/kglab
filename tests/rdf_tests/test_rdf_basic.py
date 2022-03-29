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
import json

from rdf_tests.rdflib_tools import read_manifest


def parse_manifest(dir_, file_):
    """ Retrieve tests manifest """
    manifest_file = DATA_DIR / dir_ / file_
    ic(manifest_file)

    yield read_manifest(manifest_file)

def clean_filepath(filepath):
    """ Clean paths loaded from RDF manifest """
    return str(Path(str(filepath))).replace("file:", "")

def result_to_string(iter_):
    import json
    res = [json.dumps(row.asdict()) for row in iter_]
    return "\n".join(res)
        
    
class Report(dict):
    __basic = {"input", "query", "error", "length_check_error"}

    def full(self):
        return json.dumps(self)
    
    def log(self):
        print("---------------- REPORT ----------------")
        print(self)

    def __str__(self):
        dct = {}
        for name in self.keys():
            dct[name] = {}
            for k in self[name]:
                if k in self.__basic:
                    dct[name][k] = self[name][k]
        return json.dumps(dct, indent=4)

#
# report global variable
#
report = Report()

def run_test(t, dir_):
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
    
    report[t.name] = {}
    report[t.name]["input"] = None
    report[t.name]["query"] = None
    report[t.name]["expected"] = None
    report[t.name]["output"] = None
    report[t.name]["error"] = None
    report[t.name]["length_check"] = None
    report[t.name]["length_check_error"] = None

    #
    # load test data in the graph
    #
    if t.data is not None:
        kg.load_rdf(t.data)
        fname = t.data.split("/")[-1]
        report[t.name]["input"] = f"{dir_}/{fname}"  
        
    
    # for s, p, o in kg._g: print(s,p,o)

    #
    # load test SPARQL query
    #
    sparql = None
    action_path = clean_filepath(t.action)
    with open(action_path, mode="r") as f:
        sparql = f.read()
    qname = t.action.split("/")[-1]
    report[t.name]["query"] = f"{dir_}/{qname}"  

    # for row in kg.query(sparql): ic(row)  

    #
    # check if the query returned something
    #
    try:
        report[t.name]["output"] = result_to_string(kg.query(sparql))
        for row in kg.query(sparql):
            assertion = row is not None
            if assertion is False:
                assert False
    except AssertionError:
        report[t.name]["error"] = "ERROR: query result returned None"
        return      
    except Exception as e:
        report[t.name]["error"] = str(e)
        return

    #
    # read the expected results as dictionary
    #    
    if t.result is not None:
        report[t.name]["output"] = result_to_string(kg.query(sparql))
        results_path = clean_filepath(t.result)
        with open(results_path) as f:
            report[t.name]["expected"] = f.read()

        if t.result.endswith(".srx"):
            import xmltodict
            results_dct = xmltodict.parse(
                open(results_path, mode="rb").read()
            )

            # ic(results_dct["sparql"]["results"])

            #
            # for now we just test the length of the results to spot major anomalies
            #
            try:
                report[t.name]["length_check"] = \
                    len(list(kg.query(sparql))) == len(results_dct["sparql"]["results"])
            except Exception as e:
                report[t.name]["length_check"] = False
                report[t.name]["length_check_error"] = str(e)

            #
            # TODO: add more checks here
            #
        elif t.result.endswith(".ttl"):
            #
            # TODO: add check here for ttl serialised files
            #
            pass
            


def test_rdf_runner(rdf_basic=True, oxigraph=True):
    if rdf_basic is True:
        dir_, file_ = "basic", "manifest.ttl"
        generator = parse_manifest(dir_, file_)
        for loop in generator:
            for e, type_, test in loop:
                print(f"Running {dir_}/{test.name}")
                run_test(test, dir_)

    if oxigraph is True:
        dir_, file_ = "oxigraph-tests/sparql", "manifest.ttl"
        generator = parse_manifest(dir_, file_)
        for loop in generator:
            for e, type_, test in loop:
                print(f"Running {dir_}/{test.name}")
                run_test(test, dir_)
        
    report.log()  
                
        