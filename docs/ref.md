# Reference: `kglab` package
## [`KnowledgeGraph` class](#KnowledgeGraph)
#### [`__init__` method](#kglab.KnowledgeGraph.__init__)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L47)

```python
__init__(name="kg+lab", base_uri=None, language="en", namespaces={}, graph=None)
```
        



#### [`merge_ns` method](#kglab.KnowledgeGraph.merge_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L85)

```python
merge_ns(ns_set)
```
        



#### [`add_ns` method](#kglab.KnowledgeGraph.add_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L95)

```python
add_ns(prefix, uri)
```
Since rdflib converts Namespace bindings to URIRef, we'll keep references to them



#### [`get_ns` method](#kglab.KnowledgeGraph.get_ns)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L107)

```python
get_ns(prefix)
```
prefix: the TTL-format prefix used to reference the namespace
return: rdflib.Namespace


*returns:* `rdflib.namespace.Namespace`

#### [`get_context` method](#kglab.KnowledgeGraph.get_context)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L118)

```python
get_context()
```
Return a context needed for JSON-LD serialization


*returns:* `dict`

#### [`add` method](#kglab.KnowledgeGraph.add)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L138)

```python
add(s, p, o)
```
        



#### [`type_date` classmethod](#kglab.KnowledgeGraph.type_date)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L149)

```python
type_date(date, tz)
```
input `date` should be interpretable as having a local timezone


*returns:* `rdflib.term.Literal`

#### [`load_rdf` method](#kglab.KnowledgeGraph.load_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L174)

```python
load_rdf(path, format="n3", encoding="utf-8")
```
        



#### [`load_rdf_text` method](#kglab.KnowledgeGraph.load_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L191)

```python
load_rdf_text(data, format="n3", encoding="utf-8")
```
        



#### [`save_rdf` method](#kglab.KnowledgeGraph.save_rdf)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L203)

```python
save_rdf(path, format="n3", encoding="utf-8")
```
        



#### [`save_rdf_text` method](#kglab.KnowledgeGraph.save_rdf_text)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L220)

```python
save_rdf_text(format="n3", encoding="utf-8")
```
        


*returns:* `str`

#### [`load_jsonld` method](#kglab.KnowledgeGraph.load_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L231)

```python
load_jsonld(path, encoding="utf-8")
```
        



#### [`save_jsonld` method](#kglab.KnowledgeGraph.save_jsonld)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L244)

```python
save_jsonld(path, encoding="utf-8")
```
        



#### [`load_parquet` method](#kglab.KnowledgeGraph.load_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L263)

```python
load_parquet(path)
```
        



#### [`save_parquet` method](#kglab.KnowledgeGraph.save_parquet)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L276)

```python
save_parquet(path, compression="gzip")
```
        



#### [`query` method](#kglab.KnowledgeGraph.query)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L293)

```python
query(sparql, bindings={})
```
        


*returns:* `typing.Iterable`

#### [`n3fy` classmethod](#kglab.KnowledgeGraph.n3fy)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L305)

```python
n3fy(d, nm, pythonify=True)
```
        


*returns:* `dict`

#### [`query_as_df` method](#kglab.KnowledgeGraph.query_as_df)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L329)

```python
query_as_df(sparql, bindings={}, simplify=True, pythonify=True)
```
        


*returns:* `pandas.core.frame.DataFrame`

#### [`validate` method](#kglab.KnowledgeGraph.validate)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L353)

```python
validate(shacl_graph=None, shacl_graph_format=None, ont_graph=None, ont_graph_format=None, advanced=False, inference=None, abort_on_error=None, serialize_report_graph="n3", debug=False, **kwargs)
```
        


*returns:* `typing.Tuple[bool, ForwardRef('KnowledgeGraph'), str]`

#### [`infer_skos_related` method](#kglab.KnowledgeGraph.infer_skos_related)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L403)

```python
infer_skos_related()
```
Make sure that skos:related is stated in both directions (S23).



#### [`infer_skos_topConcept` method](#kglab.KnowledgeGraph.infer_skos_topConcept)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L415)

```python
infer_skos_topConcept()
```
Infer skos:topConceptOf/skos:hasTopConcept (S8) and skos:inScheme (S7).



#### [`infer_skos_hierarchical` method](#kglab.KnowledgeGraph.infer_skos_hierarchical)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L433)

```python
infer_skos_hierarchical(narrower=True)
```
Infer skos:broader/skos:narrower (S25) but only keep skos:narrower on request.
:param bool narrower: If set to False, skos:narrower will not be added,
but rather removed.



#### [`infer_skos_transitive` method](#kglab.KnowledgeGraph.infer_skos_transitive)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L456)

