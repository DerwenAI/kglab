# kglab

The **kglab** library provides a simple abstraction layer in Python
for building and using knowledge graphs.

> **SPECIAL REQUEST:**
> Which features would you like to see the most in an open source Python library for building and using knowledge graphs? Please add suggestions to this online survey: https://forms.gle/FMHgtmxHYWocprMn6  This will help us prioritize our roadmap for **kglab**.


## Background

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
  * quality assurance (e.g., axioms)
  * managing a mix of namespaces
  * serialization to/from multiple formats
  * parallel processing across a cluster
  * interactive visualization
  * queries
  * graph algorithms
  * transitivity and other forms of enriching a graph
  * embedding (deep learning integration)
  * inference (e.g., PSL, Bayesian Networks, Causal, MLN, etc.)
  * other ML integrations
 
The **kglab** library provides a reasonably "Pythonic" abstraction layer
for these operations on KGs.
The class definitions can be subclassed and extended to handle specific needs.

Meanwhile, we're also extending some of the key components with distributed
versions, based on [`ray`](https://ray.io/) for better use of horizontal
scale-out and parallelization.

NB: this repo is *UNDER CONSTRUCTION* and will undergo much iteration prior
to the "KG 101" tutorial at https://www.knowledgeconnexions.world/talks/kg-101/

See [wiki](https://github.com/DerwenAI/kglab/wiki) for further details.


## Installation

Dependencies:

- [Python 3.6+](https://www.python.org/downloads/)
- [rdflib](https://rdflib.readthedocs.io/)
- [rdflib-json](https://github.com/RDFLib/rdflib-jsonld)
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [pyarrow](https://arrow.apache.org/)
- [NetworkX](https://networkx.org/)
- [dateutil](https://pypi.org/project/python-dateutil/)
- [pyvis](https://pyvis.readthedocs.io/)
- [matplotlib](https://matplotlib.org/)
- [pslpython](https://psl.linqs.org/)
- [gensim](https://radimrehurek.com/gensim/)
- [pylev](https://github.com/toastdriven/pylev)

To install from [PyPi](https://pypi.python.org/pypi/kglab):
```
pip install kglab
```

If you work directly from this Git repo, be sure to install the dependencies
as well:
```
pip install -r requirements.txt
```

If you would like to run a local Notebook install Jupyter Lab:

If you use conda, you can install it with:
```
conda install -c conda-forge jupyterlab
```

If you use pip, you can install it with:
```
pip install jupyterlab
```
If installing via `pip install --user` you must add the user-level bin 
directory to your PATH environment variable in order to launch JupyterLab.

If you are using a Unix derivative (FreeBSD, GNU / Linux, OS X), you can 
achieve this by using the `export PATH="$HOME/.local/bin:$PATH"` command.

Once installed, launch JupyterLab with:
```
jupyter-lab
```

## Tutorial Outline

1. Building a graph in RDF using `rdflib`
  * [`ex01_0.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_0.ipynb)
    * examine the dataset
  * [`ex01_1.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_1.ipynb)
    * construct a graph from RDF triples
    * using multiple namespaces
    * proper handling of literals
    * serialization to strings and files using `Turtle` and `JSON-LD`
2. Leveraging the `kglab` abstraction layer
  * [`ex01_2.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_2.ipynb)
    * construct and serialize the same graph using  `kglab`
3. Interactive graph visualization with `pyvis`
  * [`ex01_3.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_3.ipynb)
    * render triples as an interactive graph
4. Build a medium size KG from a CSV dataset
  * [`ex01_4.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_4.ipynb)
    * iterate through a dataset, representing a recipe for each row
    * compare relative file sizes for different serialization formats
5. Running SPARQL queries
  * [`ex01_5.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_5.ipynb)
    * load the medium size KG from the earlier example
    * run a SPARQL query to identify recipes with special ingredients and cooking times
    * use SPARQL queries and post-processing to create annotations
6. Graph algorithms with `networkx`
  * [`ex01_6.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_6.ipynb)
    * load the medium size KG from the earlier example
    * run graph algorithms in `networkx` to analyze properties of the KG
7. Statistical relational learning with `pslpython`
  * [`ex01_7.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_7.ipynb)
    * use RDF to represent the "simple acquaintance" PSL example graph
    * load the graph into a KG
    * visualize the KG
    * run PSL to infer uncertainty in the `knows` relation for grounded nodes
8. Vector embedding with `gensim`
  * [`ex01_8.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_8.ipynb)
    * curating annotations
    * analyze ingredient labels from 250K recipes
    * use vector embedding to rank relatedness for labels
    * add string similarity for an approximate pareto archive

---

## Production Use Cases

  * [Derwen](https://derwen.ai/) and its client projects


[![kg+lab](https://github.com/DerwenAI/kglab/blob/main/docs/kglab.png)](https://github.com/DerwenAI/kglab/blob/main/docs/kglab.png)


## Kudos

Many thanks to our contributors:
[@jake-aft](https://github.com/jake-aft),
plus general support from [Derwen, Inc.](https://derwen.ai/)
and [The Knowledge Graph Conference](https://www.knowledgegraph.tech/).

