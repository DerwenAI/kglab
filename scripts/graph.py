
from os.path import abspath, dirname
import pathlib
import sys
import typing

from icecream import ic
from cryptography.hazmat.primitives import hashes  # type: ignore  # pylint: disable=E0401
import rdflib  # type: ignore  # pylint: disable=E0401
import rdflib.plugin  # type: ignore  # pylint: disable=E0401

sys.path.insert(0, str(pathlib.Path(dirname(dirname(abspath(__file__))))))
from kglab.graph import PropertyStore


if __name__ == "__main__":
    rdflib.plugin.register(
        "kglab",
        rdflib.store.Store,
        "kglab",
        "PropertyStore",
    )

    use_new_store = True # False
    lpg: typing.Optional[ PropertyStore ] = None  # type: ignore

    if use_new_store:
        graph = rdflib.Graph(
            store = "kglab",
            identifier = "foo",
        )

        lpg = PropertyStore.get_lpg(graph)
        lpg.digest = hashes.Hash(hashes.BLAKE2b(64))  # type: ignore
    else:
        graph = rdflib.Graph()


    ## load RDF triples
    ttl_text = """
@prefix sota: <http://www.w3.org/2012/12/rdf-val/SOTA-ex#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

sota:peep0 a foaf:Person ;
    foaf:givenName "Alice" ;
    foaf:familyName "Nakamoto" ;
    foaf:phone <tel:+1.555.222.2222> ;
    foaf:mbox <mailto:nak@gmail.com> .

sota:peep1 a foaf:Person ;
    foaf:givenName "Bob" ;
    foaf:familyName "Patel" ;
    foaf:phone <tel:+1.555.666.5150> ;
    foaf:mbox <mailto:bobp@gmail.com> .

sota:peep2 a foaf:Person ;
    foaf:givenName "Dhanya" ;
    foaf:familyName "O'Neill" ;
    foaf:phone <tel:+1.555.123.9876> ;
    foaf:mbox <mailto:do-n@gmail.com> .
    """

    graph.parse(data=ttl_text, format="ttl")
    ic(len(graph))


    ## run a SPARQL query
    bindings: dict = {
        "surname": rdflib.term.Literal("Alice"),
    }

    sparql = """
    SELECT ?person ?pred ?surname
      WHERE {
        ?person ?pred ?surname .
      }
    ORDER BY DESC(?surname)
    """

    for row in graph.query(sparql, initBindings=bindings):
        r = row.asdict()
        ic(r)


    ## remove
    for s, p, o in graph:
        pass

    graph.remove((s, p, o,))
    ic(len(graph))

    graph.remove((s, p, o,))

    if lpg is not None:
        ic(lpg.digest.finalize().hex())  # type: ignore
        ic(lpg._node_names)
        ic(lpg._rel_names)
        ic(lpg._tuples)
