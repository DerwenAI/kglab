
from icecream import ic
import datetime
import json
import kglab
import pathlib
import rdflib
import sys


SEEN = set()

NAMESPACES = {
    "roam":  "https://roamresearch.com/ns/",
}


def scan_object (kg, obj):
    roam_ns = NAMESPACES["roam"]
    uid = obj["uid"]

    if uid not in SEEN:
        SEEN.add(uid)

        url = roam_ns + uid;
        node = rdflib.URIRef(url)

        kg.add(node, kg.get_ns("rdf").type, kg.get_ns("dct").Text)

        if "title" in obj:
            descrip = obj["title"]
        elif "string" in obj:
            descrip = obj["string"]

        kg.add(node, kg.get_ns("skos").definition, rdflib.Literal(descrip))

        user_uid = obj[":edit/user"][":user/uid"]
        user_url = roam_ns + user_uid;
        kg.add(node, kg.get_ns("dct").Creator, rdflib.URIRef(user_url))

        timestamp = obj["edit-time"]
        dt = datetime.datetime.utcfromtimestamp(round(timestamp / 1000.0))
        kg.add(node, kg.get_ns("dct").Date, rdflib.Literal(dt.isoformat(), datatype=rdflib.XSD.dateTime))

        if "children" in obj:
            for child in obj["children"]:
                child_uid = scan_object(kg, child)
                child_url = roam_ns + child_uid;
                kg.add(node, kg.get_ns("dct").references, rdflib.URIRef(child_url))

    return uid


kg = kglab.KnowledgeGraph(namespaces=NAMESPACES)


path = pathlib.Path("roam.json")
data = json.load(path.open())

for obj in data:
    uid = scan_object(kg, obj)

#kg.infer_owlrl_closure()

ttl = kg.save_rdf_text()
print(ttl)
