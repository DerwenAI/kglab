# Reference: `kglab` package
## [`KnowledgeGraph` class](#KnowledgeGraph)
#### [`__init__` method](#kglab.KnowledgeGraph.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L49)

```python
__init__(name="kg+lab", base_uri=None, language="en", namespaces={}, graph=None)
```




#### [`merge_ns` method](#kglab.KnowledgeGraph.merge_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L87)

```python
merge_ns(ns_set)
```




#### [`add_ns` method](#kglab.KnowledgeGraph.add_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L97)

```python
add_ns(prefix, uri)
```
Since rdflib converts Namespace bindings to URIRef, we'll keep references to them



#### [`get_ns` method](#kglab.KnowledgeGraph.get_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L109)

```python
get_ns(prefix)
```
prefix: the TTL-format prefix used to reference the namespace
return: rdflib.Namespace



#### [`get_context` method](#kglab.KnowledgeGraph.get_context)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L120)

```python
get_context()
```
Return a context needed for JSON-LD serialization



#### [`add` method](#kglab.KnowledgeGraph.add)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L140)

```python
add(s, p, o)
```




#### [`type_date` classmethod](#kglab.KnowledgeGraph.type_date)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L151)

```python
type_date(date, tz)
```
input `date` should be interpretable as having a local timezone



#### [`load_rdf` method](#kglab.KnowledgeGraph.load_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L212)

```python
load_rdf(path, format="n3", encoding="utf-8")
```




#### [`load_rdf_text` method](#kglab.KnowledgeGraph.load_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L227)

```python
load_rdf_text(data, format="n3", encoding="utf-8")
```




#### [`save_rdf` method](#kglab.KnowledgeGraph.save_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L239)

```python
save_rdf(path, format="n3", base=None, encoding="utf-8", **args)
```
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination.
This traps some edge cases for the `destination` parameter in RDFlib which had been overloaded.

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

  * `format` : `str`  
serialization format, defaults to N3 triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins – excluding the `"json-ld"` format; otherwise this throws a `TypeError` exception

  * `base` : `str`  
optional base set for the graph

  * `encoding` : `str`  
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception



#### [`save_rdf_text` method](#kglab.KnowledgeGraph.save_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L310)

```python
save_rdf_text(format="n3", base=None, encoding="utf-8", **args)
```
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to a string.

  * `format` : `str`  
serialization format, defaults to N3 triples; see `_RDF_FORMAT` for a list of default formats, which can be extended with plugins; otherwise this throws a `TypeError` exception

  * `base` : `str`  
optional base set for the graph

  * `encoding` : `str`  
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception

  * *returns* : `typing.AnyStr`  
A string representing the RDF graph



#### [`load_jsonld` method](#kglab.KnowledgeGraph.load_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L359)

```python
load_jsonld(path, encoding="utf-8")
```




#### [`save_jsonld` method](#kglab.KnowledgeGraph.save_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L376)

```python
save_jsonld(path, encoding="utf-8", **args)
```
A wrapper for [`rdflib.Graph.serialize()`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html?highlight=serialize#rdflib.Graph.serialize) which serializes the RDF graph to the `path` destination as [JSON-LD](https://json-ld.org/).

  * `path` : `typing.Union[str, pathlib.Path, urlpath.URL, typing.IO]`  
must be a file name (str) or a path object (not a URL) to a local file reference; or a [*writable, bytes-like object*](https://docs.python.org/3/glossary.html#term-bytes-like-object); otherwise this throws a `TypeError` exception

  * `encoding` : `str`  
text encoding value, defaults to `"utf-8"`, must be in the [Python codec registry](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo); otherwise this throws a `LookupError` exception



#### [`load_parquet` method](#kglab.KnowledgeGraph.load_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L418)

```python
load_parquet(path, **kwargs)
```




#### [`save_parquet` method](#kglab.KnowledgeGraph.save_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L435)

```python
save_parquet(path, compression="snappy", **kwargs)
```




#### [`query` method](#kglab.KnowledgeGraph.query)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L457)

```python
query(sparql, bindings={})
```




#### [`n3fy` classmethod](#kglab.KnowledgeGraph.n3fy)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L469)

```python
n3fy(d, nm, pythonify=True)
```




#### [`query_as_df` method](#kglab.KnowledgeGraph.query_as_df)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L493)

```python
query_as_df(sparql, bindings={}, simplify=True, pythonify=True)
```




#### [`validate` method](#kglab.KnowledgeGraph.validate)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L517)

```python
validate(shacl_graph=None, shacl_graph_format=None, ont_graph=None, ont_graph_format=None, advanced=False, inference=None, abort_on_error=None, serialize_report_graph="n3", debug=False, **kwargs)
```




#### [`infer_skos_related` method](#kglab.KnowledgeGraph.infer_skos_related)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L567)

```python
infer_skos_related()
```
Make sure that skos:related is stated in both directions (S23).



#### [`infer_skos_topConcept` method](#kglab.KnowledgeGraph.infer_skos_topConcept)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L579)

```python
infer_skos_topConcept()
```
Infer skos:topConceptOf/skos:hasTopConcept (S8) and skos:inScheme (S7).



#### [`infer_skos_hierarchical` method](#kglab.KnowledgeGraph.infer_skos_hierarchical)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L597)

```python
infer_skos_hierarchical(narrower=True)
```
Infer skos:broader/skos:narrower (S25) but only keep skos:narrower on request.
:param bool narrower: If set to False, skos:narrower will not be added,
but rather removed.



#### [`infer_skos_transitive` method](#kglab.KnowledgeGraph.infer_skos_transitive)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L620)

```python
infer_skos_transitive(narrower=True)
```
Perform transitive closure inference (S22, S24).



#### [`infer_skos_symmetric_mappings` method](#kglab.KnowledgeGraph.infer_skos_symmetric_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L641)

```python
infer_skos_symmetric_mappings(related=True)
```
Ensure that the symmetric mapping properties (skos:relatedMatch,
skos:closeMatch and skos:exactMatch) are stated in both directions (S44).
:param bool related: Add the skos:related super-property for all
    skos:relatedMatch relations (S41).



#### [`infer_skos_hierarchical_mappings` method](#kglab.KnowledgeGraph.infer_skos_hierarchical_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L668)

```python
infer_skos_hierarchical_mappings(narrower=True)
```
Infer skos:broadMatch/skos:narrowMatch (S43) and add the super-properties
skos:broader/skos:narrower (S41).
:param bool narrower: If set to False, skos:narrowMatch will be removed not added.



#### [`infer_rdfs_classes` method](#kglab.KnowledgeGraph.infer_rdfs_classes)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L697)

```python
infer_rdfs_classes()
```
Perform RDFS subclass inference.
Mark all resources with a subclass type with the upper class.



#### [`infer_rdfs_properties` method](#kglab.KnowledgeGraph.infer_rdfs_properties)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L724)

```python
infer_rdfs_properties()
```
Perform RDFS subproperty inference.
Add superproperties where subproperties have been used.



#### [`infer_rdfs_closure` method](#kglab.KnowledgeGraph.infer_rdfs_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L751)

```python
infer_rdfs_closure()
```
Add inferred triples from RDFS based on OWL-RL,
see <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>



#### [`infer_owlrl_closure` method](#kglab.KnowledgeGraph.infer_owlrl_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L763)

```python
infer_owlrl_closure()
```
Add inferred triples from OWL based on OWL-RL,
see <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>



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

