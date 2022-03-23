# Reference: `kglab` package
<img src='../assets/nouns/api.png' alt='API by Adnen Kadri from the Noun Project' />
## [`KnowledgeGraph` class](#KnowledgeGraph)

This is the primary class used to represent RDF graphs, on which the other classes are dependent.
See <https://derwen.ai/docs/kgl/concepts/#knowledge-graph>

Core feature areas include:

  * namespace management (ontology, controlled vocabularies)
  * graph construction
  * serialization
  * SPARQL querying
  * SHACL validation
  * inference based on OWL-RL, RDFS, SKOS
    
---
#### [`__init__` method](#kglab.KnowledgeGraph.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L78)

```python
__init__(name="generic", base_uri=None, language="en", store=None, use_gpus=True, import_graph=None, namespaces=None)
```
Constructor for a `KnowledgeGraph` object.

  * `name` : `str`  
optional, internal name for this graph

  * `base_uri` : `str`  
the default [*base URI*](https://tools.ietf.org/html/rfc3986#section-5.1) for this RDF graph

  * `language` : `str`  
the default [*language tag*](https://www.w3.org/TR/rdf11-concepts/#dfn-language-tag), e.g., used for [*language indexing*](https://www.w3.org/TR/json-ld11/#language-indexing)

  * `store` : `str`  
optionally, string representing an `rdflib.Store` plugin to use.

  * `use_gpus` : `bool`  
optionally, use the NVidia GPU devices with [RAPIDS](https://rapids.ai/) if these libraries have been installed and the devices are available; defaults to `True`

  * `import_graph` : `typing.Union[rdflib.graph.ConjunctiveGraph, rdflib.graph.Dataset, rdflib.graph.Graph, NoneType]`  
optionally, another existing RDF graph to be used as a starting point

  * `namespaces` : `dict`  
a dictionary of [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) (dict values) and their corresponding *prefix* strings (dict keys) to add as *controlled vocabularies* which are available for use in the RDF graph, binding each prefix to the given namespace



---
#### [`build_blank_graph` method](#kglab.KnowledgeGraph.build_blank_graph)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L142)

```python
build_blank_graph()
```
Build a new `rdflib.Graph` object, based on storage plugin configuration.



---
#### [`rdf_graph` method](#kglab.KnowledgeGraph.rdf_graph)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L156)

```python
rdf_graph()
```
Accessor for the RDF graph.

  * *returns* : `rdflib.graph.Graph`  
the [`rdflib.Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=graph#graph) object



---
#### [`add_ns` method](#kglab.KnowledgeGraph.add_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L181)

```python
add_ns(prefix, iri, override=True, replace=False)
```
Adds another [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) among the *controlled vocabularies* available to use in the RDF graph, binding the `prefix` to the given namespace.

Since the RDFlib [`NamespaceManager`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.namespace.NamespaceManager) automagically converts all input bindings into [`URIRef`](https://www.w3.org/TR/rdf-concepts/#section-Graph-URIref) instead, we'll keep references to the namespaces – for later use.

  * `prefix` : `str`  
a [namespace prefix](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-prefix); it's recommended to confirm prefix usage (based on convention) by searching on <http://prefix.cc/>

  * `iri` : `str`  
URL to use for constructing the [namespace IRI](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-iri)

  * `override` : `bool`  
rebind, even if the given namespace is already bound with another prefix

  * `replace` : `bool`  
replace any existing prefix with the new namespace



---
#### [`get_ns` method](#kglab.KnowledgeGraph.get_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L225)

```python
get_ns(prefix)
```
Lookup a [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) among the *controlled vocabularies* available to use in the RDF graph.

  * `prefix` : `str`  
a [namespace prefix](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-prefix)

  * *returns* : `rdflib.namespace.Namespace`  
the RDFlib [`Namespace`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) for the *controlled vocabulary* referenced by `prefix`



---
#### [`get_ns_dict` method](#kglab.KnowledgeGraph.get_ns_dict)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L241)

```python
get_ns_dict()
```
Generate a dictionary of the *namespaces* used in this RDF graph.

  * *returns* : `dict`  
a `dict` describing the namespaces in this RDF graph



---
#### [`describe_ns` method](#kglab.KnowledgeGraph.describe_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L263)

```python
describe_ns()
```
Describe the *namespaces* used in this RDF graph.

  * *returns* : `pandas.core.frame.DataFrame`  
a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) describing the namespaces in this RDF graph; uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled



---
#### [`get_context` method](#kglab.KnowledgeGraph.get_context)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L290)

```python
get_context()
```
Generates a [*JSON-LD context*](https://www.w3.org/TR/json-ld11/#the-context) used for
serializing the RDF graph as [JSON-LD](https://json-ld.org/).

  * *returns* : `dict`  
context needed for JSON-LD serialization



---
#### [`encode_date` method](#kglab.KnowledgeGraph.encode_date)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L309)

```python
encode_date(dt, tzinfos)
```
Helper method to ensure that an input `datetime` value has a timezone that can be interpreted by [`rdflib.XSD.dateTime`](https://www.w3.org/TR/xmlschema-2/#dateTime).

  * `dt` : `str`  
input datetime as a string

  * `tzinfos` : `dict`  
timezones as a dict, used by

  * *returns* : `rdflib.term.Literal`  
[`rdflib.Literal`](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#literals) formatted as an XML Schema 2 `dateTime` value



---
#### [`add` method](#kglab.KnowledgeGraph.add)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L331)

```python
add(s, p, o)
```
Wrapper for [`rdflib.Graph.add()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=add#rdflib.Graph.add) to add a relation *(subject, predicate, object)* to the RDF graph, if it doesn't already exist.
Uses the RDF Graph as its context.

To prepare for upcoming **kglab** features, **this is the preferred method for adding relations to an RDF graph.**

  * `s` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*subject* node;

  * `p` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*predicate* relation;

  * `o` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*object* node;



---
#### [`remove` method](#kglab.KnowledgeGraph.remove)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L365)

```python
remove(s, p, o)
```
Wrapper for [`rdflib.Graph.remove()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=add#rdflib.Graph.remove) to remove a relation *(subject, predicate, object)* from the RDF graph, if it exist.
Uses the RDF Graph as its context.

To prepare for upcoming **kglab** features, **this is the preferred method for removing relations from an RDF graph.**

  * `s` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*subject* node;

  * `p` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*predicate* relation;

  * `o` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*object* node;



---
#### [`load_rdf` method](#kglab.KnowledgeGraph.load_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/decorators.py#L61)

```python
load_rdf(path, format="ttl", base=None, **args)
```
Wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from the `path` source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.
Throws `TypeError` whenever a format parser plugin encounters a syntax error.

Note: this adds relations to an RDF graph, although it does not overwrite the existing RDF graph.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); otherwise this throws a `TypeError` exception

  * `format` : `str`  
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

  * `base` : `str`  
logical URI to use as the document base; if not specified, the document location gets used

  * *returns* : `KnowledgeGraph`  
this `KnowledgeGraph` object – used for method chaining



---
#### [`load_rdf_text` method](#kglab.KnowledgeGraph.load_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L559)

```python
load_rdf_text(data, format="ttl", base=None, **args)
```
Wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from a text.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

  * `data` : `typing.AnyStr`  
text representation of RDF graph data

  * `format` : `str`  
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

  * `base` : `str`  
logical URI to use as the document base; if not specified, the document location gets used

  * *returns* : `KnowledgeGraph`  
this `KnowledgeGraph` object – used for method chaining



---
#### [`save_rdf` method](#kglab.KnowledgeGraph.save_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L602)

```python
save_rdf(path, format="ttl", base=None, encoding="utf-8", **args)
```
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination.
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

  * `format` : `str`  
serialization format, which defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

  * `base` : `str`  
optional base set for the graph

  * `encoding` : `str`  
optional text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception



---
#### [`save_rdf_text` method](#kglab.KnowledgeGraph.save_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L667)

```python
save_rdf_text(format="ttl", base=None, encoding="utf-8", **args)
```
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to a string.

  * `format` : `str`  
serialization format, which defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins; otherwise this throws a `TypeError` exception

  * `base` : `str`  
optional base set for the graph

  * `encoding` : `str`  
optional text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

  * *returns* : `typing.AnyStr`  
text representing the RDF graph



---
#### [`load_jsonld` method](#kglab.KnowledgeGraph.load_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/decorators.py#L61)

```python
load_jsonld(path, encoding="utf-8", **args)
```
Wrapper for [`rdflib-jsonld.parser.JsonLDParser.parse()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/parser.py) which parses an RDF graph from a [JSON-LD](https://json-ld.org/) source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

  * `encoding` : `str`  
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

  * *returns* : `KnowledgeGraph`  
this `KnowledgeGraph` object – used for method chaining



---
#### [`save_jsonld` method](#kglab.KnowledgeGraph.save_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L754)

```python
save_jsonld(path, encoding="utf-8", **args)
```
Wrapper for [`rdflib-jsonld.serializer.JsonLDSerializer.serialize()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/serializer.py) which serializes the RDF graph to the `path` destination as [JSON-LD](https://json-ld.org/).
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

  * `encoding` : `str`  
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception



---
#### [`load_parquet` method](#kglab.KnowledgeGraph.load_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/decorators.py#L61)

```python
load_parquet(path, **kwargs)
```
Wrapper for [`pandas.read_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html?highlight=read_parquet#pandas.read_parquet) which parses an RDF graph represented as a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.
Uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled.

To prepare for upcoming **kglab** features, **this is the preferred method for deserializing an RDF graph.**

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; a file URL can also be a path to a directory that contains multiple partitioned files, including a bucket in cloud storage – based on [`fsspec`](https://github.com/intake/filesystem_spec)

  * *returns* : `KnowledgeGraph`  
this `KnowledgeGraph` object – used for method chaining



---
#### [`save_parquet` method](#kglab.KnowledgeGraph.save_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L843)

```python
save_parquet(path, compression="snappy", storage_options=None, **kwargs)
```
Wrapper for [`pandas.to_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html?highlight=to_parquet) which serializes an RDF graph to a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.
Uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled.

To prepare for upcoming **kglab** features, **this is the preferred method for serializing an RDF graph.**

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str), path object to a local file reference, or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; accessing cloud storage is based on [`fsspec`](https://github.com/intake/filesystem_spec)

  * `compression` : `str`  
name of the compression algorithm to use; defaults to `"snappy"`; can also be `"gzip"`, `"brotli"`, or `None` for no compression

  * `storage_options` : `dict`  
extra options parsed by [`fsspec`](https://github.com/intake/filesystem_spec) for cloud storage access; **NOT USED** until `pandas` 1.2.x becomes stable across platforms and also RAPIDS provides support



---
#### [`load_csv` method](#kglab.KnowledgeGraph.load_csv)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L888)

```python
load_csv(url)
```
Wrapper for [`csvwlib`](https://github.com/DerwenAI/csvwlib) which parses a CSV file from the `path` source, then converts to RDF and merges into this RDF graph.

  * `url` : `str`  
must be a URL represented as a string

  * *returns* : `KnowledgeGraph`  
this `KnowledgeGraph` object – used for method chaining



---
#### [`materialize` method](#kglab.KnowledgeGraph.materialize)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L909)

```python
materialize(config)
```
Binding to the morph-kgc `materialize()` method.

  * `config` : `str`  
morph-kgc configuration, it can be the path to the config file, or a string with the config; see <https://github.com/oeg-upm/Morph-KGC/wiki/Usage#library>

  * *returns* : `KnowledgeGraph`  
this `KnowledgeGraph` object – used for method chaining



---
#### [`import_roam` method](#kglab.KnowledgeGraph.import_roam)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/decorators.py#L61)

```python
import_roam(path, encoding="utf-8")
```
Import a graph in JSON that has been exported from the [Roam Research](https://roamresearch.com/) note-taking tool, then convert its objects and attributes into RDF representation.

For more details about the exported data from Roam Research, see:

  * <https://roamstack.com/roam-data-outside-roam/>
  * <https://nesslabs.com/roam-research-input-output>
  * <https://davidbieber.com/snippets/2020-04-25-roam-json-export/>

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) to a local file reference – possibly a glob with a wildcard; or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

  * `encoding` : `str`  
optional text encoding value, which defaults to `"utf-8"`; must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

  * *returns* : `typing.List[str]`  
a list of identifiers for the top-level nodes added from the Roam Research graph



---
#### [`query` method](#kglab.KnowledgeGraph.query)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1039)

```python
query(sparql, bindings=None)
```
Wrapper for [`rdflib.Graph.query()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=query#rdflib.Graph.query) to perform a SPARQL query on the RDF graph.

  * `sparql` : `str`  
text for the SPARQL query

  * `bindings` : `dict`  
initial variable bindings

  * *yields* :  
[`rdflib.query.ResultRow`](https://rdflib.readthedocs.io/en/stable/_modules/rdflib/query.html?highlight=ResultRow#) named tuples, to iterate through the query result set



---
#### [`query_as_df` method](#kglab.KnowledgeGraph.query_as_df)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1067)

```python
query_as_df(sparql, bindings=None, simplify=True, pythonify=True)
```
Wrapper for [`rdflib.Graph.query()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=query#rdflib.Graph.query) to perform a SPARQL query on the RDF graph.

  * `sparql` : `str`  
text for the SPARQL query

  * `bindings` : `dict`  
initial variable bindings

  * `simplify` : `bool`  
convert terms in each row of the result set into a readable representation for each term, using N3 format

  * `pythonify` : `bool`  
convert instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

  * *returns* : `pandas.core.frame.DataFrame`  
the query result set represented as a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html); uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled



---
#### [`visualize_query` method](#kglab.KnowledgeGraph.visualize_query)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1111)

```python
visualize_query(sparql, notebook=False)
```
Visualize the given SPARQL query as a [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network)

  * `sparql` : `str`  
input SPARQL query to be visualized

  * `notebook` : `bool`  
optional boolean flag, whether to initialize the PyVis graph to render within a notebook; defaults to `False`

  * *returns* : `pyvis.network.Network`  
PyVis network object, to be rendered



---
#### [`n3fy` method](#kglab.KnowledgeGraph.n3fy)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1132)

```python
n3fy(node, pythonify=True)
```
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize a node into a human-readable representation using N3 format.

  * `node` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

  * `pythonify` : `bool`  
flag to force instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

  * *returns* : `typing.Any`  
text (or Python objects) for the serialized node



---
#### [`n3fy_row` method](#kglab.KnowledgeGraph.n3fy_row)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1158)

```python
n3fy_row(row_dict, pythonify=True)
```
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize one row of a result set from a SPARQL query into a human-readable representation for each term using N3 format.

  * `row_dict` : `dict`  
one row of a SPARQL query results, as a `dict`

  * `pythonify` : `bool`  
flag to force instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

  * *returns* : `dict`  
a dictionary of serialized row bindings



---
#### [`unbind_sparql` classmethod](#kglab.KnowledgeGraph.unbind_sparql)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1184)

```python
unbind_sparql(sparql, bindings, preamble="")
```
Substitute the _binding variables_ into the text of a SPARQL query,
to obviate the need for binding variables specified separately.
This can be helpful for debugging, or for some query engines that
may not have full SPARQL support yet.

  * `sparql` : `str`  
text for the SPARQL query

  * `bindings` : `dict`  
variable bindings

  * *returns* : `str`  
a string of the expanded SPARQL query



---
#### [`validate` method](#kglab.KnowledgeGraph.validate)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1220)

```python
validate(shacl_graph=None, shacl_graph_format=None, ont_graph=None, ont_graph_format=None, advanced=False, inference=None, inplace=True, abort_on_first=None, **kwargs)
```
Wrapper for [`pyshacl.validate()`](https://github.com/RDFLib/pySHACL) for validating the RDF graph using rules expressed in the [SHACL](https://www.w3.org/TR/shacl/) (Shapes Constraint Language).

  * `shacl_graph` : `typing.Union[rdflib.graph.ConjunctiveGraph, rdflib.graph.Dataset, rdflib.graph.Graph, ~AnyStr, NoneType]`  
text representation, file path, or URL of the SHACL *shapes graph* to use in validation

  * `shacl_graph_format` : `typing.Union[str, NoneType]`  
RDF format, if the `shacl_graph` parameter is a text representation of the *shapes graph*

  * `ont_graph` : `typing.Union[rdflib.graph.ConjunctiveGraph, rdflib.graph.Dataset, rdflib.graph.Graph, ~AnyStr, NoneType]`  
text representation, file path, or URL of an optional, extra ontology to mix into the RDF graph
ont_graph_format
RDF format, if the `ont_graph` parameter is a text representation of the extra ontology

  * `advanced` : `typing.Union[bool, NoneType]`  
enable advanced SHACL features

  * `inference` : `typing.Union[str, NoneType]`  
prior to validation, run OWL2 RL profile-based expansion of the RDF graph based on [OWL-RL](https://github.com/RDFLib/OWL-RL); values: `"rdfs"`, `"owlrl"`, `"both"`, `None`

  * `inplace` : `typing.Union[bool, NoneType]`  
when enabled, do not clone the RDF graph prior to inference/expansion, just manipulate it in-place

  * `abort_on_first` : `typing.Union[bool, NoneType]`  
abort validation on the first error

  * *returns* : `typing.Tuple[bool, KnowledgeGraph, str]`  
a tuple of `conforms` (RDF graph passes the validation rules) + `report_graph` (report as a `KnowledgeGraph` object) + `report_text` (report formatted as text)



---
#### [`infer_owlrl_closure` method](#kglab.KnowledgeGraph.infer_owlrl_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1298)

```python
infer_owlrl_closure()
```
Infer deductive closure for [OWL 2 RL semantics](https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules) based on [OWL-RL](https://owl-rl.readthedocs.io/en/latest/stubs/owlrl.html#module-owlrl)

See <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>



---
#### [`infer_rdfs_closure` method](#kglab.KnowledgeGraph.infer_rdfs_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1311)

```python
infer_rdfs_closure()
```
Infer deductive closure for [RDFS semantics](https://www.w3.org/TR/rdf-mt/) based on [OWL-RL](https://owl-rl.readthedocs.io/en/latest/stubs/owlrl.html#module-owlrl)

See <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>



---
#### [`infer_rdfs_properties` method](#kglab.KnowledgeGraph.infer_rdfs_properties)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1324)

```python
infer_rdfs_properties()
```
Perform RDFS sub-property inference, adding super-properties where sub-properties have been used.

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



---
#### [`infer_rdfs_classes` method](#kglab.KnowledgeGraph.infer_rdfs_classes)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1352)

```python
infer_rdfs_classes()
```
Perform RDFS subclass inference, marking all resources having a subclass type with their superclass.

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



---
#### [`infer_skos_related` method](#kglab.KnowledgeGraph.infer_skos_related)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1385)

```python
infer_skos_related()
```
Infer OWL symmetry (both directions) for `skos:related`
[(*S23*)](https://www.w3.org/TR/skos-reference/#S23)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



---
#### [`infer_skos_concept` method](#kglab.KnowledgeGraph.infer_skos_concept)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1400)

```python
infer_skos_concept()
```
Infer `skos:topConceptOf` as a sub-property of `skos:inScheme`
[(*S7*)](https://www.w3.org/TR/skos-reference/#S7)

Infer `skos:topConceptOf` as `owl:inverseOf` the property `skos:hasTopConcept`
[(*S8*)](https://www.w3.org/TR/skos-reference/#S8)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



---
#### [`infer_skos_hierarchical` method](#kglab.KnowledgeGraph.infer_skos_hierarchical)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1424)

```python
infer_skos_hierarchical(narrower=True)
```
Infer `skos:narrower` as `owl:inverseOf` the property `skos:broader`; although only keep `skos:narrower` on request
[(*S25*)](https://www.w3.org/TR/skos-reference/#S25)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

  * `narrower` : `bool`  
if false, `skos:narrower` will be removed instead of added



---
#### [`infer_skos_transitive` method](#kglab.KnowledgeGraph.infer_skos_transitive)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1451)

```python
infer_skos_transitive(narrower=True)
```
Infer transitive closure,
`skos:broader` as a sub-property of `skos:broaderTransitive`, and `skos:narrower` as a sub-property of `skos:narrowerTransitive`
[(*S22*)](https://www.w3.org/TR/skos-reference/#S22)

Infer `skos:broaderTransitive` and `skos:narrowerTransitive` (on request only) as instances of `owl:TransitiveProperty`
[(*S24*)](https://www.w3.org/TR/skos-reference/#S24)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

  * `narrower` : `bool`  
also infer transitive closure for `skos:narrowerTransitive`



---
#### [`infer_skos_symmetric_mappings` method](#kglab.KnowledgeGraph.infer_skos_symmetric_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1480)

```python
infer_skos_symmetric_mappings(related=True)
```
Infer symmetric mapping properties (`skos:relatedMatch`, `skos:closeMatch`, `skos:exactMatch`) as instances of `owl:SymmetricProperty`
[(*S44*)](https://www.w3.org/TR/skos-reference/#S44)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

  * `related` : `bool`  
infer the `skos:related` super-property for all `skos:relatedMatch` relations



---
#### [`infer_skos_hierarchical_mappings` method](#kglab.KnowledgeGraph.infer_skos_hierarchical_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1511)

```python
infer_skos_hierarchical_mappings(narrower=True)
```
Infer `skos:narrowMatch` as `owl:inverseOf` the property `skos:broadMatch`
[(*S43*)](https://www.w3.org/TR/skos-reference/#S43)

Infer the `skos:related` super-property for all `skos:relatedMatch` relations
[(*S41*)](https://www.w3.org/TR/skos-reference/#S41)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

  * `narrower` : `bool`  
if false, `skos:narrowMatch` will be removed instead of added



## [`Subgraph` class](#Subgraph)

Base class for projection of an RDF graph into an *algebraic object* such as a *vector*, *matrix*, or *tensor* representation, to support integration with non-RDF graph libraries.
In other words, this class provides means to vectorize selected portions of a graph as a [*dimension*](https://mathworld.wolfram.com/Dimension.html).
See <https://derwen.ai/docs/kgl/concepts/#subgraph>

Features support several areas of use cases, including:

  * label encoding
  * vectorization (parallel processing)
  * graph algorithms
  * visualization
  * embedding (deep learning)
  * probabilistic graph inference (statistical relational learning)

The base case is where a *subset* of the nodes in the source RDF graph get represented as a *vector*, in the `node_vector` member.
This provides an efficient *index* on a constructed *dimension*, solely for the context of a specific use case.
    
---
#### [`__init__` method](#kglab.Subgraph.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L47)

```python
__init__(kg, preload=None)
```
Constructor for creating and manipulating a *subgraph* as a [*vector*](https://mathworld.wolfram.com/Vector.html),
projecting from an RDF graph represented by a `KnowledgeGraph` object.

  * `kg` : `kglab.kglab.KnowledgeGraph`  
the source RDF graph

  * `preload` : `list`  
an optional, pre-determined list to pre-load for *label encoding*



---
#### [`transform` method](#kglab.Subgraph.transform)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L71)

```python
transform(node)
```
Transforms a node in an RDF graph to an integer value, as a unique identifier with the closure of a specific use case.
The integer value can then be used to index into an *algebraic object* such as a *matrix* or *tensor*.
Effectvely, this method is similar to a [`sklearn.preprocessing.LabelEncoder`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html).

Notes:

  * the integer value is **not** a [*uuid*](https://tools.ietf.org/html/rfc4122) since it is only defined within the closure of a specific use case.
  * a special value `-1` represents the unique identifier for a non-existent (`None`) node, which is useful in data structures that have optional placeholders for links to RDF nodes

  * `node` : `typing.Union[str, NoneType, rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
a node in the RDF graph

  * *returns* : `int`  
a unique identifier (an integer index) for the `node` in the RDF graph



---
#### [`inverse_transform` method](#kglab.Subgraph.inverse_transform)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L108)

```python
inverse_transform(id)
```
Inverse transform from an intenger to a node in the RDF graph, using the identifier as an index into the node vector.

  * `id` : `int`  
an integer index for the `node` in the RDF graph

  * *returns* : `typing.Union[str, NoneType, rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
node in the RDF graph



---
#### [`n3fy` method](#kglab.Subgraph.n3fy)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L127)

```python
n3fy(node)
```
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to serialize a node into a human-readable representation using N3 format.
This method provides a convenience, which in turn calls `KnowledgeGraph.n3fy()`

  * `node` : `typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

  * *returns* : `typing.Any`  
text (or Python object) for the serialized node



## [`SubgraphMatrix` class](#SubgraphMatrix)

Projection of a RDF graph to a [*matrix*](https://mathworld.wolfram.com/AdjacencyMatrix.html) representation.
Typical use cases include integration with non-RDF graph libraries for *graph algorithms*.
    
---
#### [`__init__` method](#kglab.SubgraphMatrix.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L151)

```python
__init__(kg, sparql, bindings=None, src_dst=None)
```
Constructor for creating and manipulating a *subgraph* as a [*matrix*](https://mathworld.wolfram.com/AdjacencyMatrix.html),
projecting from an RDF graph represented by a `KnowledgeGraph` object.

  * `kg` : `kglab.kglab.KnowledgeGraph`  
the source RDF graph

  * `sparql` : `str`  
text for a SPARQL query that yields pairs to project into the *subgraph*; by default this expects the query to return bindings for `subject` and `object` nodes in the RDF graph

  * `bindings` : `dict`  
initial variable bindings

  * `src_dst` : `typing.List[str]`  
an optional map to override the  `subject` and `object` bindings expected in the SPARQL query results; defaults to `None`



---
#### [`build_df` method](#kglab.SubgraphMatrix.build_df)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L185)

```python
build_df(show_symbols=False)
```
Factory pattern to populate a [`pandas.DataFrame`](https://pandas.pydata.org/docs/reference/frame.html) object, using transforms in this subgraph.

Note: this method is primarily intended for [`cuGraph`](https://docs.rapids.ai/api/cugraph/stable/) support. Loading via a `DataFrame` is required – in lieu of using the `nx.add_node()` approach.
Therefore the support for representing *bipartite* graphs is still pending.

  * `show_symbols` : `bool`  
optionally, include the symbolic representation for each node; defaults to `False`

  * *returns* : `pandas.core.frame.DataFrame`  
the populated `DataFrame` object; uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled



---
#### [`build_nx_graph` method](#kglab.SubgraphMatrix.build_nx_graph)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L234)

```python
build_nx_graph(nx_graph, bipartite=False)
```
Factory pattern to populate a [`networkx.DiGraph`](https://networkx.org/documentation/latest/reference/classes/digraph.html) object, using transforms in this subgraph.
See <https://networkx.org/>

  * `nx_graph` : `networkx.classes.digraph.DiGraph`  
pass in an unpopulated [`networkx.DiGraph`](https://networkx.org/documentation/latest/reference/classes/digraph.html) object; must be a [`cugraph.DiGraph`](https://docs.rapids.ai/api/cugraph/stable/api.html#digraph) if GPUs are enabled

  * `bipartite` : `bool`  
flag for whether the `(subject, object)` pairs should be partitioned into *bipartite sets*, in other words whether the *adjacency matrix* is symmetric; ignored if GPUs are enabled

  * *returns* : `networkx.classes.digraph.DiGraph`  
the populated `NetworkX` graph object; uses the [RAPIDS `cuGraph` library](https://docs.rapids.ai/api/cugraph/stable/) if GPUs are enabled



---
#### [`build_ig_graph` method](#kglab.SubgraphMatrix.build_ig_graph)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L276)

```python
build_ig_graph(ig_graph)
```
Factory pattern to populate an [`igraph.Graph`](https://igraph.org/python/doc/igraph.Graph-class.html) object, using transforms in this subgraph.
See <https://igraph.org/python/doc/>

Note that `iGraph` is somewhat notorious for being quite difficult to install correctly across a wide range of different platforms and environments.
Consequently this has been removed from being a dependency for `kglab`; to use `iGraph` please install and import it separately.

  * `ig_graph` : `typing.Any`  
pass in an unpopulated [`igraph.Graph`](https://igraph.org/python/doc/igraph.Graph-class.html) object

  * *returns* : `typing.Any`  
the populated  `iGraph` graph object



## [`SubgraphTensor` class](#SubgraphTensor)

Projection of a RDF graph to a [*tensor*](https://mathworld.wolfram.com/Tensor.html) representation.
Typical use cases include integration with non-RDF graph libraries for *visualization* and *embedding*.
    
---
#### [`__init__` method](#kglab.SubgraphTensor.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L314)

```python
__init__(kg, excludes=None)
```
Constructor for creating and manipulating a *subgraph* as a [*tensor*](https://mathworld.wolfram.com/Tensor.html),
projecting from an RDF graph represented by a `KnowledgeGraph` object.

  * `kg` : `kglab.kglab.KnowledgeGraph`  
the source RDF graph

  * `excludes` : `list`  
a list of RDF predicates to exclude from projection into the *subgraph*



---
#### [`as_tuples` method](#kglab.SubgraphTensor.as_tuples)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L338)

```python
as_tuples()
```
Iterator for enumerating the RDF triples to be included in the subgraph, used in factory patterns for visualizations.
This allows a kind of *lazy evaluation*.

  * *yields* :  
the RDF triples within the subgraph



---
#### [`as_tensor_edges` method](#kglab.SubgraphTensor.as_tensor_edges)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L353)

```python
as_tensor_edges()
```
Iterator for enumerating the edges connecting to each predicate in the
subgraph, to be used to represent the KG in `PyTorch`.

  * *yields* :  
a subject and object edge for each predicate, in tensor representation



---
#### [`as_tensor` method](#kglab.SubgraphTensor.as_tensor)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L377)

```python
as_tensor(quiet=True)
```
Represents the KG as an edge list where each predicate has edges
connecting to its subject and object.

This can be used to load a [`Tensor`](https://pytorch.org/docs/stable/tensors.html)
in PyTorch, for example:

```
edge_list = kg.as_tensor()
tensor = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
```

  * `quiet` : `bool`  
boolean flag to disable `tqdm` progress bar calculation and output

  * *returns* : `typing.List[typing.Tuple[int, int, int]]`  
an edge list for the loaded tensor object



---
#### [`pyvis_style_node` method](#kglab.SubgraphTensor.pyvis_style_node)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L416)

```python
pyvis_style_node(pyvis_graph, node_id, label, style=None)
```
Adds a node into a [PyVis](https://pyvis.readthedocs.io/) network, optionally with styling info.

  * `pyvis_graph` : `pyvis.network.Network`  
the [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html?highlight=network#pyvis.network.Network) being used for *interactive visualization*

  * `node_id` : `int`  
unique identifier for a node in the RDF graph

  * `label` : `str`  
text label for the node

  * `style` : `dict`  
optional style dictionary



---
#### [`build_pyvis_graph` method](#kglab.SubgraphTensor.build_pyvis_graph)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L460)

```python
build_pyvis_graph(notebook=False, style=None)
```
Factory pattern to create a [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html?highlight=network#pyvis.network.Network) object, populated by transforms in this subgraph.
See <https://pyvis.readthedocs.io/>

  * `notebook` : `bool`  
flag for whether or not the interactive visualization will be generated within a notebook

  * `style` : `dict`  
optional style dictionary

  * *returns* : `pyvis.network.Network`  
a `PyVis` network object



## [`Measure` class](#Measure)

This class measures an RDF graph.
Its downstream use cases include: graph size estimates; computation costs; constructed shapes.
See <https://derwen.ai/docs/kgl/concepts/#measure>

Core feature areas include:

  * descriptive statistics
  * topological analysis
    
---
#### [`__init__` method](#kglab.Measure.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L150)

```python
__init__(name="generic")
```
Constructor for this graph measure.

  * `name` : `str`  
optional name for this measure



---
#### [`reset` method](#kglab.Measure.reset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L167)

```python
reset()
```
Reset (reinitialize) all of the counts for different kinds of census, which include:

  * total nodes
  * total edges
  * count for each kind of *subject* (`Simplex0`)
  * count for each kind of *predicate* (`Simplex0`)
  * count for each kind of *object* (`Simplex0`)
  * count for each kind of *literal* (`Simplex0`)
  * item census (`Simplex1`)
  * dyad census (`Simplex1`)



---
#### [`get_node_count` method](#kglab.Measure.get_node_count)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L192)

```python
get_node_count()
```
Accessor for the node count.

  * *returns* : `int`  
value of `node_count`



---
#### [`get_edge_count` method](#kglab.Measure.get_edge_count)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L204)

```python
get_edge_count()
```
Accessor for the edge count.

  * *returns* : `int`  
value of `edge_count`



---
#### [`measure_graph` method](#kglab.Measure.measure_graph)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L216)

```python
measure_graph(kg)
```
Run a full measure of the given RDF graph.

  * `kg` : `kglab.kglab.KnowledgeGraph`  
`KnowledgeGraph` object representing the RDF graph to be measured



---
#### [`get_keyset` method](#kglab.Measure.get_keyset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L241)

```python
get_keyset(incl_pred=True)
```
Accessor for the set of items (domain: nodes, predicates, labels, URLs, literals, etc.) that were measured.
Used for *label encoding* in the transform between an RDF graph and a matrix or tensor representation.

  * `incl_pred` : `bool`  
flag to include the predicates in the set of keys to be encoded

  * *returns* : `typing.List[str]`  
sorted list of keys to be used in the encoding



## [`Simplex0` class](#Simplex0)

Count the distribution of a class of items in an RDF graph.
In other words, tally an "item census" – to be consistent with the usage of that term.
    
---
#### [`__init__` method](#kglab.Simplex0.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L25)

```python
__init__(name="generic")
```
Constructor for an item census.

  * `name` : `str`  
optional name for this measure



---
#### [`increment` method](#kglab.Simplex0.increment)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L40)

```python
increment(item0)
```
Increment the count for this item.

  * `item0` : `typing.Union[str, rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
an item (domain: node, predicate, label, URL, literal, etc.) to be counted



---
#### [`get_tally` method](#kglab.Simplex0.get_tally)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L53)

```python
get_tally()
```
Accessor for the item counts.

  * *returns* : `typing.Union[pandas.core.frame.DataFrame, NoneType]`  
a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with the count distribution, sorted in ascending order



---
#### [`get_keyset` method](#kglab.Simplex0.get_keyset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L70)

```python
get_keyset()
```
Accessor for the set of items (domain) counted.

  * *returns* : `set`  
set of keys for the items (domain: nodes, predicates, labels, URLs, literals, etc.) that were counted



## [`Simplex1` class](#Simplex1)

Measure a dyad census in an RDF graph, i.e., count the relations (directed edges) which connect two nodes.
    
---
#### [`__init__` method](#kglab.Simplex1.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L87)

```python
__init__(name="generic")
```
Constructor for a dyad census.

  * `name` : `str`  
optional name for this measure



---
#### [`increment` method](#kglab.Simplex1.increment)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L101)

```python
increment(item0, item1)
```
Increment the count for a dyad represented by the two given items.

  * `item0` : `typing.Union[str, rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
"source" item (domain: node, label, URL, etc.) to be counted

  * `item1` : `typing.Union[str, rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
"sink" item (range: node, label, literal, URL, etc.) to be counted



---
#### [`get_tally_map` method](#kglab.Simplex1.get_tally_map)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L119)

```python
get_tally_map()
```
Accessor for the dyads census.

  * *returns* : `typing.Tuple[pandas.core.frame.DataFrame, dict]`  
a tuple of a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with the count distribution, sorted in ascending order; and a map of the observed links between "source" and "sink" items



## [`PSLModel` class](#PSLModel)

Class representing a
[*probabilistic soft logic*](../glossary/#probabilistic-soft-logic)
(PSL) model.

For PSL-specific terminology used here, see <https://psl.linqs.org/wiki/master/Glossary.html>

Note: You need to have a Java JDK installed to run PSL.
    
---
#### [`__init__` method](#kglab.PSLModel.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L42)

```python
__init__(name=None)
```
Wrapper for constructing a [`pslpython.model.Model`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/model.py).

  * `name` : `str`  
optional name of the PSL model; if not supplied, PSL generates a random name



---
#### [`clear_model` method](#kglab.PSLModel.clear_model)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L57)

```python
clear_model()
```
Clear any pre-existing data from each of the predicates, to initialize the model.

  * *returns* : `PSLModel`  
this PSL model – use for method chaining



---
#### [`add_predicate` method](#kglab.PSLModel.add_predicate)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L72)

```python
add_predicate(raw_name, size=None, closed=False, arg_types=None)
```
Add a [`pslpython.predicate.Predicate`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/predicate.py) to this model.
Enough details must be supplied for PSL to infer the number and types of each predicate's arguments.

  * `raw_name` : `str`  
name of the predicate; must be unique among all of the predicates

  * `size` : `int`  
optional, the number of arguments for this predicate

  * `closed` : `bool`  
indicates that this predicate is fully observed, i.e., all substitutions of this predicate have known values and will behave as evidence for inference; otherwise, if `False` then infer some values of this predicate; defaults to `False`

  * `arg_types` : `typing.List`  
optional, a list of types for the arguments for this predicate; all arguments will default to string

  * *returns* : `PSLModel`  
this PSL model – use for method chaining



---
#### [`add_rule` method](#kglab.PSLModel.add_rule)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L110)

```python
add_rule(rule_string, weighted=None, weight=None, squared=None)
```
Add a [`pslpython.rule.Rule`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/rule.py) to this model.

  * a weighted rule can change its weight or squared status
  * a weighted rule cannot convert into an unweighted rule nor visa-versa
  * unweighted rules are [*constraints*](https://psl.linqs.org/wiki/master/Constraints.html)

For more details, see <https://psl.linqs.org/wiki/master/Rule-Specification.html>

  * `rule_string` : `str`  
text representation for specifying the rule

  * `weighted` : `bool`  
indicates that this rule is weighted

  * `weight` : `float`  
weight of this rule

  * `squared` : `bool`  
indicates that this rule's potential is squared

  * *returns* : `PSLModel`  
this PSL model – use for method chaining



---
#### [`add_data_row` method](#kglab.PSLModel.add_data_row)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L223)

```python
add_data_row(predicate_name, args, partition="observations", truth_value=1.0, verbose=False)
```
Add a single record to a specified predicate, within a specified partition.

  * `predicate_name` : `str`  
name of the specific predicate; name normalization will be handled internally; raises `ModelError` if the predicate name is not found

  * `args` : `list`  
arguments for the record being added, as a list

  * `partition` : `str`  
label for the [`pslpython.partition.Partition`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/partition.py) into which the `data` gets added; must be among `[ "observations", "targets", "truth" ]`; defaults to `"observations"`; see <https://psl.linqs.org/wiki/master/Data-Storage-in-PSL.html>

  * `truth_value` : `float`  
optional truth value of the record being added

  * `verbose` : `bool`  
flag for verbose trace of each added record

  * *returns* : `PSLModel`  
this PSL model – use for method chaining



---
#### [`trace_predicate` method](#kglab.PSLModel.trace_predicate)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L267)

```python
trace_predicate(predicate_name, partition="observations", path=None)
```
Construct a trace of the data in a specified predicate, within a specified partition, formatted as a dataframe.
Use a consistent column naming and sort order, so that these values can be used later in testing.
Optionally write out this out to a TSV file.

  * `predicate_name` : `str`  
name of the specific predicate; name normalization will be handled internally; raises `ModelError` if the predicate name is not found

  * `partition` : `str`  
label for the [`pslpython.partition.Partition`](https://github.com/linqs/psl/blob/master/psl-python/pslpython/partition.py) into which the `data` gets added; must be among `[ "observations", "targets", "truth" ]`; defaults to `"observations"`; see <https://psl.linqs.org/wiki/master/Data-Storage-in-PSL.html>

  * `path` : `pathlib.Path`  
optional output path for the TSV file; defaults to `None`

  * *returns* : `pandas.core.frame.DataFrame`  
dataframe representing the traced partition data



---
#### [`compare_predicate` classmethod](#kglab.PSLModel.compare_predicate)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L304)

```python
compare_predicate(df, trace_path)
```
Compare the values of a predict with its expected values which get loaded from a file.
This will print any expected (missing) or error (mismatched) rows.

  * `df` : `pandas.core.frame.DataFrame`  
dataframe from `trace_predicate`

  * `trace_path` : `pathlib.Path`  
path to a TSV file of expected values, saved from the trace of a baseline run

  * *returns* : `pandas.core.frame.DataFrame`  
dataframe loaded from the expected values



---
#### [`infer` method](#kglab.PSLModel.infer)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L342)

```python
infer(method="", cli_options=None, psl_config=None, jvm_options=None)
```
Run inference on this model, storing the inferred results in an internal dataframe.

  * `method` : `str`  
the inference method to use

  * `cli_options` : `list`  
additional options to pass to PSL, based on its CLI options; see <https://psl.linqs.org/wiki/master/Configuration.html>

  * `psl_config` : `dict`  
configuration options passed directly to the PSL core code; see <https://psl.linqs.org/wiki/master/Configuration-Options.html>

  * `jvm_options` : `list`  
options passed to the JVM running the PSL Java library; most commonly `"-Xmx"` and `"-Xms"`



---
#### [`get_results` method](#kglab.PSLModel.get_results)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/srl.py#L382)

```python
get_results(predicate_name)
```
Accessor for the inferred results for a specified predicate.

  * `predicate_name` : `str`  
name of the specific predicate; name normalization will be handled internally; raises `ModelError` if the predicate name is not found

  * *returns* : `pandas.core.frame.DataFrame`  
inferred values as a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html), with columns names for each argument plus the `"truth"` value



## [`GPViz` class](#GPViz)

Class used to Visualize the graph pattern of a SPARQL query.
This source comes from <https://github.com/pebbie/sparqlgpviz>
modified to limit its dependencies to RDFlib and PyVis.

by Peb Ruswono Aryan <https://github.com/pebbie>
    
---
#### [`__init__` method](#kglab.GPViz.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/gpviz.py#L61)

```python
__init__(sparql, namespaces)
```
Constructor for GPViz, to visualize the given SPARQL query as a [`pyvis.network.Network`](https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network)

  * `sparql` : `str`  
input SPARQL query to be visualized

  * `namespaces` : `typing.Dict[str, str]`  
the namespaces for the corresponding RDF graph



---
#### [`visualize_query` method](#kglab.GPViz.visualize_query)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/gpviz.py#L360)

```python
visualize_query(notebook=False)
```
Visualize the SPARQL query as a PyVis network.

  * *returns* : `pyvis.network.Network`  
PyVis graph to be rendered



---
## [module functions](#kglab)
---
#### [`calc_quantile_bins` function](#kglab.calc_quantile_bins)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L51)

```python
calc_quantile_bins(num_rows)
```
Calculate the bins to use for a quantile stripe, using [`numpy.linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)

  * `num_rows` : `int`  
number of rows in the target dataframe

  * *returns* : `numpy.ndarray`  
the calculated bins, as a [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)



---
#### [`get_gpu_count` function](#kglab.get_gpu_count)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L17)

```python
get_gpu_count()
```
Special handling for detecting GPU availability: an approach
recommended by the NVidia RAPIDS engineering team, since `nvml`
bindings are difficult for Python libraries to keep updated.

  * *returns* : `int`  
count of available GPUs, where `0` means none or disabled.



---
#### [`import_from_neo4j` function](#kglab.import_from_neo4j)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/external_import.py#L19)

```python
import_from_neo4j(username, password, dbname, host="localhost", port="7474")
```
Wrapper for a
[`Cypher`](https://neo4j.com/labs/neosemantics/tutorial/#_using_the_cypher_n10s_rdf_export_procedure)
export request, to provide neo4j integration through the
[`neosemantics`](https://neo4j.com/labs/neosemantics/) library.

Tested with ~10GB of stored triples.

  * `username` : `str`  
the user name, as a string

  * `password` : `str`  
the password, as a string

  * `dbname` : `str`  
the database name, as a string

  * `host` : `str`  
optionally, the neo4j server domain name or IP address, as a string – including the protocol scheme; defaults to `"http://localhost"`

  * `port` : `str`  
optionally, the neo4j server port; defaults to `"7474"`

  * *returns* : `rdflib.graph.Graph`  
an [`rdflib.Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=graph#graph) object parsed from the exported RDF



---
#### [`root_mean_square` function](#kglab.root_mean_square)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L104)

```python
root_mean_square(values)
```
Calculate the [*root mean square*](https://mathworld.wolfram.com/Root-Mean-Square.html) of the values in the given list.

  * `values` : `list`  
list of values to use in the RMS calculation

  * *returns* : `float`  
RMS metric as a float



---
#### [`stripe_column` function](#kglab.stripe_column)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L67)

```python
stripe_column(values, bins, use_gpus=False)
```
Stripe a column in a dataframe, by interpolating quantiles into a set of discrete indexes.

  * `values` : `list`  
list of values to stripe

  * `bins` : `int`  
quantile bins; see [`calc_quantile_bins()`](#calc_quantile_bins-function)

  * `use_gpus` : `bool`  
optionally, use the NVidia GPU devices with the [RAPIDS libraries](https://rapids.ai/) if these libraries have been installed and the devices are available; defaults to `False`

  * *returns* : `numpy.ndarray`  
the striped column values, as a [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html); uses the [RAPIDS `cuDF` library](https://docs.rapids.ai/api/cudf/stable/) if GPUs are enabled



---
## [module types](#kglab)
#### [`Census_Dyad_Tally` type](#kglab.Census_Dyad_Tally)
```python
Census_Dyad_Tally = typing.Tuple[pandas.core.frame.DataFrame, dict]
```

#### [`Census_Item` type](#kglab.Census_Item)
```python
Census_Item = typing.Union[str, rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
```

#### [`EvoShapeBoard` type](#kglab.EvoShapeBoard)
```python
EvoShapeBoard = typing.List[typing.List[~Evolike]]
```

#### [`EvoShapeDistance` type](#kglab.EvoShapeDistance)
```python
EvoShapeDistance = typing.Tuple[int, int, float]
```

#### [`GraphLike` type](#kglab.GraphLike)
```python
GraphLike = typing.Union[rdflib.graph.ConjunctiveGraph, rdflib.graph.Dataset, rdflib.graph.Graph]
```

#### [`IOPathLike` type](#kglab.IOPathLike)
```python
IOPathLike = typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]
```

#### [`NodeLike` type](#kglab.NodeLike)
```python
NodeLike = typing.Union[str, NoneType, rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
```

#### [`PathLike` type](#kglab.PathLike)
```python
PathLike = typing.Union[str, pathlib.Path, urlpath.URL]
```

#### [`RDF_Node` type](#kglab.RDF_Node)
```python
RDF_Node = typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
```

#### [`RDF_Triple` type](#kglab.RDF_Triple)
```python
RDF_Triple = typing.Tuple[typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode], typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode], typing.Union[rdflib.term.Node, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]]
```

#### [`SPARQL_Bindings` type](#kglab.SPARQL_Bindings)
```python
SPARQL_Bindings = typing.Tuple[str, dict]
```

#### [`SerializedEvoShape` type](#kglab.SerializedEvoShape)
```python
SerializedEvoShape = typing.List[~Evolike]
```

