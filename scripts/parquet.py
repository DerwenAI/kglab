#!/usr/bin/env python
# -*- coding: utf-8 -*-

from icecream import ic  # type: ignore  # pylint: disable=E0401
import chocolate  # type: ignore  # pylint: disable=E0401
import json
import pandas as pd  # type: ignore  # pylint: disable=E0401
import pathlib
import pyarrow as pa
import rdflib  # type: ignore  # pylint: disable=E0401
import typing
import urlpath  # type: ignore  # pylint: disable=E0401

PathLike = typing.Union[ str, pathlib.Path, urlpath.URL ]
IOPathLike = typing.Union[ PathLike, typing.IO ]


class KnowledgeGraph:

    _PARQUET_COL_NAMES: typing.List[str] = [
        "subject",
        "predicate",
        "object"
    ]


    def __init__ (
        self,
    ):
        self._g = rdflib.Graph()


    def load_parquet (
        self,
        path: IOPathLike,
        **kwargs: typing.Any,
        ) -> "KnowledgeGraph":
        """
        """
        df = pd.read_parquet(
            path,
            **chocolate.filter_args(kwargs, pd.read_parquet)
        )

        df.apply(
            lambda row: self._g.parse(data="{} {} {} .".format(row[0], row[1], row[2]), format="ttl"),
            axis=1,
        )

        ic(df)

        table = pa.Table.from_pandas(df)
        ic(table.schema.metadata)

        meta = table.schema.metadata[b'pandas'].decode("utf-8")
        print(type(meta))
        ic(meta)

        j = json.loads(meta)
        ic(j)

        return self


    def save_parquet (
        self,
        path: IOPathLike,
        *,
        compression: str = "snappy",
        storage_options: dict = None, # pylint: disable=W0613
        **kwargs: typing.Any,
        ) -> None:
        """
        """
        rows_list: typing.List[dict] = [
            {
                self._PARQUET_COL_NAMES[0]: s.n3(),
                self._PARQUET_COL_NAMES[1]: p.n3(),
                self._PARQUET_COL_NAMES[2]: o.n3(),
            }
            for s, p, o in self._g
        ]

        df = pd.DataFrame(rows_list, columns=self._PARQUET_COL_NAMES)

        df.to_parquet(
            path,
            compression=compression,
            #storage_options=storage_options,
            **chocolate.filter_args(kwargs, df.to_parquet),
        )


if __name__ == "__main__":
    ns_prefix = {
        "ind": "http://purl.org/heals/ingredient/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "wtm": "http://purl.org/heals/food/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
    }

    ns = {}
    kg = KnowledgeGraph()

    for prefix, iri in ns_prefix.items():
        ns[prefix] = rdflib.Namespace(iri)
        kg._g.namespace_manager.bind(prefix, ns[prefix])

    uri = "https://www.food.com/recipe/327593"
    s = rdflib.URIRef(uri)

    p = ns["wtm"].hasCookTime
    o = ns["wtm"].Recipe
    kg._g.add((s, p, o,))

    p = ns["wtm"].hasCookTime
    o = rdflib.Literal("PT8M", datatype=ns["xsd"].duration)
    kg._g.add((s, p, o,))

    p = ns["wtm"].hasIngredient
    o = ns["ind"].ChickenEgg
    kg._g.add((s, p, o,))

    p = ns["wtm"].hasIngredient
    o = ns["ind"].CowMilk
    kg._g.add((s, p, o,))

    p = ns["wtm"].hasIngredient
    o = ns["ind"].WholeWheatFlour
    kg._g.add((s, p, o,))

    kg.save_parquet("foo.parquet")
    kg.load_parquet("foo.parquet")
