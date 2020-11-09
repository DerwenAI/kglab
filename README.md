# kglab

The **kglab** library provides a simple to use abstraction layer in Python
for building knowledge graphs.
For several KG projects, we kept reusing a similar working set of libraries:

  * [`rdflib`](https://rdflib.readthedocs.io/)
  * [`networkx`](https://networkx.org/)
  * [`pyvis`](https://pyvis.readthedocs.io/)
  * [`pytextrank`](https://pypi.org/project/pytextrank/)
  * [`richcontext.scholapi`](https://pypi.org/project/richcontext-scholapi/)
  * [`skosify`](https://skosify.readthedocs.io/)


## Background

Each of those libraries provides a useful piece of the pizzle when you need
to leverage *knowledge representation*, *graph algorithms*, *entity linking*,
*interactive visualization*, *metadata queries*, *axioms*, etc.
However, some of them are relatively low-level (e.g., `rdflib`) or perhaps not
maintained as much (e.g., `skosify`) and there are challenges integrating them.
Challenges we kept having to reinvent work-arounds to resolve.

There are general operations that one must perform on knowledge graphs:

  * building triples
  * quality assurance (e.g., axioms)
  * managing a mix of namespaces
  * serialization to/from multiple formats
  * interactive visualization
  * queries
  * graph algorithms
  * inference, transitivity, etc.
  * embedding
  * other ML integrations
 
The **kglab** library provides a reasonably "Pythonic" abstraction layer
for these operations on KGs.
These class definitions can be subclassed and extended to handle more 
specific needs.
Meanwhile, we're also extending some of the key components with distributed
versions, based on [`ray`](https://ray.io/) for better use of horizontal
scale-out and parallelization.

NB: this repo is *UNDER CONSTRUCTION* and will undergo much iteration prior
to the "KG 101" tutorial at https://www.knowledgeconnexions.world/talks/kg-101/

See [wiki](https://github.com/DerwenAI/kglab/wiki) for further details.


## Installation

Prerequisites:

- [Python 3.5+](https://www.python.org/downloads/)
- [rdflib](https://rdflib.readthedocs.io/)
- [NetworkX](https://networkx.org/)
- [pyvis](https://pyvis.readthedocs.io/)

To install from [PyPi](https://pypi.python.org/pypi/kglab):

```
pip install kglab
```

If you work directly from this Git repo, be sure to install the dependencies
as well:

```
pip install -r requirements.txt
```


## Tutorial Outline

1. Building a graph in RDF using `rdflib`
  * [`ex01_0.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_0.ipynb)
    * examine the dataset
  * [`ex01_1.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_1.ipynb)
    * construct a graph from RDF triples
    * using multiple namespaces
    * proper handling of literals
    * seralization to strings and files using `Turtle` and `JSON-LD`
2. Leveraging the `kglab` abstraction layer
  * [`ex01_2.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_2.ipynb)
    * construct and serialize the same graph using  `kglab`
3. Interactive graph visualization with `pyvis`
  * [`ex01_3.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_3.ipynb)
    * render triples as an interactive graph


---

## Production Use Cases

  * [Derwen](https://derwen.ai/) and its client projects
