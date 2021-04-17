# Use Cases

<img src="../assets/nouns/evidence.png" alt="Usage by Adrien Coquet from the Noun Project" />

## DRAFT: Work in progress

This material is a work in progress, at "rough draft" stage.


## Operationalizing AI

One of the major learnings from a decade-plus of data science is that
AI adoption in enterprise requires more than one team.
Instead there must be extensive cross-team coordination with executive
support.
Moreover, the projects cannot be merely *proof-of-concept* (POC)
"one-offs".
To sustain this kind of work, organizations must pursue more
efficient, effective approaches often called *Operationalizing AI* to
produce a steady stream of AI projects.
One difficulty of course is that enterprise organization must often
integrate with internal *legacy* systems.

The **kglab** library provides means for an enterprise organization to
establish and explore a *baseline* implementation for a knowledge graph
practice internally.
If an organization can see where it needs to integrate with its legacy
systems, or where features within **kglab** could be migrated into
proprietary systems, then use of this library may dramatically reduce
*time-to-market* key performance indicators for enterprise KG
projects.


## Data Context

["data context"]( http://cidrdb.org/cidr2017/papers/p111-hellerstein-cidr17.pdf) – 

In a world where organizations must be resilient in the face of abrupt
changes, we must adapt more resilient means for reconciling data from
a wide variety of sources: vendors, customers, partners, government
agencies, standards bodies, and so on.

KGs provide means for a kind of *abstraction layer* to make the data
cohere.


However, it's not clear when Gartner will acknowledge the breadth of
industry adoption for KG approaches in enterprise data management.

To paraphrase [Natasha Noy](https://research.google/people/NatalyaNoy/), 
a research scientist at Google Research and highly-regarded practitioner 
in this field:

> An "enterprise knowledge graph" provides *ground truth* through which we can reconcile our queries and other usage of many disparate data stores.

For example, having *persistent identifiers* with other metadata
attached is a great start.



---


For several KG projects, we kept reusing a similar working set of libraries:

  * [`rdflib`](https://rdflib.readthedocs.io/)
  * [`networkx`](https://networkx.org/)
  * [`pyvis`](https://pyvis.readthedocs.io/)
  * [`pytextrank`](https://pypi.org/project/pytextrank/)
  * [`richcontext.scholapi`](https://pypi.org/project/richcontext-scholapi/)
  * [`skosify`](https://skosify.readthedocs.io/)

Each of these libraries provides a useful piece of the puzzle when you need
to leverage *knowledge representation*, *graph algorithms*, *entity linking*,
*interactive visualization*, *metadata queries*, *axioms*, etc.
However, some of them are relatively low-level (e.g., `rdflib`) or perhaps not
maintained as much (e.g., `skosify`) and there are challenges integrating them.
Challenges we kept having to reinvent work-arounds to resolve.

There are general operations that one must perform on knowledge graphs:

  * building triples
  * managing a mix of namespaces
  * serialization to/from multiple formats
  * queries
  * interactive visualization
  * transitivity and other forms of enriching a graph
  * graph algorithms
  * inference (e.g., PSL, Bayesian Networks, Causal, MLN, etc.)
  * quality assurance (e.g., axioms)
  * parallel processing across a cluster
  * embedding (deep learning integration)
  * other ML integrations

