"""
Serialization-Deserialization for `KnowledgeGraph`
see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

## Python standard libraries
import datetime
import io
import json
import typing
import codecs
import urlpath
import pathlib

### third-parties libraries
from icecream import ic  # type: ignore
import chocolate  # type: ignore
import csvwlib  # type: ignore
import morph_kgc  # type: ignore
import pandas as pd  # type: ignore

import rdflib  # type: ignore
import rdflib.plugin  # type: ignore
import rdflib.plugins.parsers.notation3 as rdf_n3  # type: ignore

## kglab - core classes
from .decorators import multifile
from .pkg_types import IOPathLike, PathLike
from .util import get_gpu_count, Mixin
from .version import _check_version


## pre-constructor set-up
_check_version()

if get_gpu_count() > 0:
    import cudf  # type: ignore  # pylint: disable=E0401


class SerdeMixin (Mixin):
    """
Provide serialization and deserialization methods for `KnowledgeGraph`:
* RDF
* JSONLD
* Parquet
* CSV
* Morph-KGC
* ROAM
    """
    ######################################################################
    ## serialization
    ##
    ## Format and software agnostic: We are interested in technology
    ## that will not be a barrier to widespread use. We want to allow
    ## the export of the entity triples in a variety of formats, at
    ## the most basic level as a CSV, so that an analyst can load the
    ## results into their system of choice. By prioritizing
    ## non-proprietary, universal formats the results can be easily
    ## integrated into several of the existing tools for creating
    ## network graphs.

    _RDF_FORMAT: typing.Tuple = (
        # RDFXMLParser
        "application/rdf+xml",
        "xml",
        # N3Parser
        "text/n3",
        "n3",
        # TurtleParser
        "text/turtle",
        "turtle",
        "ttl",
        # NTParser
        "application/n-triples",
        "ntriples",
        "nt",
        "nt11",
        # NQuadsParser
        "application/n-quads",
        "nquads",
        # TriXParser
        "application/trix",
        "trix",
        # TrigParser
        "trig",
        # JsonLDParser
        "json-ld",
    )

    _ERROR_ENCODE: str = "The text `encoding` value does not match anything in the Python codec registry"
    _ERROR_PATH: str = "The `path` file object must be a writable, bytes-like object"


    @classmethod
    def _check_format (
        cls,
        format: str,
        ) -> None:
        """
Semiprivate method to error-check that a `format` parameter corresponds to a known RDFlib serialization plugin;
otherwise this throws a `TypeError` exception
        """
        if format not in cls._RDF_FORMAT:
            try:
                rdflib.plugin.get(format, rdflib.serializer.Serializer)
            except Exception:
                raise TypeError("unknown format: {format}")


    @classmethod
    def _check_encoding (
        cls,
        encoding: str,
        ) -> None:
        """
Semiprivate method to error-check that an `encoding` parameter is within the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo);
otherwise this throws a `LookupError` exception
        """
        try:
            codecs.lookup(encoding)
        except LookupError:
            raise LookupError(cls._ERROR_ENCODE)


    @classmethod
    def _get_filename (
        cls,
        path: PathLike,
        ) -> typing.Optional[str]:
        """
Semiprivate method to extract a file name (str) for a file reference from a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) or its subclasses

    returns:
a string as a file name or URL to a file reference
        """
        if not path:
            filename = None
        elif isinstance(path, urlpath.URL):
            filename = str(path)
        elif isinstance(path, pathlib.Path):
            filename = path.as_posix()
        elif isinstance(path, str):
            filename = path
        else:
            raise TypeError(f"path variable not recognised {type(path)}")

        return filename


    @multifile()
    def load_rdf (
        self,
        path: IOPathLike,
        *,
        format: str = "ttl",
        base: str = None,
        **args: typing.Any,
        ) -> "KnowledgeGraph": # type: ignore
        """
Wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from the `path` source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.
Throws `TypeError` whenever a format parser plugin encounters a syntax error.

