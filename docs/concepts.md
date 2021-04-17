# Graph Concepts

<img src="../assets/nouns/concepts.png" alt="concept by Nithinan Tatah from the Noun Project" />

## DRAFT: Work in progress

This material is a work in progress, at "rough draft" stage.


## Class Abstractions

The primary abstractions used in **kglab** are based on a small set of
Python classes.
These class definitions can be subclassed and extended to handle
specific use cases as needed.


### Knowledge Graph

[`kglab.KnowledgeGraph`](../ref/#knowledgegraph-class)

the representation of *RDF graphs*,
including use of *semantic technologies* / *ontology* / *controlled vocabularies*,
and also handling *property graph* features

  * *namespace management*
  * *graph construction*
  * *serialization*
  * *querying*
  * *validation*
  * *inference*


### Subgraph

[`kglab.Subgraph`](../ref/#subgraph-class)

  * *transforms to matrix/tensor*
  * *label encoding*
  * *visualization*
  * *graph algorithms*
  * *probabilistic graph inference*
  * *embedding*


### Measure

[`kglab.Measure`](../ref/#measure-class)

  * *descriptive statistics*
  * *topological analysis*
  * constructing *shapes*
  * estimates of graph size and complexity
  * estimated computation costs