```python
infer_skos_transitive(narrower=True)
```
Perform transitive closure inference (S22, S24).



#### [`infer_skos_symmetric_mappings` method](#kglab.KnowledgeGraph.infer_skos_symmetric_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L477)

```python
infer_skos_symmetric_mappings(related=True)
```
Ensure that the symmetric mapping properties (skos:relatedMatch,
skos:closeMatch and skos:exactMatch) are stated in both directions (S44).
:param bool related: Add the skos:related super-property for all
    skos:relatedMatch relations (S41).



#### [`infer_skos_hierarchical_mappings` method](#kglab.KnowledgeGraph.infer_skos_hierarchical_mappings)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L504)

```python
infer_skos_hierarchical_mappings(narrower=True)
```
Infer skos:broadMatch/skos:narrowMatch (S43) and add the super-properties
skos:broader/skos:narrower (S41).
:param bool narrower: If set to False, skos:narrowMatch will be removed not added.



#### [`infer_rdfs_classes` method](#kglab.KnowledgeGraph.infer_rdfs_classes)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L533)

```python
infer_rdfs_classes()
```
Perform RDFS subclass inference.
Mark all resources with a subclass type with the upper class.



#### [`infer_rdfs_properties` method](#kglab.KnowledgeGraph.infer_rdfs_properties)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L560)

```python
infer_rdfs_properties()
```
Perform RDFS subproperty inference.
Add superproperties where subproperties have been used.



#### [`infer_rdfs_closure` method](#kglab.KnowledgeGraph.infer_rdfs_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L587)

```python
infer_rdfs_closure()
```
Add inferred triples from RDFS based on OWL-RL,
see <https://wiki.uib.no/info216/index.php/Python_Examples#RDFS_inference_with_RDFLib>



#### [`infer_owlrl_closure` method](#kglab.KnowledgeGraph.infer_owlrl_closure)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/kglab.py#L599)

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
        


*returns:* `typing.List[str]`

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
        


*returns:* `typing.Union[pandas.core.frame.DataFrame, NoneType]`

#### [`get_keyset` method](#kglab.Simplex0.get_keyset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L50)

```python
get_keyset()
```
        


*returns:* `set`

## [`Simplex1` class](#Simplex1)
#### [`get_tally` method](#kglab.Simplex1.get_tally)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L37)

```python
get_tally()
```
        


*returns:* `typing.Union[pandas.core.frame.DataFrame, NoneType]`

#### [`get_keyset` method](#kglab.Simplex1.get_keyset)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/topo.py#L50)

```python
get_keyset()
```
        


*returns:* `set`

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
        


*returns:* `typing.Tuple[pandas.core.frame.DataFrame, dict]`

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


*returns:* `typing.Generator[typing.Tuple[typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode], typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode], typing.Union[rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]], NoneType, NoneType]`

#### [`transform` method](#kglab.Subgraph.transform)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L43)

```python
transform(node)
```
Label encoding: return a unique integer ID for the given graph node.


*returns:* `int`

#### [`inverse_transform` method](#kglab.Subgraph.inverse_transform)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L59)

```python
inverse_transform(id)
```
Label encoding: return the graph node corresponding to a unique integer ID.


*returns:* `typing.Union[str, NoneType, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]`

#### [`get_name` method](#kglab.Subgraph.get_name)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/subg.py#L72)

```python
get_name(node)
```
Produce a human-readable label from an RDF node.


*returns:* `str`

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


*returns:* `pyvis.network.Network`

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


*returns:* `numpy.ndarray`

#### [`root_mean_square` function](#kglab.root_mean_square)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L49)

```python
root_mean_square(values)
```
Calculate the *root mean square* of the values in the given list.

values: list of values to use in the RMS calculation
return: RMS metric as a float


*returns:* `float`

#### [`stripe_column` function](#kglab.stripe_column)
[*\[source\]*](https://github.com/DerwenAI/kglab/blob/main/kglab/util.py#L26)

```python
stripe_column(values, bins)
```
Stripe a column in a dataframe, by interpolated quantiles into a set of discrete indexes.

values: list of values to stripe
bins: quantile bins; see [`calc_quantile_bins()`](#calc_quantile_bins-function)
return: the striped column values, as a NumPy array


*returns:* `numpy.ndarray`

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

#### [`NodeLike` type](#kglab.NodeLike)
```python
NodeLike = typing.Union[str, NoneType, rdflib.term.URIRef, rdflib.term.Literal, rdflib.term.BNode]
```

#### [`PathLike` type](#kglab.PathLike)
```python
PathLike = typing.Union[str, pathlib.Path]
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

