# kglab

The **kglab** library provides a simple abstraction layer in Python
for building knowledge graphs.

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

Then to use the library, the simplest form is:
```
import kglab

kg = kglab.KnowledgeGraph()
```

See the tutorial notebooks for sample code and patterns to use in
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


## Documentation

We use [MkDocs](https://www.mkdocs.org/) and [mknotebooks](https://github.com/greenape/mknotebooks)
to generate documentation pages.
Source is in the `docs` subdirectory.

To set up your MkDocs environment locally:
```
pip install mkdocs-material
pip install mknotebooks
```

To rebuild the pages from Markdown:
```
mkdocs build
```

To launch the MkDocs microsite locally:
```
mkdocs serve
```

Then browse <http://localhost:8000>


## Build Instructions

This project uses `typing` and [`mypy`](https://mypy.readthedocs.io/) for *type checking*.
To install:
```
pip install mypy
```

To run type checking:
```
mypy kglab/*.py
```

To update the [PyPi release](https://pypi.org/project/kglab/):
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

**kglab** has an [MIT](https://spdx.org/licenses/MIT.html) license,
which is succinct and simplifies use in commercial applications.

Please use the following BibTeX entry for citing **kglab** if you use it in your research or software.
Citations are helpful for the continued development and maintenance of this library.

```
@software{kglab,
  author = {Paco Nathan},
  title = {{kglab: a simple abstraction layer in Python for building and using knowledge graphs}},
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
