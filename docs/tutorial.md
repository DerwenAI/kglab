# Syllabus

<img src="../assets/nouns/tutorial.png" alt="Video Tutorial by artworkbean from the Noun Project" />

## Abstract

Python has excellent libraries for working with graphs which provide:
semantic technologies, graph queries, interactive visualizations,
graph algorithms, probabilistic graph inference, as well as embedding
and other integrations with deep learning.
However, almost none of these have integration paths other than
writing lots of custom code, and most do not share common file
formats.
Moreover, few of these libraries integrate effectively with popular
data science tools (e.g., pandas, scikit-learn, PyTorch, spaCy, etc.)
or with popular infrastructure for scale-out (Apache Spark, Ray,
RAPIDS, Apache Parquet, fsspec, etc.) on cloud computing.

This tutorial introduces **kglab** – an open source project that
integrates RDFlib, OWL-RL, pySHACL, NetworkX, iGraph, pslpython,
PyVis, and more – to show how to use a wide range of graph-based
approaches, blending smoothly into data science workflows, and working
efficiently with popular data engineering practices.  The material
emphasizes hands-on coding examples which you can reuse; best
practices for integrating and leveraging other useful libraries;
history and bibliography (e.g., links to primary sources); accessible,
detailed API documentation; a detailed glossary of terminology; plus
links to many helpful resources, such as online 'playgrounds" –
meanwhile, keeping a practical focus on use cases.

The coding exercises in the following tutorial are based on progressive
examples based on cooking recipes, which illustrate the use of **kglab**
and related libraries in Python for *graph data science*.


## Prerequisites

  * Some coding experience in Python (you can read a 20-line program)
  * Interest in use cases that require *knowledge graph representation*

Additionally, if you've completed *Algebra 2* in secondary school and
have some business experience working with data analytics – both can
come in handy.


## Audience

  * Python developers who need to work with KGs
  * Data Scientists, Data Engineers, Machine Learning Engineers
  * Technical Leaders who want hands-on KG implementation experience
  * Executives working on data strategy who need to learn about KG capabilities
  * People interested in developing personal knowledge graphs


## Key Takeaways

  * Hands-on experience with popular open source libraries in Python for building KGs, including rdflib, pyshacl, networkx, owlrl, pslpython, and more
  * Coding examples that can be used as starting points for your own KG projects
  * How to blend different graph-based approaches within a data science workflow to complement each other’s strengths: for data quality checks, inference, human-in-the-loop, etc.
  * Integrating with popular data science tools, such as pandas, scikit-learn, matplotlib, etc.
  * Graph data science practices that fit well with Big Data tools such as Spark, Parquet, Ray, RAPIDS, and so on


## Outline

  1. Sources for data and controlled vocabularies: using a progressive example based on a Kaggle dataset for food/recipes
  2. KG Construction in rdflib and Serialization in TTL, JSON-LD, Parquet, etc.
  3. Transformations between RDF graphs and algebraic objects
  4. Interactive Visualization with PyVis
  5. Querying with SPARQL, with results in pandas
  6. Graph-based validation with SHACL constraint rules
  7. A sampler of graph algorithms in networkx and igraph
  8. Inference based on semantic closures: RDFS, OWL-RL, SKOS
  9. Inference and data quality checks based on probabilistic soft logic
  10. Embedding (deep learning) for data preparation and KG construction


## Installation

You can run the notebooks locally on a recent laptop.
First clone the Git repository:
```
git clone https://github.com/DerwenAI/kglab.git
cd kglab
```

From there you have two possibilities

### Install dependencies locally

To install the dependencies using `pip`:
```
python3 -m pip install -r requirements.txt
```

Alternatively, to install the dependencies using `conda`:
```
conda env create -f environment.yml
conda activate kglab
```

Also make sure to install
[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/).
To install using `pip`:
```
python3 -m pip install jupyterlab
```

Or if you use `conda` you can install it with:
```
conda install -c conda-forge jupyterlab
```

Note: for installing via `pip install --user` you must add the
user-level `bin` directory to your `PATH` environment variable in
order to launch JupyterLab.
If you're using a Unix derivative (FreeBSD, GNU/Linux, OS X), you can
achieve this by using the `export PATH="$HOME/.local/bin:$PATH"`
command.

Once installed, launch JupyterLab with:
```
jupyter-lab
```

Then open the `examples` subdirectory to launch the notebooks featured
in the following sections of this tutorial.

### Use docker-compose

Leveraging `docker` and `docker-compose` will free you
from having to install dependencies locally.

First make sure that you have docker and docker-compose installed
by following the [docker-compose documentation](https://docs.docker.com/compose/install/#install-compose)

Then, in your kglab folder, run:

```sh
docker-compose up
```
