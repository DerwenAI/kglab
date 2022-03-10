# kglab

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4717287.svg)](https://doi.org/10.5281/zenodo.4717287)
![Licence](https://img.shields.io/github/license/DerwenAI/kglab)
![Repo size](https://img.shields.io/github/repo-size/DerwenAI/kglab)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/DerwenAI/kglab?style=plastic)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/DerwenAI/kglab.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/DerwenAI/kglab/context:python)
![CI](https://github.com/DerwenAI/kglab/workflows/CI/badge.svg)
[![Docker Pulls](https://img.shields.io/docker/pulls/derwenai/kglab.svg?maxAge=604800)](https://hub.docker.com/r/derwenai/kglab/)
![downloads](https://img.shields.io/pypi/dm/kglab)
![sponsor](https://img.shields.io/github/sponsors/ceteri)


Welcome to *Graph Data Science*:
<https://derwen.ai/docs/kgl/>

The **kglab** library provides a simple abstraction layer in Python 3.7+
for building knowledge graphs, leveraging Pandas, NetworkX, RAPIDS, RDFLib,
Morph-KGC, pythonPSL, and many more.

> **SPECIAL REQUEST:**  
> Which features would you like in an open source Python library for building knowledge graphs?  
> Please add your suggestions through this survey:  
> https://forms.gle/FMHgtmxHYWocprMn6  
> This will help us prioritize the **kglab** roadmap.


## Reviews

[@kaaloo](https://github.com/kaaloo): 
> "Feels like it's a Hugging Face for graphs! 🤯"


## Getting Started

See the ["Getting Started"](https://derwen.ai/docs/kgl/start/)
section of the online documentation.

We recommend installing from [PyPi](https://pypi.python.org/pypi/kglab):
```bash
python3 -m pip install kglab
```

If you work directly from this Git repo, be sure to install the 
dependencies:
```bash
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
```

Alternatively, to install dependencies using `conda`:
```bash
conda env create -f environment.yml --force
conda activate kglab
```

Then to run some simple uses of this library:
```python
import kglab

# create a KnowledgeGraph object
kg = kglab.KnowledgeGraph()

# load RDF from a URL
kg.load_rdf("http://bigasterisk.com/foaf.rdf", format="xml")

# measure the graph
measure = kglab.Measure()
measure.measure_graph(kg)

print("edges: {}\n".format(measure.get_edge_count()))
print("nodes: {}\n".format(measure.get_node_count()))

# serialize as a string in "Turtle" TTL format
ttl = kg.save_rdf_text()
print(ttl)
```

See the **tutorial notebooks** in the `examples` subdirectory for
sample code and patterns to use in integrating **kglab** with other
graph libraries in Python:
<https://derwen.ai/docs/kgl/tutorial/>


> **WARNING when installing in an existing environment:**  
> Installing a new package in an existing environment may reveal  
> or create version conflicts. See the **kglab** requirements  
> in `requirements.txt` before you do. For example, there are  
> [known version conflicts](https://github.com/DerwenAI/kglab/issues/160) regarding NumPy (>= 1.19.4) and [TensorFlow 2+](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/pip_package/setup.py) (~-1.19.2)


<details>
  <summary>Using Docker</summary>

For a simple approach to running the tutorials, see use of _docker compose_:
<https://derwen.ai/docs/kgl/tutorial/#use-docker-compose>

Also, container images for each release are available on DockerHub:
<https://hub.docker.com/repository/docker/derwenai/kglab>

To build a container image and run it for the tutorials:
```bash
docker build --pull --rm -f "docker/Dockerfile" -t kglab:latest .
docker run -p 8888:8888 -it kglab
```

To build and run a container image for testing:
```bash
docker build --pull --rm -f "docker/testsuite.Dockerfile" -t kglabtest:latest .
docker run --rm -it kglabtest
```
</details>


<details>
  <summary>Build Instructions</summary>

<strong>
Note: unless you are contributing code and updates,
in most use cases won't need to build this package locally.
</strong>

Instead, simply install from
[PyPi](https://pypi.python.org/pypi/kglab)
or use [Conda](https://docs.conda.io/).

To set up the build environment locally, see the 
["Build Instructions"](https://derwen.ai/docs/kgl/build/)
section of the online documentation.
</details>


<details>
  <summary>Semantic Versioning</summary>

Before <strong>kglab</strong> reaches release <code>v1.0.0</code> the 
types and classes may undergo substantial changes and the project is 
not guaranteed to have a consistent API.

Even so, we'll try to minimize breaking changes.
We'll also be sure to provide careful notes.

See:
[changelog.txt](https://github.com/DerwenAI/kglab/blob/main/changelog.txt)
</details>


<details>
  <summary>Contributing Code</summary>

We welcome people getting involved as contributors to this open source
project!

For detailed instructions please see:
[CONTRIBUTING.md](https://github.com/DerwenAI/kglab/blob/main/CONTRIBUTING.md)
</details>


<img
 alt="illustration of a knowledge graph, plus laboratory glassware"
 src="https://raw.githubusercontent.com/DerwenAI/kglab/main/docs/assets/logo.png"
 width="231"
 />


## License and Copyright

Source code for **kglab** plus its logo, documentation, and examples
have an [MIT license](https://spdx.org/licenses/MIT.html) which is
succinct and simplifies use in commercial applications.

All materials herein are Copyright &copy; 2020-2022 Derwen, Inc.


## Attribution

Please use the following BibTeX entry for citing **kglab** if you use
it in your research or software.
Citations are helpful for the continued development and maintenance of
this library.

```bibtex
@software{kglab,
  author = {Paco Nathan},
  title = {{kglab: a simple abstraction layer in Python for building knowledge graphs}},
  year = 2020,
  publisher = {Derwen},
  doi = {10.5281/zenodo.4717287},
  url = {https://github.com/DerwenAI/kglab}
}
```


## Kudos

Many thanks to our open source [sponsors](https://github.com/sponsors/ceteri);
and to our contributors:
[@ceteri](https://github.com/ceteri),
[@dvsrepo](https://github.com/dvsrepo),
[@Ankush-Chander](https://github.com/Ankush-Chander),
[@louisguitton](https://github.com/louisguitton),
[@tomaarsen](https://github.com/tomaarsen),
[@Mec-iS](https://github.com/Mec-iS),
[@RishiKumarRay](https://github.com/RishiKumarRay),
[@ArenasGuerreroJulian](https://github.com/ArenasGuerreroJulian),
[@fils](https://github.com/fils),
[@gauravjaglan](https://github.com/gauravjaglan),
[@pebbie](https://github.com/pebbie),
[@CatChenal](https://github.com/CatChenal),
[@jake-aft](https://github.com/jake-aft),
[@dmoore247](https://github.com/dmoore247),
plus general support from [Derwen, Inc.](https://derwen.ai/);
the [Knowledge Graph Conference](https://www.knowledgegraph.tech/)
and [Connected Data World](https://connected-data.world/);
plus an even larger scope of [use cases](https://derwen.ai/docs/kgl/use_case/)
represented by their communities;
[Kubuntu Focus](https://kfocus.org/),
the [RAPIDS team @ NVIDIA](https://rapids.ai/),
[Gradient Flow](https://gradientflow.com/),
and
[Manning Publications](https://www.manning.com/).
