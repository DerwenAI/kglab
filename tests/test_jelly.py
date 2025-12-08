import pathlib
import tempfile
import apeye.url
from rdflib import URIRef, Literal
import kglab


def make_test_graph():
    kg = kglab.KnowledgeGraph()
    s = URIRef("http://example.org/Alice")
    p = URIRef("http://example.org/name")
    o = Literal("Alice")
    kg.add(s, p, o)
    return kg, (s, p, o)


def test_jelly_roundtrip_basic(tmp_path):
    kg, triple = make_test_graph()

    file = tmp_path / "basic.jelly"
    kg.save_rdf(file, format="jelly")

    kg2 = kglab.KnowledgeGraph().load_rdf(file, format="jelly")

    assert len(kg2._g) == 1
    assert triple in kg2._g


def test_jelly_load_save_measure(tmp_path):
    kg, _ = make_test_graph()

    file = tmp_path / "measure.jelly"
    kg.save_rdf(file, format="jelly")

    kg2 = kglab.KnowledgeGraph()
    kg2.load_rdf(file, format="jelly")

    measure = kglab.Measure()
    measure.measure_graph(kg2)

    assert measure.get_edge_count() == 1
    assert measure.get_node_count() == 1


def test_multiple_file_load_jelly(tmp_path):
    kg1, _ = make_test_graph()
    f1 = tmp_path / "one.jelly"
    kg1.save_rdf(f1, format="jelly")

    kg2, _ = make_test_graph()
    f2 = tmp_path / "two.jelly"
    kg2.save_rdf(f2, format="jelly")

    kg_seq = kglab.KnowledgeGraph()
    kg_seq.load_rdf(f1, format="jelly")
    kg_seq.load_rdf(f2, format="jelly")

    measure = kglab.Measure()
    measure.measure_graph(kg_seq)
    seq_edges = measure.get_edge_count()
    seq_nodes = measure.get_node_count()

    kg_glob = kglab.KnowledgeGraph()
    kg_glob.load_rdf(str(tmp_path / "*.jelly"), format="jelly")

    measure.reset()
    measure.measure_graph(kg_glob)

    assert measure.get_edge_count() == seq_edges
    assert measure.get_node_count() == seq_nodes


def test_jelly_formats_paths(tmp_path):
    kg, triple = make_test_graph()

    file_path = tmp_path / "pathlib_test.jelly"
    kg.save_rdf(file_path, format="jelly")

    kg2 = kglab.KnowledgeGraph()
    kg2.load_rdf(str(file_path), format="jelly")
    assert triple in kg2._g

    url = apeye.url.URL(file_path.as_uri())
    kg3 = kglab.KnowledgeGraph()
    kg3.load_rdf(url, format="jelly")
    assert triple in kg3._g


def test_jelly_query_after_load(tmp_path):
    kg, _ = make_test_graph()
    file = tmp_path / "query_test.jelly"
    kg.save_rdf(file, format="jelly")

    kg2 = kglab.KnowledgeGraph().load_rdf(file, format="jelly")

    df = kg2.query_as_df("SELECT (COUNT(*) as ?Triples) WHERE { ?s ?p ?o }")
    assert df.values[0][0] == 1
