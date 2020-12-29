# kglab

The **kglab** library provides a simple abstraction layer in Python
for building knowledge graphs.
Welcome to *graph-based data science*.

> **SPECIAL REQUEST:**
> Which features would you like to see the most in an open source Python library for building and using knowledge graphs? Please add suggestions to this online survey: https://forms.gle/FMHgtmxHYWocprMn6  This will help us prioritize the roadmap for **kglab**.


## Getting Started

To install from [PyPi](https://pypi.python.org/pypi/kglab):
```
pip install kglab
```

If you work directly from this Git repo, be sure to install the 
dependencies as well:
```
pip install -r requirements.txt
```

Then to use the library with some simple use cases:
```
import kglab

# create a KnowledgeGraph object
kg = kglab.KnowledgeGraph()

# load RDF from a URL
kg.load_rdf("http://bigasterisk.com/foaf.rdf", format="xml")

# measure the graph
measure = kglab.Measure()
measure.measure_graph(kg)

print("edges: {}\n".format(measure.edge_count))
print("nodes: {}\n".format(measure.node_count))

# serialize as a string in "Turtle" TTL format
ttl = kg.save_rdf_text()
print("```")
print(ttl[:999])
print("```")
```

See the **tutorial notebooks** for sample code and patterns to use in
integrating `kglab` with other popular related libraries in Python:
<https://github.com/DerwenAI/kglab/blob/main/docs/tutorial.md>


### Dependencies

- [Python 3.6+](https://www.python.org/downloads/)
- [cairocffi](https://github.com/Kozea/cairocffi)
- [gensim](https://radimrehurek.com/gensim/)
- [GPUtil](https://github.com/anderskm/gputil)
- [leidenalg](https://github.com/vtraag/leidenalg)
- [matplotlib](https://matplotlib.org/)
- [NetworkX](https://networkx.org/)
- [NumPy](https://numpy.org/)
- [OWL-RL](https://github.com/RDFLib/OWL-RL)
- [pandas](https://pandas.pydata.org/)
- [pslpython](https://psl.linqs.org/)
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [pyarrow](https://arrow.apache.org/)
- [pylev](https://github.com/toastdriven/pylev)
- [python-dateutil](https://pypi.org/project/python-dateutil/)
- [python-igraph](https://igraph.org/python/)
- [pyvis](https://pyvis.readthedocs.io/)
- [RDFlib](https://rdflib.readthedocs.io/)
- [rdflib-json](https://github.com/RDFLib/rdflib-jsonld)


## Build Instructions

To set up the build environment locally:
```
pip install -r requirements_build.txt
```

You will also need to download
[`ChromeDriver`](https://chromedriver.chromium.org/downloads) 
for your version of the `Chrome` brower, saved as `chromedriver` in this directory.

This project uses `typing` and [`mypy`](https://mypy.readthedocs.io/) for *type checking*.
To run type checking:
```
mypy kglab/*.py
```

This project uses `unittest` and [`coverage`](https://coverage.readthedocs.io/) for *unit test* coverage. 
Source for unit tests is in the `test.py` module.
To run unit tests:
```
coverage run -m unittest discover
```

To generate a coverage report and upload it to the `codecov.io`
reporting site (if you have the token):
```
coverage report
bash <(curl -s https://codecov.io/bash) -t @.cc_token
```

Test coverage reports can be viewed at
<https://codecov.io/gh/DerwenAI/kglab>

To generate documentation pages, this project uses:

  * [`MkDocs`](https://www.mkdocs.org/)
  * [`makedocs-material`](https://squidfunk.github.io/mkdocs-material/)
  * [`Jupyter`](https://jupyter.org/install)
  * [`nbconvert`](https://nbconvert.readthedocs.io/)
  * [`Selenium`](https://selenium-python.readthedocs.io/)
  * [`Chrome`](https://www.google.com/chrome/)
  * [`Flask`](https://flask.palletsprojects.com/)

Source for documentation is in the `docs` subdirectory.
To build the documentation:
```
./nb_md.sh
./pkg_doc.py docs/ref.md
mkdocs build
```

To preview the generated microsite locally:
```
./preview.py
```

Then browse to <http://localhost:8000> to review the generated
documentation.


To update the [release on PyPi](https://pypi.org/project/kglab/):
```
./push_pypi.sh
```


---

[![kg+lab](https://github.com/DerwenAI/kglab/blob/main/docs/illo/kglab.png)](https://github.com/DerwenAI/kglab/blob/main/docs/illo/kglab.png)

## Production Use Cases

  * [Derwen](https://derwen.ai/) and its client projects


## Similar Projects

See also:

  * [zincbase](https://github.com/complexdb/zincbase)
    * *pro:* probabilistic graph measures, complex simulation suite, leverages GPUs
    * *con:* lacks interchange with RDF or other standard formats
  * [KGTK](https://github.com/usc-isi-i2/kgtk)
    * *pro:* many excellent examples, well-documented in Jupyter notebooks
    * *con:* mostly a CLI tool, primarily based on TSV data


## Attribution

Source code for **kglab** plus its logo, documentation, and examples
have an [MIT license](https://spdx.org/licenses/MIT.html) which is
succinct and simplifies use in commercial applications.

All materials herein are Copyright (c) 2020-2021 Derwen, Inc.

Please use the following BibTeX entry for citing **kglab** if you use it in your research or software.
Citations are helpful for the continued development and maintenance of this library.

```
@software{kglab,
  author = {Paco Nathan},
  title = {{kglab: a simple abstraction layer in Python for building knowledge graphs}},
  year = 2020,
  publisher = {Derwen},
  url = {https://github.com/DerwenAI/kglab}
}
```


## Kudos

Many thanks to our contributors:
[@jake-aft](https://github.com/jake-aft),
[@dmoore247](https://github.com/dmoore247),
plus general support from [Derwen, Inc.](https://derwen.ai/)
and [The Knowledge Graph Conference](https://www.knowledgegraph.tech/).
