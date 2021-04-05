#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from icecream import ic  # type: ignore
import jinja2  # pylint: disable=E0401
import json
import kglab
import pathlib
#import sys
import tempfile
import typing


def get_jinja2_template (
    template_file: str,
    ) -> jinja2.Template:
    """
Load a Jinja2 template.
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("."),
        autoescape=True,
        )

    return env.get_template(template_file)


def is_kind (  # pylint: disable=W0621
    item: dict,
    kind_list: typing.List[str],
    ) -> bool:
    """
Test whether the given JSON-LD content item has a "@type" within the
specified list.
    """
    if "@type" not in item:
        return False

    return any(map(lambda k: item["@type"].endswith(k), kind_list))  # pylint: disable=W0108


######################################################################
## main entry point

if __name__ == "__main__":
    # create a KnowledgeGraph object
    kg = kglab.KnowledgeGraph()

    # load RDF from a file
    ttl_path = pathlib.Path("../pytextrank/docs/biblio.ttl")
    kg.load_rdf(ttl_path, format="ttl")

    # serialize as JSON-LD
    json_path = pathlib.Path(tempfile.NamedTemporaryFile().name)
    kg.save_jsonld(json_path)

    bib_g = []

    # transform for use by templates
    with open(json_path, "r") as f:
        bib_j = json.load(f)
        bib_g = bib_j["@graph"]

    types = {
        item["@type"]
        for item in bib_g
        if "@type" in item
        }
    #ic(types)

    authors = {
        item["@id"]: item
        for item in bib_g
        if is_kind(item, ["Author"])
        }
    #ic(authors)

    pubs = {
        item["@id"]: item
        for item in bib_g
        if is_kind(item, ["Collection", "Journal", "Proceedings"])
        }
    #ic(pubs)

    content = sorted(
        [
            item
            for item in bib_g
            if is_kind(item, ["Article", "Slideshow"])
            ],
        key = lambda item: item["https://derwen.ai/ns/v1#citeKey"],
        )
    #ic(content)

    letters = sorted(list({
                item["https://derwen.ai/ns/v1#citeKey"][0].upper()
                for item in content
                }))

    groups: typing.Dict[str, list] = {
        l: []
        for l in letters
        }

    for item in content:
        #ic(item)

        trans = {
            "citekey": item["https://derwen.ai/ns/v1#citeKey"],
            "type": item["@type"].split("/")[-1],
            "url": item["@id"],
            "date": item["dct:date"]["@value"],
            "title": item["dct:title"],
            "abstract": item["http://purl.org/ontology/bibo/abstract"],
            }

        trans["auth"] = [
            {
                "url": auth["@id"],
                "name": authors[auth["@id"]]["http://xmlns.com/foaf/0.1/name"],
                }
            for auth in item["http://purl.org/ontology/bibo/authorList"]["@list"]
            ]

        if "http://purl.org/ontology/bibo/doi" in item:
            trans["doi"] = item["http://purl.org/ontology/bibo/doi"]["@value"]

        if "https://derwen.ai/ns/v1#openAccess" in item:
            trans["open"] = item["https://derwen.ai/ns/v1#openAccess"]["@id"]

        if "dct:isPartOf" in item:
            pub = pubs[item["dct:isPartOf"]["@id"]]

            trans["pub"] = {
                "url": pub["dct:identifier"]["@id"],
                "title": pub["http://purl.org/ontology/bibo/shortTitle"],
                }

            if "http://purl.org/ontology/bibo/volume" in item:
                trans["pub"]["volume"] = item["http://purl.org/ontology/bibo/volume"]["@value"]

            if "http://purl.org/ontology/bibo/issue" in item:
                trans["pub"]["issue"] = item["http://purl.org/ontology/bibo/issue"]["@value"]

            if "http://purl.org/ontology/bibo/pageStart" in item:
                trans["pub"]["pageStart"] = item["http://purl.org/ontology/bibo/pageStart"]["@value"]

            if "http://purl.org/ontology/bibo/pageEnd" in item:
                trans["pub"]["pageEnd"] = item["http://purl.org/ontology/bibo/pageEnd"]["@value"]

        #ic(trans)
        letter = item["https://derwen.ai/ns/v1#citeKey"][0].upper()
        groups[letter].append(trans)

    # render markdown using templates
    template = get_jinja2_template("biblio.template")
    md_path = pathlib.Path("out.md")

    with open(md_path, "w") as f:
        f.write(template.render(groups=groups))
