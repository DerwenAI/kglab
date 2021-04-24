# Dependencies

<img src="../assets/nouns/api.png" alt="API by Adnen Kadri from the Noun Project" />

The **kglab** package requires [Python 3.6+](https://www.python.org/downloads/).

Package dependencies as defined in
[`requirements.txt`](https://github.com/DerwenAI/kglab/blob/main/requirements.txt)
include:

- [chocolate](https://github.com/seungjaeryanlee/chocolate)
- [csvwlib](https://github.com/DerwenAI/csvwlib)
- [fsspec](https://filesystem-spec.readthedocs.io/)[^1]
- [gcsfs](https://gcsfs.readthedocs.io/)
- [gensim](https://radimrehurek.com/gensim/)
- [icecream](https://github.com/gruns/icecream)
- [matplotlib](https://matplotlib.org/)
- [NetworkX](https://networkx.org/)
- [NumPy](https://numpy.org/)
- [OWL-RL](https://owl-rl.readthedocs.io/)
- [pandas](https://pandas.pydata.org/)
- [pslpython](https://psl.linqs.org/)
- [pyarrow](https://arrow.apache.org/)
- [pylev](https://github.com/toastdriven/pylev)
- [pynvml](https://github.com/gpuopenanalytics/pynvml)
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [python-dateutil](https://dateutil.readthedocs.io/)
- [pyvis](https://pyvis.readthedocs.io/)
- [RDFlib](https://rdflib.readthedocs.io/)
- [rdflib-json](https://github.com/RDFLib/rdflib-jsonld)
- [requests](https://requests.readthedocs.io/)
- [scikit-learn](https://scikit-learn.org/stable/)
- [statsmodels](https://www.statsmodels.org/)
- [torch](https://pytorch.org/)
- [tqdm](https://tqdm.github.io/)
- [urlpath](https://github.com/chrono-meter/urlpath)


## NVidia GPU support

Additional package dependencies are required for GPU support through 
[RAPIDS](https://rapids.ai/) and must be installed separately:

- [cuDF](https://docs.rapids.ai/api/cudf/stable/api.html)
- [cuGraph](https://docs.rapids.ai/api/cugraph/stable/api.html)

These require use of `conda` and we strongly recommend that you
determine the correct configuration via the 
[release selector](https://rapids.ai/start.html#get-rapids).


## iGraph support

Since there are difficulties getting `igraph` to install correctly
across different environments, it is not included as a direct
dependency.
Instead you'll need to install the following packages separately:

- [cairocffi](https://cairocffi.readthedocs.io/)
- [leidenalg](https://leidenalg.readthedocs.io/)
- [python-igraph](https://igraph.org/python/)


[^1]: You may need to [install extra dependencies](https://filesystem-spec.readthedocs.io/en/latest/index.html?highlight=extra#installation) for `fsspec` since not all included filesystems are usable by default. Support for Amazon S3 and Google GCS are installed by default. See the `extras_require` dict in <https://github.com/intake/filesystem_spec/blob/master/setup.py>
