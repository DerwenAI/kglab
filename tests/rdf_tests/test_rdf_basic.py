"""
Run official RDF-tests and Oxigraph tests from text files
<https://github.com/w3c/rdf-tests>
"""

from os.path import abspath, dirname
import sys
from pathlib import Path

project_dir = Path(dirname(dirname(dirname(abspath(__file__)))))
sys.path.insert(0, str(project_dir))
tests_dir = project_dir / "tests"
sys.path.insert(0, str(tests_dir))
DATA_DIR = project_dir / "tests" / "rdf_tests" / "dat"

from rdflib.plugins.sparql.results.rdfresults import RDFResult
import kglab
from icecream import ic
import json

from rdf_tests.rdflib_tools import read_manifest, bindingsCompatible


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
    """ Just some neat print-out """
    __basic = {"input", "query", "error", "length_check_error"}

    def full(self):
        return json.dumps(self)
    
    def log(self):
        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- REPORT -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print(self)
        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

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
        
    
    #
    # load test SPARQL query
    #
    sparql = None
    action_path = clean_filepath(t.action)
    with open(action_path, mode="r") as f:
        sparql = f.read()
    qname = t.action.split("/")[-1]
    report[t.name]["query"] = f"{dir_}/{qname}"  

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
    results_path = clean_filepath(t.result)
    
    if t.result is not None:
        report[t.name]["output"] = result_to_string(kg.query(sparql))
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
            expected = RDFResult(t.result)
            try:
                assert bindingsCompatible(expected, kg.query(sparql))
            except AssertionError:
                report[t.name]["error"] = "ERROR: bindings do not match"


def test_rdf_runner():
    tests_list = (
        "algebra","basic", "bind", "ask",
        "oxigraph-tests/sparql",
        "cast", "exists", "grouping",
        "distinct", "sort", "expr-ops",
        "construct", "syntax-sparql1",
        "syntax-sparql2", "syntax-sparql3",
        "syntax-sparql4", "syntax-sparql5",
    )
    
    
    for dir_ in tests_list:
        generator = parse_manifest(dir_, "manifest.ttl")
        for loop in generator:
            for e, type_, test in loop:
                print(f"Running {dir_}/{test.name}")
                run_test(test, dir_)
    
    
        
    report.log()

    from datetime import datetime
    t = datetime.now().strftime("%H:%M:%S")
    fname = dirname(abspath(__file__)) + f"/report-{t}.json"
    print(fname)
    with open(fname, mode="w") as f:
        f.write(str(report))
