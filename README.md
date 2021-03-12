# kglab

[![DOI](https://zenodo.org/badge/307214458.svg)](https://zenodo.org/badge/latestdoi/307214458)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/DerwenAI/kglab?style=plastic)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

The **kglab** library provides a simple abstraction layer in Python
for building knowledge graphs.

Welcome to *graph-based data science*:
<https://derwen.ai/docs/kgl/>

> **SPECIAL REQUEST**:   
> Which features would you like in an open source Python library for building knowledge graphs?  
> Please add your suggestions through this survey:  
> https://forms.gle/FMHgtmxHYWocprMn6  
> This will help us prioritize the **kglab** roadmap.


## Getting Started

See the ["Getting Started"](https://derwen.ai/docs/kgl/start/)
section of the online documentation.

To install from [PyPi](https://pypi.python.org/pypi/kglab):
```
pip install kglab
```

If you work directly from this Git repo, be sure to install the 
dependencies as well:
```
pip install -r requirements.txt
```

Then to use the library with a simple use case:
```
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
print("```")
print(ttl[:999])
print("```")
```

See the **tutorial notebooks** in the `examples` subdirectory for
sample code and patterns to use in integrating **kglab** with other
graph libraries in Python:
<https://derwen.ai/docs/kgl/tutorial/>


## Semantic Versioning

Before **kglab** reaches release `v1.0.0` the types and classes may
undergo substantial changes and the project is not guaranteed to have
a consistent API.
Even so, we will try to minimize breaking changes and provide careful
notes in the `changelog.txt` file.


## Contributing Code

We welcome people getting involved as contributors to this open source
project!
Please see the
[CONTRIBUTING.md](https://github.com/DerwenAI/kglab/blob/main/CONTRIBUTING.md)
file for instructions.


## Build Instructions

**Note: unless you are contributing code and updates,
in most use cases won't need to build this package locally.**

Instead, simply install from
[PyPi](https://pypi.python.org/pypi/kglab)
or [Conda](https://docs.conda.io/).

To set up the build environment locally, see the 
["Build Instructions"](https://derwen.ai/docs/kgl/build/)
section of the online documentation.

![illustration of a knowledge graph, plus laboratory glassware](https://raw.githubusercontent.com/DerwenAI/kglab/main/docs/assets/logo.png)


## License and Copyright

Source code for **kglab** plus its logo, documentation, and examples
have an [MIT license](https://spdx.org/licenses/MIT.html) which is
succinct and simplifies use in commercial applications.

All materials herein are Copyright &copy; 2020-2021 Derwen, Inc.


## Attribution

Please use the following BibTeX entry for citing **kglab** if you use
it in your research or software.
Citations are helpful for the continued development and maintenance of
this library.

```
@software{kglab,
  author = {Paco Nathan},
  title = {{kglab: a simple abstraction layer in Python for building knowledge graphs}},
  year = 2020,
  publisher = {Derwen},
  doi = {10.5281/zenodo.4602403},
  url = {https://github.com/DerwenAI/kglab}
}
```


## Kudos

Many thanks to our contributors:
[@ceteri](https://github.com/ceteri),
[@gauravjaglan](https://github.com/gauravjaglan),
[@louisguitton](https://github.com/louisguitton),
[@jake-aft](https://github.com/jake-aft),
[@dmoore247](https://github.com/dmoore247),
plus general support from [Derwen, Inc.](https://github.com/DerwenAI),
[KFocus](https://kfocus.org/),
the [NVidia RAPIDS team](https://rapids.ai/),
[Gradient Flow](https://gradientflow.com/),
the [KGC Community](https://github.com/KGConf),
[Connected Data London](https://connected-data.london/),
and
[Manning Publications](https://www.manning.com/).
