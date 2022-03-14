
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

    if use_new_store:
        graph = rdflib.Graph(
            store = "kglab",
            identifier = "foo",
        )

        lpg = PropertyStore.get_lpg(graph)
        ic(type(lpg))

        lpg.digest = hashes.Hash(hashes.BLAKE2b(64))  # type: ignore
    else:
        graph = rdflib.Graph()


    ## load RDF triples

    ttl_text = """
@prefix : <http://www.w3.org/2012/12/rdf-val/SOTA-ex#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

:peep0 a foaf:Person ;
    foaf:givenName "Alice" ;
    foaf:familyName "Nakamoto" ;
    foaf:phone <tel:+1.555.222.2222> ;
    foaf:mbox <mailto:nak@gmail.com> .

:peep1 a foaf:Person ;
    foaf:givenName "Bob" ;
    foaf:familyName "Patel" ;
    foaf:phone <tel:+1.555.666.5150> ;
    foaf:mbox <mailto:bobp@gmail.com> .

:peep2 a foaf:Person ;
    foaf:givenName "Dhanya" ;
    foaf:familyName "O'Neill" ;
    foaf:phone <tel:+1.555.123.9876> ;
    foaf:mbox <mailto:do-n@gmail.com> .
    """

    graph.parse(data=ttl_text, format="ttl")
    ic(len(graph))


    ## run a SPARQL query

    bindings: typing.Dict[ str, str ] = {
        "surname": "Alice",
    }

    sparql = """
    SELECT ?person ?pred ?surname
      WHERE {
        ?person ?pred ?surname .
      }
    ORDER BY DESC(?surname)
    """

    for row in graph.query(sparql, initBindings=bindings):
        ic(row.asdict())


    sys.exit(0)
    ## misc. CRUD operations

    s = rdflib.term.URIRef("https://www.food.com/recipe/327593")
    p = rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    o = rdflib.term.URIRef("http://purl.org/heals/food/Recipe")

    graph.add((s, p, o))
