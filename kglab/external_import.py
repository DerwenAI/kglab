#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/kglab#license-and-copyright

"""
Provide support for importing RDF data from multiple existing graph
databases, preferably triplestores:

  * neo4j
  * Ontotext-GraphDB
  * Blazegraph
  * DataStax
"""

import json
import requests  # pylint: disable=E0401
import rdflib  # type: ignore  # pylint: disable=E0401
import urllib.parse


def import_from_neo4j (
    username: str,
    password: str,
    dbname: str,
    host: str = "localhost",
    port: str = "7474"
    ) -> rdflib.Graph:
    """
Wrapper for a
[`Cypher`](https://neo4j.com/labs/neosemantics/tutorial/#_using_the_cypher_n10s_rdf_export_procedure)
export request, to provide neo4j integration through the
[`neosemantics`](https://neo4j.com/labs/neosemantics/) library.

Tested with ~10GB of stored triples.

    username:
the user name, as a string

    password:
the password, as a string

    dbname:
the database name, as a string

    host:
optionally, the neo4j server domain name or IP address, as a string – including the protocol scheme; defaults to `"http://localhost"`

    port:
optionally, the neo4j server port; defaults to `"7474"`

    returns:
an [`rdflib.Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=graph#graph) object parsed from the exported RDF
    """
    # get all of the entities and properties via `neosemantics`
    # exported as RDF triples
    cypher = "Match (n)-[r]->(m) Return n,r,m;"

    payload = {
        "cypher": cypher,
        "format": "RDF/XML",
        }

    # construct the export URL
    u = urllib.parse.urlparse(host)
    netloc = "{}:{}".format(u.netloc, port)
    path = "/rdf/{}/cypher".format(dbname)
    url = urllib.parse.urlunparse((u.scheme, netloc, path, "", "", "",))

    try:
        response = requests.post(
            url,
            auth = (username, password),
            data = json.dumps(payload),
            )

        # raise an error on unsuccessful status codes
        response.raise_for_status()
    except Exception as e:  # pylint: disable=W0703
        print("neo4j import: ", e)

    g = rdflib.Graph().parse(data=response.text)
    return g


######################################################################
## main entry point

if __name__ == "__main__":
    graph = import_from_neo4j(  # nosec
        username = "user",
        password = "pswd",
        dbname = "rdfdb",
        host = "localhost",
        port = "7474",
        )
