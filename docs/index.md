# Graph-Based Data Science

<img src="assets/logo.png" width="113" alt="illustration of a knowledge graph, plus laboratory glassware"/>

The **kglab** package provides a simple
[abstraction layer](glossary/#abstraction-layer)
in Python for building
[*knowledge graphs*](glossary/#knowledge-graph).

The main goal is to leverage idiomatic Python for common use cases in 
[data science](glossary/#data-science)
and 
[data engineering](glossary/#data-engineering)
work that require graph data, presenting 
[*graph-based data science*](glossary/#graph-based-data-science)
as an emerging practice.


## Cut to the Chase

  1. To get started right away, jump to [*Getting Started*](start/)
  1. For an extensive, hands-on coding tour through **kglab**, follow the [*Tutorial*](tutorial/) notebooks
  1. Check the source code at <https://github.com/DerwenAI/kglab>


## Motivations

!!! note
    **FAQ:** Why build yet another graph library, when there are already so many available?

A short list of primary motivations have been identified for
**kglab**, its design criteria, and engineering trade-offs:


### Popular Graph Libraries

**Point 1:**
integrate with popular graph libraries, including 
[RDFlib](https://rdflib.readthedocs.io/),
[OWL-RL](https://owl-rl.readthedocs.io/),
[pySHACL](https://github.com/RDFLib/pySHACL),
[NetworkX](https://networkx.org/),
[iGraph](https://igraph.org/python/),
[PyVis](https://pyvis.readthedocs.io/), 
[node2vec](http://snap.stanford.edu/node2vec/),
[pslpython](https://psl.linqs.org/),
[pgmpy](https://pgmpy.org/),
and so on –
several of which would otherwise not have much common ground.


### Data Science Workflows

**Point 2:**
close integration plus example code for working with the
["PyData" stack](https://numfocus.org/sponsored-projects),
namely
[pandas](https://pandas.pydata.org/),
[NumPy](https://numpy.org/),
[scikit-learn](https://scikit-learn.org/),
[matplotlib](https://matplotlib.org/),
etc.,
as well as
[PyTorch](https://pytorch.org/),
and other quintessential data science tools.


### Distributed Systems Infrastructure

**Point 3:**
integrate efficiently with *Big Data* tools and practices for contemporary
[data engineering](glossary/#data-engineering)
and
[cloud computing](glossary/#cloud-computing)
infrastructure, including:
[Ray](https://ray.io/),
[Jupyter](https://jupyter.org/),
[RAPIDS](https://rapids.ai/),
[Apache Arrow](https://arrow.apache.org/),
[Apache Parquet](https://parquet.apache.org/),
[Apache Spark](https://spark.apache.org/),
etc.


### Natural Language Understanding

**Point 4:**
incorporate graph-based methods and
[semantic technologies](glossary/#semantic-technologies)
into
[`spaCy`](https://spacy.io/) pipelines, e.g., through 
[`pytextrank`](https://github.com/DerwenAI/pytextrank/), 
plus
[`biome.text`](https://www.recogn.ai/biome-text/)
and other customized
[natural language](glossary/#natural-language)
pipelines.


### Hybrid AI Approaches

**Point 5:**
explore "hybrid" approaches that combine 
[machine learning](glossary/#machine-learning)
with
symbolic, rule-based processing – including 
[probabilistic graph inference](glossary/#probabilistic-graph-inference)
and
[knowledge graph embedding](glossary/#knowledge-graph-embedding).


The overall intent of **kglab** is to build an
[abstraction layer](glossary/#abstraction-layer)
for
[KG](glossary/#kg)
work in Python,
provided as a *library* not as a *framework*.


## Getting Help

The [Knowledge Graph Conference](glossary/#knowledge-graph-conference)
hosts several community resources where you can post questions and 
get help about **kglab** and related
[KG](glossary/#kg)
topics.

  * [community Slack](https://knowledgegraphconf.slack.com/archives/C017LUAML8Z) – specifically on the `#ask` channel
  * [Knowledge Tech Q&A site](https://answers.knowledgegraph.tech/) for extended discussions
  * ["KG 101"](https://knowledge-connexions-conference.heysummit.com/talks/kg-101/) tutorial at *Knowledge Connexions* 2020
  * [*Just Enough Math*](https://www.linkedin.com/groups/6725785/) group on LinkedIn – join to receive related updates, news, conference coupons, etc.

[KGC](glossary/#knowledge-graph-conference)
also hosts 
[monthly office hours](https://www.notion.so/KG-Community-Events-Calendar-8aacbe22efa94d9b8b39b7288e22c2d3)
for [Paco Nathan](author/) and others involved in this open source project.


## Feedback and Roadmap

!!! note
    **SPECIAL REQUEST:** Which features would you like to see the most 
    in an open source Python library for building knowledge graphs?

Your feedback through this online survey helps us prioritize the roadmap for **kglab**:
<https://forms.gle/FMHgtmxHYWocprMn6>

Links for other open source community resources:

  * [Milestones](https://github.com/DerwenAI/kglab/milestones)
  * [GH Issues](https://github.com/DerwenAI/kglab/issues)
  * [Project Board](https://github.com/DerwenAI/kglab/projects/1)