Note: this adds relations to an RDF graph, although it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); otherwise this throws a `TypeError` exception

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
logical URI to use as the document base; if not specified, the document location gets used

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        # error checking for the `format` parameter
        if format == "json-ld":
            raise TypeError("Use the load_jsonld() method instead")

        self._check_format(format)

        # substitute the `KnowledgeGraph.base_uri` as the document base, if used
        if not base and self.base_uri:
            base = self.base_uri

        try:
            if hasattr(path, "read"):
                self._g.parse(  # type: ignore
                    path,
                    format=format,
                    publicID=base,
                    **args,
                    )
            else:
                self._g.parse(  # type: ignore
                    self._get_filename(path),
                    format=format,
                    publicID=base,
                    **args,
                    )
        except rdf_n3.BadSyntax as e:
            ic(path)
            raise TypeError(str(e))

        return self


    def load_rdf_text (
        self,
        data: typing.AnyStr,
        *,
        format: str = "ttl",
        base: str = None,
        **args: typing.Any,
        ) -> "KnowledgeGraph": # type: ignore
        """
Wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from a text.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    data:
text representation of RDF graph data

    format:
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
logical URI to use as the document base; if not specified, the document location gets used

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        # error checking for the `format` parameter
        self._check_format(format)

        # substitute the `KnowledgeGraph.base_uri` as the document base, if used
        if not base and self.base_uri:
            base = self.base_uri

        self._g.parse( # type: ignore
            data=data,
            format=format,
            publicID=base,
            **args,
        )

        return self


    def save_rdf (
        self,
        path: IOPathLike,
        *,
        format: str = "ttl",
        base: str = None,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> None:
        """
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination.
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

    format:
