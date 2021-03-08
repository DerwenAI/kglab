"""Provide support for importing rdf data from multiple existing graph databases preferable triplestores: Neo4J(neosemantics), Ontotext-GraphDB, Blazegraph, Dstastax"""
import requests
import json
import rdflib

#NEO4J support - tested with ~10GB of stored triples
def import_from_neo4j(user, pswd,dbname,ip = "localhost", port = "7474"  ):
    #url = 'http://localhost:7474/rdf/dbname/cypher'
    url = "http://"+ip+":"+port+"/rdf/"+dbname+"/cypher"
    cypher = 'Match (n)-[r]->(m) Return n,r,m;'#Get all entities and properties in neosemantics(RDF triples)
    payload = { 'cypher' : cypher , 'format' : 'RDF/XML' }

    try:
        response = requests.post(url, auth=(user, pswd), data = json.dumps(payload))
        response.raise_for_status()  # raise an error on unsuccessful status codes
    except Exception as e:
        print("Exception Found: ",e )

    g=rdflib.Graph()
    return g.parse(data=response.text)
  
# graph = import_from_neo4j("user", "pswd", "rdfdb",ip = "localhost", port = "7474" )
