# Dependencies

The **kglab** package requires [Python 3.6+](https://www.python.org/downloads/).

Package dependencies as defined in
[`requirements.txt`](https://github.com/DerwenAI/kglab/blob/main/requirements.txt)
include:

- [cairocffi](https://cairocffi.readthedocs.io/)
- [chocolate](https://github.com/seungjaeryanlee/chocolate)
- [csvwlib](https://github.com/DerwenAI/csvwlib)
- [fsspec](https://filesystem-spec.readthedocs.io/)[^1]
- [gcsfs](https://gcsfs.readthedocs.io/)
- [gensim](https://radimrehurek.com/gensim/)
- [GPUtil](https://github.com/anderskm/gputil)
- [icecream](https://github.com/gruns/icecream)
- [leidenalg](https://leidenalg.readthedocs.io/)
- [matplotlib](https://matplotlib.org/)
- [NetworkX](https://networkx.org/)
- [NumPy](https://numpy.org/)
- [OWL-RL](https://owl-rl.readthedocs.io/)
- [pandas](https://pandas.pydata.org/)
- [pslpython](https://psl.linqs.org/)
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [pyarrow](https://arrow.apache.org/)
- [pylev](https://github.com/toastdriven/pylev)
- [python-dateutil](https://dateutil.readthedocs.io/)
- [python-igraph](https://igraph.org/python/)
- [pyvis](https://pyvis.readthedocs.io/)
- [RDFlib](https://rdflib.readthedocs.io/)
- [rdflib-json](https://github.com/RDFLib/rdflib-jsonld)
- [scikit-learn](https://scikit-learn.org/stable/)
- [urlpath](https://github.com/chrono-meter/urlpath)


[^1]: You may need to [install extra dependencies](https://filesystem-spec.readthedocs.io/en/latest/index.html?highlight=extra#installation) for `fsspec` since not all included filesystems are usable by default. Support for Amazon S3 and Google GCS are installed by default. See the `extras_require` dict in <https://github.com/intake/filesystem_spec/blob/master/setup.py>
