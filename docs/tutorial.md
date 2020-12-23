# Learning to use `kglab`

## Setup

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
    * [`ex01.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex01.ipynb)
    * construct a graph from RDF triples
    * using multiple namespaces
    * proper handling of literals
    * serialization to strings and files using `Turtle` and `JSON-LD`
1. Leveraging the `kglab` abstraction layer
    * [`ex02.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex02.ipynb)
    * construct and serialize the same graph using  `kglab`
1. Interactive graph visualization with `pyvis`
    * [`ex03.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex03.ipynb)
    * render triples as an interactive graph
1. Build a medium size KG from a CSV dataset
    * [`ex04.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex04.ipynb)
    * iterate through a dataset, representing a recipe for each row
    * compare relative file sizes for different serialization formats
1. Running SPARQL queries
    * [`ex05.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex05.ipynb)
    * load the medium size KG from the earlier example
    * run a SPARQL query to identify recipes with special ingredients and cooking times
    * use SPARQL queries and post-processing to create annotations
1. SHACL validation with `pySHACL`
    * [`ex06.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex06.ipynb)
    * SHACL validation with `pySHACL`
    * SHACL examples with `kglab` using the recipe KG
1. Graph algorithms with `networkx`
    * [`ex07.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex07.ipynb)
    * load the medium size KG from the earlier example
    * run graph algorithms in `networkx` to analyze properties of the KG
1. Statistical relational learning with `pslpython`
    * [`ex08.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex08.ipynb)
    * use RDF to represent the "simple acquaintance" PSL example graph
    * load the graph into a KG
    * visualize the KG
    * run PSL to infer uncertainty in the `knows` relation for grounded nodes
1. Vector embedding with `gensim`
    * [`ex09.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex09.ipynb)
    * curating annotations
    * analyze ingredient labels from 250K recipes
    * use vector embedding to rank relatedness for labels
    * add string similarity, and an approximate pareto archive
1. Measurement and inference
    * [`ex10.ipynb`](https://github.com/DerwenAI/kglab/blob/main/examples/ex10.ipynb)
    * measure a KG with `kglab.Measure`
    * inference based on `owlrl`
    * inference based on `skosify`
