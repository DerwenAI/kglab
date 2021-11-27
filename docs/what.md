# What's a Knowledge Graph?

<img src="../assets/nouns/concepts.png" alt="concept by Nithinan Tatah from the Noun Project" />

## DRAFT: Work in progress

This material is a work in progress, at "rough draft" stage.


First, read:
[[hogan2020knowledge]](../biblio/#hogan2020knowledge)

Some good elements for KG definition:
<https://towardsdatascience.com/how-to-create-representations-of-entities-in-a-knowledge-graph-using-pyrdf2vec-82e44dad1a0#1f07>
>Graphs are data structures that are useful to represent ubiquitous phenomena, such as social networks, chemical molecules and recommendation systems. One of their strengths lies in the fact that they explicitly model relations (i.e. edges) between individual units (i.e. nodes), which adds an extra dimension to the data.

compare:
[[nathan2019fifty]](../biblio/#nathan2019fifty)

going back to:
[[peirce1882]](../biblio/#peirce1882)


## Just Enough Graph Theory

In a pure mathematical form, where a *node* (or *vertex*) can connect
through an *edge* (or *arc* or *link*) to another node.

$$
G=\{V, E\}
$$

In that case an *adjacency matrix* can represent the entire graph.
Each node has a row and a column in the matrix.

  * https://en.wikipedia.org/wiki/Adjacency_matrix
  * https://mathworld.wolfram.com/AdjacencyMatrix.html

In the simplest form, a `1` value in the matrix element represents an
edge between nodes or a `0` otherwise.

  * symmetric for undirected graphs
  * asymmetric for directed graphs

If a directed graph has *weights* on its edges (i.e., to represent the
probability of an event between two nodes) then replace the `1` value
with the weight or probability.
This is called a *stochastic matrix*

  * https://en.wikipedia.org/wiki/Stochastic_matrix
  * transitions of Markov chain (state)

There's an entire field of *algebraic graph theory* that translates
between *graph theory* and *linear algebra*.

eigenvalues, eigenvectors, spectrum

non-negative, symmetric properties allow for *factorization* (or *decomposition*):

  * https://en.wikipedia.org/wiki/Matrix_decomposition
  * https://sparse.tamu.edu/about
  * https://www.cs.purdue.edu/homes/dgleich/


## RDF Graph

  * RDF graph, [*semantic technologies*](../glossary/#semantic-technologies)
  * KG compare/contrast with [*property graph*](../glossary/#property-graph)
  * the ubiquity of graph-based work in data science
  * graph algorithms vs. visualization vs. graph AI vs. probabilistic graphs vs. graph queries
  * *separation of concerns* between graph data science and data engineering
  * lessons of 2010 all over again: MPPs, BI, EDW, etc.

narrative arc: 
[[linden2006early]](../biblio/#linden2006early)
 => 
[[kreps2014]](../biblio/#kreps2014)
 =>
[[anderson2020dt]](../biblio/#anderson2020dt)
with
[[breiman2001]](../biblio/#breiman2001)
[[brewer2012cap]](../biblio/#brewer2012cap)
in-between

In 2018, Gartner began to acknowledge the term 
[*knowledge graph*](../glossary/#knowledge-graph)
and in mid-2020 described the importance of KGs for developing 
AI applications[^1].

---

KGs allow for multiple teams to be working concurrently, i.e., with
less centralized control.

This is in contrast to legacy notion about 
[*one size fits all*](../glossary/#osfa)
(OSFA) for data management.

To wit, the best way to make data *consistent* and *available*[^2]
is not to import **all** of the data sources into a single 
[data management](../glossary/#data-management)
framework, where a limited of set of individuals proscribe the
schema and access rules.
Those days are long gone.


[^1]: ["How to Build Knowledge Graphs That Enable AI-Driven Enterprise Applications"](https://www.gartner.com/en/documents/3985680/how-to-build-knowledge-graphs-that-enable-ai-driven-ente), Afraz Jaffri, *Gartner Research* (2020-05-27)

[^2]: see [[brewer2012cap]](../biblio/#brewer2012cap) for discussion of the *CAP Theorem*
