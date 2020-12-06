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
 
The **kglab** library provides a reasonably "Pythonic" abstraction layer
for these operations on KGs.
The class definitions can be subclassed and extended to handle specific needs.

Meanwhile, we're also extending some of the key components with distributed
versions, based on [`ray`](https://ray.io/) for better use of horizontal
scale-out and parallelization.


## Installation

Dependencies:

- [Python 3.6+](https://www.python.org/downloads/)
- [RDFlib](https://rdflib.readthedocs.io/)
- [rdflib-json](https://github.com/RDFLib/rdflib-jsonld)
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
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

If you would like to run a local notebook, install JupyterLab:

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

If you are using a Unix derivative (FreeBSD, GNU/Linux, OS X), you can 
achieve this by using the `export PATH="$HOME/.local/bin:$PATH"` command.

Once installed, launch JupyterLab with:
```
jupyter-lab
```


## Tutorial Outline

1. Building a graph in RDF using `rdflib`
  * [`ex00.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex00.ipynb)
    * examine the dataset
  * [`ex01.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01.ipynb)
    * construct a graph from RDF triples
    * using multiple namespaces
    * proper handling of literals
    * serialization to strings and files using `Turtle` and `JSON-LD`
2. Leveraging the `kglab` abstraction layer
  * [`ex02.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex02.ipynb)
    * construct and serialize the same graph using  `kglab`
3. Interactive graph visualization with `pyvis`
  * [`ex03.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex03.ipynb)
    * render triples as an interactive graph
4. Build a medium size KG from a CSV dataset
  * [`ex04.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex04.ipynb)
    * iterate through a dataset, representing a recipe for each row
    * compare relative file sizes for different serialization formats
5. Running SPARQL queries
  * [`ex05.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex05.ipynb)
    * load the medium size KG from the earlier example
    * run a SPARQL query to identify recipes with special ingredients and cooking times
    * use SPARQL queries and post-processing to create annotations
6. SHACL validation with `pySHACL`
  * [`ex06.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex06.ipynb)
    * SHACL examples with recipe data
7. Graph algorithms with `networkx`
  * [`ex07.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex07.ipynb)
    * load the medium size KG from the earlier example
    * run graph algorithms in `networkx` to analyze properties of the KG
8. Statistical relational learning with `pslpython`
  * [`ex08.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex08.ipynb)
    * use RDF to represent the "simple acquaintance" PSL example graph
    * load the graph into a KG
    * visualize the KG
    * run PSL to infer uncertainty in the `knows` relation for grounded nodes
9. Vector embedding with `gensim`
  * [`ex09.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex09.ipynb)
    * curating annotations
    * analyze ingredient labels from 250K recipes
    * use vector embedding to rank relatedness for labels
    * add string similarity, and an approximate pareto archive

---

[![kg+lab](https://github.com/DerwenAI/kglab/blob/main/docs/kglab.png)](https://github.com/DerwenAI/kglab/blob/main/docs/kglab.png)

## Production Use Cases

  * [Derwen](https://derwen.ai/) and its client projects


## Similar Projects

See also:

  * [zincbase](https://github.com/complexdb/zincbase)


## Attribution

**kglab** has an [MIT](https://spdx.org/licenses/MIT.html) license,
which is succinct and simplifies use in commercial applications.

Please use the following BibTeX entry for citing **kglab** if you use it in your research or software.
Citations are helpful for the continued development and maintenance of this library.

```
@misc{kglab,
    author    = {Paco Nathan},
    title     = {{kglab: a simple abstraction layer in Python for building and using knowledge graphs}},
    month     = nov,
    year      = 2020,
    publisher = {Derwen},
    url       = {https://github.com/DerwenAI/kglab}
    }
```


## Kudos

Many thanks to our contributors:
[@jake-aft](https://github.com/jake-aft),
[@dmoore247](https://github.com/dmoore247),
plus general support from [Derwen, Inc.](https://derwen.ai/)
and [The Knowledge Graph Conference](https://www.knowledgegraph.tech/).