serialization format, which defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
optional text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking for the `format` parameter
        if format == "json-ld":
            raise TypeError("Use the save_jsonld() method instead")

        self._check_format(format)

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # substitute the `KnowledgeGraph.base_uri` base set for the graph, if used
        if not base and self.base_uri:
            base = self.base_uri

        # error checking for a file-like object `path` parameter
        if hasattr(path, "write"):
            if hasattr(path, "encoding"):
                raise TypeError(self._ERROR_PATH)

            try:
                self._g.serialize( # type: ignore
                    destination=path,
                    format=format,
                    base=base,
                    encoding=encoding,
                    **args,
                    )
            except io.UnsupportedOperation:
                raise TypeError(self._ERROR_PATH)

        # otherwise write to a local file reference
        else:
            self._g.serialize( # type: ignore
                destination=self._get_filename(path),
                format=format,
                base=base,
                encoding=encoding,
                **args,
            )


    def save_rdf_text (
        self,
        *,
        format: str = "ttl",
        base: str = None,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> typing.AnyStr:
        """
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to a string.

    format:
serialization format, which defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins; otherwise this throws a `TypeError` exception

    base:
optional base set for the graph

    encoding:
optional text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

    returns:
text representing the RDF graph
        """
        # error checking for the `format` parameter
        self._check_format(format)

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # substitute the `KnowledgeGraph.base_uri` base set for the graph, if used
        if not base and self.base_uri:
            base = self.base_uri

        return self._g.serialize(  # type: ignore
            destination=None,
            format=format,
            base=base,
            encoding=encoding,
            **args,
        ).decode(encoding)


    @multifile()
    def load_jsonld (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> "KnowledgeGraph": # type: ignore
        """
Wrapper for [`rdflib-jsonld.parser.JsonLDParser.parse()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/parser.py) which parses an RDF graph from a [JSON-LD](https://json-ld.org/) source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

    encoding:
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # error checking for a file-like object `path` parameter
        if hasattr(path, "read"):
            f = path
        else:
            f = open(path, "r", encoding=encoding)  # type: ignore

        # load JSON from file (to verify format and trap exceptions at
        # this level) then dump to string – which is expected by the
        # JSON-LD plugin for RDFlib
        self._g.parse( # type: ignore
            data=json.dumps(json.load(f)),  # type: ignore
            format="json-ld",
            encoding=encoding,
            **args,
        )

        return self


    def save_jsonld (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        **args: typing.Any,
        ) -> None:
        """
Wrapper for [`rdflib-jsonld.serializer.JsonLDSerializer.serialize()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/serializer.py) which serializes the RDF graph to the `path` destination as [JSON-LD](https://json-ld.org/).
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

    path:
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

    encoding:
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception
        """
        # error checking for a file-like object `path` parameter
        if hasattr(path, "write"):
            if hasattr(path, "encoding"):
                raise TypeError(self._ERROR_PATH)

            f = path
        else:
            f = open(self._get_filename(path), "wb") # type: ignore

        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        f.write( # type: ignore
            self._g.serialize( # type: ignore
                format="json-ld",
                context=self.get_context(),
                indent=2,
                encoding=encoding,
                **args,
            )
        )


    _PARQUET_COL_NAMES: typing.List[str] = [
        "subject",
        "predicate",
        "object"
    ]

    @multifile()
    def load_parquet (
        self,
        path: IOPathLike,
        **kwargs: typing.Any,
        ) -> "KnowledgeGraph": # type: ignore
        """
Wrapper for [`pandas.read_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html?highlight=read_parquet#pandas.read_parquet) which parses an RDF graph represented as a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.
Uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled.

To prepare for upcoming **kglab** features, **this is the preferred method for deserializing an RDF graph.**

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; a file URL can also be a path to a directory that contains multiple partitioned files, including a bucket in cloud storage – based on [`fsspec`](https://github.com/intake/filesystem_spec)

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        if self.use_gpus:
            df = cudf.read_parquet(
                path,
                **chocolate.filter_args(kwargs, pd.read_parquet)
            ).to_pandas()

        else:
            df = pd.read_parquet(
                path,
                **chocolate.filter_args(kwargs, pd.read_parquet)
            )

        df.apply(
            lambda row: self._g.parse( # type: ignore
                data=f"{ row[0] } { row[1] } { row[2] } .",
                format="ttl",
            ),
            axis=1,
        )

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
Wrapper for [`pandas.to_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html?highlight=to_parquet) which serializes an RDF graph to a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.
Uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled.

To prepare for upcoming **kglab** features, **this is the preferred method for serializing an RDF graph.**

    path:
must be a file name (str), path object to a local file reference, or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; accessing cloud storage is based on [`fsspec`](https://github.com/intake/filesystem_spec)

    compression:
name of the compression algorithm to use; defaults to `"snappy"`; can also be `"gzip"`, `"brotli"`, or `None` for no compression

    storage_options:
extra options parsed by [`fsspec`](https://github.com/intake/filesystem_spec) for cloud storage access; **NOT USED** until `pandas` 1.2.x becomes stable across platforms and also RAPIDS provides support
        """
        rows_list: typing.List[dict] = [
            {
                self._PARQUET_COL_NAMES[0]: s.n3(),
                self._PARQUET_COL_NAMES[1]: p.n3(),
                self._PARQUET_COL_NAMES[2]: o.n3(),
            }
            for s, p, o in self._g # type: ignore
        ]

        if self.use_gpus:
            df = cudf.DataFrame(rows_list, columns=self._PARQUET_COL_NAMES)
        else:
            df = pd.DataFrame(rows_list, columns=self._PARQUET_COL_NAMES)

        df.to_parquet(
            path,
            compression=compression,
            #storage_options=storage_options,
            **chocolate.filter_args(kwargs, df.to_parquet),
        )


    def load_csv (
        self,
        url: str,
        ) -> "KnowledgeGraph": # type: ignore
        """
Wrapper for [`csvwlib`](https://github.com/DerwenAI/csvwlib) which parses a CSV file from the `path` source, then converts to RDF and merges into this RDF graph.

    url:
must be a URL represented as a string

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        new_rdf = csvwlib.CSVWConverter.to_rdf(
            url,
            mode="minimal",
            format="ttl",
        )
        return self.load_rdf_text(new_rdf)


    def materialize (
        self,
        config: str,
        ) -> "KnowledgeGraph": # type: ignore
        """
Binding to the [Morph-KGC](https://github.com/oeg-upm/morph-kgc) `materialize()` method.

    config:
morph-kgc configuration, it can be the path to the config file, or a string with the config; see <https://morph-kgc.readthedocs.io/en/latest/documentation/#library>

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        if len(self._g) == 0: # type: ignore
            # generate the triples and load them to an RDFlib graph
            self._g = morph_kgc.materialize(config)
        else:
            # merge
            # for caveats about merging this way:
            # <https://rdflib.readthedocs.io/en/stable/merging.html>
            self._g.parse(morph_kgc.materialize(config)) # type: ignore

        return self


    ######################################################################
    ## Roam Research integration

    def _walk_roam_graph (
        self,
        obj: dict,
        seen_uid: typing.Set[str] = None,
        ) -> str:
        """
Semiprivate method to traverse the Roam Research exported graph recursively, converting its objects into RDF representation.

    obj:
object to parse

    returns:
The `uid` identifier for the parsed object
        """
        if not seen_uid:
            seen_uid = set()

        roam_ns = str(self.get_ns("roam"))
        uid = obj["uid"]

        if uid not in seen_uid:
            seen_uid.add(uid)

            # create a node for this object
            node = rdflib.URIRef(roam_ns + uid)
            self.add(node, self.get_ns("rdf").type, self.get_ns("dct").Text)

            # represent title (complex object) or string description (simple object)
            if "title" in obj:
                descrip = obj["title"]
            elif "string" in obj:
                descrip = obj["string"]

            self.add(node, self.get_ns("skos").definition, rdflib.Literal(descrip))

            # represent the user who created/edited this object
            user_uid = obj[":edit/user"][":user/uid"]
            self.add(node, self.get_ns("dct").Creator, rdflib.URIRef(roam_ns + user_uid))

            # convert millisec timestamp to Unix epoch times (UTC) to datetime
            dt = datetime.datetime.utcfromtimestamp(round(obj["edit-time"] / 1000.0))
            self.add(node, self.get_ns("dct").Date, rdflib.Literal(dt.isoformat(), datatype=rdflib.XSD.dateTime))

            if "children" in obj:
                for child_obj in obj["children"]:
                    child_uid = self._walk_roam_graph(child_obj, seen_uid)
                    self.add(node, self.get_ns("dct").references, rdflib.URIRef(roam_ns + child_uid))

        return uid


    @multifile()
    def import_roam (
        self,
        path: IOPathLike,
        *,
        encoding: str = "utf-8",
        ) -> typing.List[str]:
        """
Import a graph in JSON that has been exported from the [Roam Research](https://roamresearch.com/) note-taking tool, then convert its objects and attributes into RDF representation.

For more details about the exported data from Roam Research, see:

  * <https://roamstack.com/roam-data-outside-roam/>
  * <https://nesslabs.com/roam-research-input-output>
  * <https://davidbieber.com/snippets/2020-04-25-roam-json-export/>

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

    path:
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

    encoding:
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

    returns:
a list of identifiers for the top-level nodes added from the Roam Research graph
        """
        # error checking for the `encoding` parameter
        self._check_encoding(encoding)

        # error checking for a file-like object `path` parameter
        if hasattr(path, "read"):
            f = path
        else:
            f = open(path, "r", encoding=encoding)  # type: ignore

        # add a `roam:` prefix for a pseudo-namespace to use here,
        # which applications may need to parameterize later?
        self.add_ns("roam", "https://roamresearch.com/ns/")

        uid_list: typing.List[str] = [
            self._walk_roam_graph(obj)
            for obj in json.load(f)  # type: ignore
            ]

        return uid_list
