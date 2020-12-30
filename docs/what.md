# What is a Knowledge Graph?

  * RDF graph, [*semantic technologies*](../glossary/#semantic-technologies)
  * KG compare/contrast with [*property graph*](../glossary/#property-graph)
  * the ubiquity of graph-based work in data science
  * graph algorithms vs. visualization vs. graph AI vs. probabilistic graphs vs. graph queries
  * *separation of concerns* between graph-based data science and data engineering
  * lessons of 2010 all over again: MPPs, BI, EDW, etc.

narrative arc: 
[linden2006early](../biblio/#linden2006early)
 => 
[kreps2014](../biblio/#kreps2014)
 =>
[anderson2020dt](../biblio/#anderson2020dt)
with
[breiman2001](../biblio/#breiman2001) in-between


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

[^2]: see [brewer2012cap](../biblio/#brewer2012cap) for discussion of the *CAP Theorem*
