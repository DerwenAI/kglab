# Dependencies

<img src="../assets/nouns/api.png" alt="API by Adnen Kadri from the Noun Project" />

The **kglab** package requires [Python 3.7+](https://www.python.org/downloads/).

## Base Support

Package dependencies as defined in
[`requirements.txt`](https://github.com/DerwenAI/kglab/blob/main/requirements.txt)
include:

- [chocolate](https://github.com/seungjaeryanlee/chocolate)
- [csvwlib](https://github.com/DerwenAI/csvwlib)
- [cryptography](https://cryptography.io/)
- [decorator](https://github.com/micheles/decorator)
- [fsspec](https://filesystem-spec.readthedocs.io/)[^1]
- [gcsfs](https://gcsfs.readthedocs.io/)
- [icecream](https://github.com/gruns/icecream)
- [Morph-KGC](https://github.com/oeg-upm/morph-kgc)
- [NetworkX](https://networkx.org/)
- [NumPy](https://numpy.org/)[^2]
- [OWL-RL](https://owl-rl.readthedocs.io/)
- [Oxrdflib](https://github.com/oxigraph/oxrdflib)
- [pandas](https://pandas.pydata.org/)
- [pslpython](https://psl.linqs.org/)[^3]
- [pyarrow](https://arrow.apache.org/)
- [pynvml](https://github.com/gpuopenanalytics/pynvml)
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [python-dateutil](https://dateutil.readthedocs.io/)
- [pyvis](https://pyvis.readthedocs.io/)
- [RDFlib](https://rdflib.readthedocs.io/)
- [requests](https://requests.readthedocs.io/)
- [statsmodels](https://www.statsmodels.org/)
- [tqdm](https://tqdm.github.io/)
- [urlpath](https://github.com/chrono-meter/urlpath)


## NVIDIA GPU support

Additional package dependencies are required for GPU support through 
[RAPIDS](https://rapids.ai/) and must be installed separately:

- [cuDF](https://docs.rapids.ai/api/cudf/stable/api.html)
- [cuGraph](https://docs.rapids.ai/api/cugraph/stable/api.html)

These require use of `conda` as a base, and we strongly recommend
using the [release selector](https://rapids.ai/start.html#get-rapids).
to determine the correct configuration

Then use `pip` to install the other **kglab** dependencies atop
that base `conda` environment.


## iGraph support

Since there are difficulties getting `igraph` to install correctly
across different environments, it is not included as a direct
dependency.
Instead you'll need to install the following packages separately:

- [cairocffi](https://cairocffi.readthedocs.io/)
- [leidenalg](https://leidenalg.readthedocs.io/)
- [igraph](https://igraph.org/python/)


## Troubleshooting

### PEP 517

If you are using `pip` you may run into the dreaded
[`PEP 517`](https://www.python.org/dev/peps/pep-0517/)
errors when installing libraries.

Problems tend to be encountered with particular dependencies such as
`statsmodels`, `multidict`, `yarl`, and so on, with error messages
similar to:

> ERROR: Could not build wheels for **foobar** which use PEP 517  
> and cannot be installed directly

To be clear, this is partly due to the fact that both Windows and
macOS cut corners on their attempts to balance being both "consumer
products" and actual operating systems.
Consequently their compiler environments can became gnarled messes –
especially when you must work with a wide range of machine learning
libraries, which tend to stress this point.

To be blunt, using Linux (e.g., Ubuntu, etc.) helps if you're serious
about software engineering.

The best advice we can give to help troubleshoot this constellation 
of errors is that `PEP 517` does not play well with Python
[virtual environments](https://docs.python.org/3/tutorial/venv.html).
If you get stuck with installation errors, find a way around using a
virtual environment.

You can also try to use the following approach to pre-load the
troublesome dependencies, although YMMV:

```
pip install statsmodels  --no-binary :all:
```

This is be no means a simple matter to resolve.
For more details about root issues encountered when building Python
packages, the following discussions are highly recommended:

  * <https://twitter.com/wesmckinn/status/1148350953793490944>
  * <https://discuss.python.org/t/pep-517-and-projects-that-cant-install-via-wheels/791>
  * <https://labs.quansight.org/blog/2021/01/python-packaging-brainstorm/>


[^1]: You may need to [install extra dependencies](https://filesystem-spec.readthedocs.io/en/latest/index.html?highlight=extra#installation) for `fsspec` since not all included filesystems are usable by default. Support for Amazon S3 and Google GCS are installed by default. See the `extras_require` dict in <https://github.com/intake/filesystem_spec/blob/master/setup.py>

[^2]: There are [known version conflicts](https://github.com/DerwenAI/kglab/issues/160) regarding NumPy (>= 1.19.4) and [TensorFlow 2+](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/pip_package/setup.py) (~-1.19.2)

[^3]: You need to have a Java JDK installed to run PSL.
