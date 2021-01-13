# Reference: `kglab` package
## [`KnowledgeGraph` class](#KnowledgeGraph)

This is the primary class used to represent an RDF graph, on which the other classes are dependent.
See <https://derwen.ai/docs/kgl/concepts/#knowledge-graph>
    
#### [`__init__` method](#kglab.KnowledgeGraph.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L48)

```python
__init__(name="generic", base_uri=None, language="en", namespaces=None, graph=None)
```
Constructor for a `KnowledgeGraph` object.

  * `name` : `str`  
optional, internal name for this graph

  * `base_uri` : `str`  
the default [*base URI*](https://tools.ietf.org/html/rfc3986#section-5.1) for this RDF graph

  * `language` : `str`  
the default [*language tag*](https://www.w3.org/TR/rdf11-concepts/#dfn-language-tag), e.g., used for [*language indexing*](https://www.w3.org/TR/json-ld11/#language-indexing)

  * `namespaces` : `dict`  
a dictionary of [*namespace*s](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) (dict values) and their corresponding *prefix* strings (dict keys) to add as *controlled vocabularies* available to use in the RDF graph, binding each prefix to the given namespace.

  * `graph` : `typing.Union[rdflib.graph.ConjunctiveGraph, rdflib.graph.Dataset, rdflib.graph.Graph, NoneType]`  
optionally, another existing RDF graph to be used as a starting point



#### [`add_ns` method](#kglab.KnowledgeGraph.add_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L108)

```python
add_ns(prefix, iri, override=True, replace=False)
```
Adds another [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) among the *controlled vocabularies* available to use in the RDF graph, binding the `prefix` to the given namespace.

Since the RDFlib [`NamespaceManager`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.namespace.NamespaceManager) automagically converts all input bindings into [`URIRef`](https://www.w3.org/TR/rdf-concepts/#section-Graph-URIref) instead, we'll keep references to the namespaces – for later use.

  * `prefix` : `str`  
a [namespace prefix](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-prefix)

  * `iri` : `str`  
URL to use for constructing the [namespace IRI](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-iri)

  * `override` : `bool`  
rebind, even if the given namespace is already bound with another prefix

  * `replace` : `bool`  
replace any existing prefix with the new namespace



#### [`get_ns` method](#kglab.KnowledgeGraph.get_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L148)

```python
get_ns(prefix)
```
Lookup a [*namespace*](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) among the *controlled vocabularies* available to use in the RDF graph.

  * `prefix` : `str`  
a [namespace prefix](https://www.w3.org/TR/rdf11-concepts/#dfn-namespace-prefix)

  * *returns* : `rdflib.namespace.Namespace`  
the RDFlib [`Namespace`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=namespace#rdflib.Namespace) for the *controlled vocabulary* referenced by `prefix`



#### [`describe_ns` method](#kglab.KnowledgeGraph.describe_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L164)

```python
describe_ns()
```
Describe the *namespaces* used in this RDF graph

  * *returns* : `pandas.core.frame.DataFrame`  
a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) describing the namespaces in this RDF graph



#### [`get_context` method](#kglab.KnowledgeGraph.get_context)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L177)

```python
get_context()
```
Generates a [*JSON-LD context*](https://www.w3.org/TR/json-ld11/#the-context) used for
serializing the RDF graph as [JSON-LD](https://json-ld.org/).

  * *returns* : `dict`  
context needed for JSON-LD serialization



#### [`encode_date` method](#kglab.KnowledgeGraph.encode_date)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L201)

```python
encode_date(datetime, tzinfos)
```
Helper method to ensure that an input `datetime` value has a timezone that can be interpreted by [`rdflib.XSD.dateTime`](https://www.w3.org/TR/xmlschema-2/#dateTime).

  * `datetime` : `str`  
input datetime as a string

  * `tzinfos` : `dict`  
timezones as a dict, used by

  * *returns* : `rdflib.term.Literal`  
[`rdflib.Literal`](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#literals) formatted as an XML Schema 2 `dateTime` value.



#### [`add` method](#kglab.KnowledgeGraph.add)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L223)

```python
add(s, p, o)
```
Wrapper for [`rdflib.Graph.add()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=add#rdflib.Graph.add) to add a relation *(subject, predicate, object)* to the RDF graph, if it doesn't already exist.
Uses the RDF Graph as its context.

To prepare for upcoming **kglab** features, **this is the preferred method for adding relations to an RDF graph.**

  * `s` : `typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*subject* node; must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

  * `p` : `typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*predicate* relation; ; must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

  * `o` : `typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*object* node; must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node) or [`rdflib.term.Terminal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Literal)



#### [`remove` method](#kglab.KnowledgeGraph.remove)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L247)

```python
remove(s, p, o)
```
Wrapper for [`rdflib.Graph.remove()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=add#rdflib.Graph.remove) to remove a relation *(subject, predicate, object)* from the RDF graph, if it exist.
Uses the RDF Graph as its context.

To prepare for upcoming **kglab** features, **this is the preferred method for removing relations from an RDF graph.**

  * `s` : `typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*subject* node; must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

  * `p` : `typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*predicate* relation; ; must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node)

  * `o` : `typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`  
*object* node; must be a [`rdflib.term.Node`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Node) or [`rdflib.term.Terminal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Node#rdflib.term.Literal)



#### [`load_rdf` method](#kglab.KnowledgeGraph.load_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L367)

```python
load_rdf(path, format="ttl", base=None, **args)
```
Wrapper for [`rdflib.Graph.parse()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse) which parses an RDF graph from the `path` source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object)

  * `format` : `str`  
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

  * `base` : `str`  
logical URI to use as the document base; if not specified the document location is used



#### [`load_rdf_text` method](#kglab.KnowledgeGraph.load_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L416)

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
logical URI to use as the document base; if not specified the document location is used



#### [`save_rdf` method](#kglab.KnowledgeGraph.save_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L454)

```python
save_rdf(path, format="ttl", base=None, encoding="utf-8", **args)
```
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination.
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

  * `format` : `str`  
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

  * `base` : `str`  
optional base set for the graph

  * `encoding` : `str`  
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception



#### [`save_rdf_text` method](#kglab.KnowledgeGraph.save_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L519)

```python
save_rdf_text(format="ttl", base=None, encoding="utf-8", **args)
```
Wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to a string.

  * `format` : `str`  
serialization format, defaults to Turtle triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins; otherwise this throws a `TypeError` exception

  * `base` : `str`  
optional base set for the graph

  * `encoding` : `str`  
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

  * *returns* : `typing.AnyStr`  
text representing the RDF graph



#### [`load_jsonld` method](#kglab.KnowledgeGraph.load_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L561)

```python
load_jsonld(path, encoding="utf-8", **args)
```
Wrapper for [`rdflib-jsonld.parser.JsonLDParser.parse()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/parser.py) which parses an RDF graph from a [JSON-LD](https://json-ld.org/) source.
This traps some edge cases for the several source-ish parameters in RDFlib which had been overloaded.

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); otherwise this throws a `TypeError` exception

  * `encoding` : `str`  
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception



#### [`save_jsonld` method](#kglab.KnowledgeGraph.save_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L597)

```python
save_jsonld(path, encoding="utf-8", **args)
```
Wrapper for [`rdflib-jsonld.serializer.JsonLDSerializer.serialize()`](https://github.com/RDFLib/rdflib-jsonld/blob/master/rdflib_jsonld/serializer.py) which serializes the RDF graph to the `path` destination as [JSON-LD](https://json-ld.org/).
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

  * `encoding` : `str`  
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception



#### [`load_parquet` method](#kglab.KnowledgeGraph.load_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L637)

```python
load_parquet(path, **kwargs)
```
Wrapper for [`pandas.read_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html?highlight=read_parquet#pandas.read_parquet) which parses an RDF graph represented as a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.

To prepare for upcoming **kglab** features, **this is the preferred method for deserializing an RDF graph.**

Note: this adds relations to an RDF graph, it does not overwrite the existing RDF graph.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str), path object to a local file reference, or a [*readable, file-like object*](https://docs.python.org/3/glossary.html#term-file-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; a file URL can also be a path to a directory that contains multiple partitioned files, including a bucket in cloud storage – based on [`fsspec`](https://github.com/intake/filesystem_spec)



#### [`save_parquet` method](#kglab.KnowledgeGraph.save_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L662)

```python
save_parquet(path, compression="snappy", storage_options=None, **kwargs)
```
Wrapper for [`pandas.to_parquet()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html?highlight=to_parquet) which serializes an RDF graph to a [Parquet](https://parquet.apache.org/) file, using the [`pyarrow`](https://arrow.apache.org/) engine.

To prepare for upcoming **kglab** features, **this is the preferred method for serializing an RDF graph.**

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str), path object to a local file reference, or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); a string could be a URL; valid URL schemes include `https`, `http`, `ftp`, `s3`, `gs`, `file`; accessing cloud storage is based on [`fsspec`](https://github.com/intake/filesystem_spec)

  * `compression` : `str`  
name of the compression algorithm to use; defaults to `"snappy"`; can also be `"gzip"`, `"brotli"`, or `None` for no compression

  * `storage_options` : `dict`  
extra options parsed by [`fsspec`](https://github.com/intake/filesystem_spec) for cloud storage access



#### [`n3fy` method](#kglab.KnowledgeGraph.n3fy)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L698)

```python
n3fy(d, pythonify=True)
```
Wrapper for RDFlib [`n3()`](https://rdflib.readthedocs.io/en/stable/utilities.html?highlight=n3#serializing-a-single-term-to-n3) and [`toPython()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=toPython#rdflib.Variable.toPython) to convert one row of a result set of a SPARQL query into a readable representation for each term, using N3 format.

  * `d` : `dict`  
one row of a SPARQL query results, as a dict

  * `pythonify` : `bool`  
flag to force instances of [`rdflib.term.Literal`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=Literal#rdflib.term.Identifier) to their Python literal representation

  * *returns* : `dict`  
a dictionary of converted terms



#### [`query` method](#kglab.KnowledgeGraph.query)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L730)

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



#### [`query_as_df` method](#kglab.KnowledgeGraph.query_as_df)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L758)

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
the query result set represented as a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)



#### [`validate` method](#kglab.KnowledgeGraph.validate)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L800)

```python
validate(shacl_graph=None, shacl_graph_format=None, ont_graph=None, ont_graph_format=None, advanced=False, inference=None, inplace=False, abort_on_error=None, **kwargs)
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
prior to validation, run OWL2 RL profile-based expansion of the RDF graph based on [OWL-RL](https://github.com/RDFLib/OWL-RL); `"rdfs"`, `"owlrl"`, `"both"`, `None`

  * `inplace` : `typing.Union[bool, NoneType]`  
when enabled, do not clone the RDF graph prior to inference/expansion, just manipulate it in-place

  * `abort_on_error` : `typing.Union[bool, NoneType]`  
abort validation on the first error

  * *returns* : `typing.Tuple[bool, KnowledgeGraph, str]`  
a tuple of `conforms` (RDF graph passes the validation rules); `report_graph` (report as a `KnowledgeGraph` object); `report_text` (report formatted as text)



#### [`infer_owlrl_closure` method](#kglab.KnowledgeGraph.infer_owlrl_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L877)

```python
infer_owlrl_closure()
```
Infer deductive closure for [OWL 2 RL semantics](https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules) based on [OWL-RL](https://owl-rl.readthedocs.io/en/latest/stubs/owlrl.html#module-owlrl)

See <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>



#### [`infer_rdfs_closure` method](#kglab.KnowledgeGraph.infer_rdfs_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L890)

```python
infer_rdfs_closure()
```
Infer deductive closure for [RDFS semantics](https://www.w3.org/TR/rdf-mt/) based on [OWL-RL](https://owl-rl.readthedocs.io/en/latest/stubs/owlrl.html#module-owlrl)

See <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>



#### [`infer_rdfs_properties` method](#kglab.KnowledgeGraph.infer_rdfs_properties)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L903)

```python
infer_rdfs_properties()
```
Perform RDFS sub-property inference, adding super-properties where sub-properties have been used.

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



#### [`infer_rdfs_classes` method](#kglab.KnowledgeGraph.infer_rdfs_classes)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L931)

```python
infer_rdfs_classes()
```
Perform RDFS subclass inference, marking all resources having a subclass type with their superclass.

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



#### [`infer_skos_related` method](#kglab.KnowledgeGraph.infer_skos_related)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L964)

```python
infer_skos_related()
```
Infer OWL symmetry (both directions) for `skos:related`
[(*S23*)](https://www.w3.org/TR/skos-reference/#S23)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



#### [`infer_skos_concept` method](#kglab.KnowledgeGraph.infer_skos_concept)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L979)

```python
infer_skos_concept()
```
Infer `skos:topConceptOf` as a sub-property of `skos:inScheme`
[(*S7*)](https://www.w3.org/TR/skos-reference/#S7)

Infer `skos:topConceptOf` as `owl:inverseOf` the property `skos:hasTopConcept`
[(*S8*)](https://www.w3.org/TR/skos-reference/#S8)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.



#### [`infer_skos_hierarchical` method](#kglab.KnowledgeGraph.infer_skos_hierarchical)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1003)

```python
infer_skos_hierarchical(narrower=True)
```
Infer `skos:narrower` as `owl:inverseOf` the property `skos:broader`; although only keep `skos:narrower` on request
[(*S25*)](https://www.w3.org/TR/skos-reference/#S25)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

  * `narrower` : `bool`  
if false, `skos:narrower` will be removed instead of added



#### [`infer_skos_transitive` method](#kglab.KnowledgeGraph.infer_skos_transitive)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1030)

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



#### [`infer_skos_symmetric_mappings` method](#kglab.KnowledgeGraph.infer_skos_symmetric_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1059)

```python
infer_skos_symmetric_mappings(related=True)
```
Infer symmetric mapping properties (`skos:relatedMatch`, `skos:closeMatch`, `skos:exactMatch`) as instances of `owl:SymmetricProperty`
[(*S44*)](https://www.w3.org/TR/skos-reference/#S44)

Adapted from [`skosify`](https://github.com/NatLibFi/Skosify) which wasn't being updated regularly.

  * `related` : `bool`  
infer the `skos:related` super-property for all `skos:relatedMatch` relations



#### [`infer_skos_hierarchical_mappings` method](#kglab.KnowledgeGraph.infer_skos_hierarchical_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L1090)

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



## [`Measure` class](#Measure)
#### [`__init__` method](#kglab.Measure.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L100)

```python
__init__(name="generic")
```




#### [`reset` method](#kglab.Measure.reset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L110)

```python
reset()
```




#### [`measure_graph` method](#kglab.Measure.measure_graph)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L125)

```python
measure_graph(kg)
```




#### [`get_keyset` method](#kglab.Measure.get_keyset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L146)

```python
get_keyset(incl_pred=True)
```




## [`Simplex0` class](#Simplex0)
#### [`__init__` method](#kglab.Simplex0.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L17)

```python
__init__(name="generic")
```




#### [`increment` method](#kglab.Simplex0.increment)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L28)

```python
increment(item)
```




#### [`get_tally` method](#kglab.Simplex0.get_tally)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L37)

```python
get_tally()
```




#### [`get_keyset` method](#kglab.Simplex0.get_keyset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L50)

```python
get_keyset()
```




## [`Simplex1` class](#Simplex1)

Measure a dyad census from the RDF graph.
    
#### [`get_tally` method](#kglab.Simplex1.get_tally)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L37)

```python
get_tally()
```




#### [`get_keyset` method](#kglab.Simplex1.get_keyset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L50)

```python
get_keyset()
```




#### [`__init__` method](#kglab.Simplex1.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L63)

```python
__init__(name="generic")
```




#### [`increment` method](#kglab.Simplex1.increment)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L73)

```python
increment(item0, item1)
```




#### [`get_tally_map` method](#kglab.Simplex1.get_tally_map)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L84)

```python
get_tally_map()
```




## [`Subgraph` class](#Subgraph)
#### [`__init__` method](#kglab.Subgraph.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L18)

```python
__init__(kg, preload=[], excludes=[])
```




#### [`triples` method](#kglab.Subgraph.triples)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L32)

```python
triples()
```
Iterator for the RDF triples to be included in the subgraph.



#### [`transform` method](#kglab.Subgraph.transform)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L43)

```python
transform(node)
```
Label encoding: return a unique integer ID for the given graph node.



#### [`inverse_transform` method](#kglab.Subgraph.inverse_transform)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L59)

```python
inverse_transform(id)
```
Label encoding: return the graph node corresponding to a unique integer ID.



#### [`get_name` method](#kglab.Subgraph.get_name)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L72)

```python
get_name(node)
```
Produce a human-readable label from an RDF node.



#### [`pyvis_style_node` method](#kglab.Subgraph.pyvis_style_node)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L90)

```python
pyvis_style_node(g, node_id, label, style={})
```




#### [`vis_pyvis` method](#kglab.Subgraph.vis_pyvis)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L114)

```python
vis_pyvis(notebook=False, style={})
```
This is one example; you may need to copy and replicate 
to construct the graph design you need.
See <https://pyvis.readthedocs.io/>



---
## [module functions](#kglab)
#### [`calc_quantile_bins` function](#kglab.calc_quantile_bins)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L13)

```python
calc_quantile_bins(num_rows)
```
Calculate the bins to use for a quantile stripe, using [`numpy.linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)

num_rows: number of rows in the dataframe
return: the calculated bins, as a NumPy array



#### [`root_mean_square` function](#kglab.root_mean_square)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L49)

```python
root_mean_square(values)
```
Calculate the *root mean square* of the values in the given list.

values: list of values to use in the RMS calculation
return: RMS metric as a float



#### [`stripe_column` function](#kglab.stripe_column)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L26)

```python
stripe_column(values, bins)
```
Stripe a column in a dataframe, by interpolated quantiles into a set of discrete indexes.

values: list of values to stripe
bins: quantile bins; see [`calc_quantile_bins()`](#calc_quantile_bins-function)
return: the striped column values, as a NumPy array



---
## [module types](#kglab)
#### [`Census_Dyad_Tally` type](#kglab.Census_Dyad_Tally)
```python
Census_Dyad_Tally = typing.Tuple[pandas.core.frame.DataFrame, dict]
```

#### [`Census_Item` type](#kglab.Census_Item)
```python
Census_Item = typing.Union[str, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
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
NodeLike = typing.Union[str, NoneType, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
```

#### [`PathLike` type](#kglab.PathLike)
```python
PathLike = typing.Union[str, pathlib.Path, urlpath.URL]
```

#### [`RDF_Node` type](#kglab.RDF_Node)
```python
RDF_Node = typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
```

#### [`RDF_Triple` type](#kglab.RDF_Triple)
```python
RDF_Triple = typing.Tuple[typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode], typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode], typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]]
```

#### [`SPARQL_Bindings` type](#kglab.SPARQL_Bindings)
```python
SPARQL_Bindings = typing.Tuple[str, dict]
```

#### [`SerializedEvoShape` type](#kglab.SerializedEvoShape)
```python
SerializedEvoShape = typing.List[~Evolike]
```

