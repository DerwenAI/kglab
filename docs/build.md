# Build Instructions

<img src="../assets/nouns/api.png" alt="API by Adnen Kadri from the Noun Project" />

!!! note
    In most cases you won't need to build this package locally.

Unless you're doing development work on the **kglab** library itself,
simply install based on the instructions in
["Getting Started"](https://derwen.ai/docs/kgl/start/).


## Setup

To set up the build environment locally:
```
python3 -m pip install -r requirements-dev.txt
```

We use *pre-commit hooks* based on [`pre-commit`](https://pre-commit.com/)
and to configure that locally:
```
pre-commit install
git config --local core.hooksPath .git/hooks/
```


## Type Checking

The pre-commit hooks use
[`typing`](https://docs.python.org/3/library/typing.html)
and
[`mypy`](https://mypy.readthedocs.io/)
for *type checking*.
To run these tests specifically:
```
mypy kglab/*.py
```


## Code Checking

The pre-commit hooks use
[`pylint`](https://www.pylint.org/)
for *code checking*.
To run these tests specifically:
```
pylint kglab/*.py
```


## Spelling Errors

The pre-commit hooks use
[`codespell`](https://github.com/codespell-project/codespell)
to check for *spelling errors*.
To run these tests specifically:
```
codespell kglab/*.py *.md docs/*.md
```


## Security Issues

The pre-commit hooks use
[`bandit`](https://bandit.readthedocs.io/)
to check for *security issues*.
To run these tests specifically:
```
bandit kglab/*.py
```


## Test Coverage

This project uses `unittest` and 
[`coverage`](https://coverage.readthedocs.io/)
for *unit test* coverage. 
Source for unit tests is in the 
[`test.py`](https://github.com/DerwenAI/kglab/blob/main/test.py)
module.

To run unit tests:
```
coverage run -m unittest discover
```

To generate a coverage report and (providing you have the access
token) upload it to the `codecov.io` reporting site:
```
coverage report
bash <(curl -s https://codecov.io/bash) -t @.cc_token
```

Test coverage reports can be viewed at
<https://codecov.io/gh/DerwenAI/kglab>


## Online Documentation

To generate documentation pages, this project uses:

  * [`MkDocs`](https://www.mkdocs.org/)
  * [`makedocs-material`](https://squidfunk.github.io/mkdocs-material/)
  * [`pymdown-extensions`](https://facelessuser.github.io/pymdown-extensions/)
  * [`MathJax`](https://www.mathjax.org/)
  * [`Jupyter`](https://jupyter.org/install)
  * [`nbconvert`](https://nbconvert.readthedocs.io/)
  * [`mknotebooks`](https://github.com/greenape/mknotebooks)
  * [`Selenium`](https://selenium-python.readthedocs.io/)
  * [`Chrome`](https://www.google.com/chrome/)
  * [`Flask`](https://flask.palletsprojects.com/)

Source for the documentation is in the 
[`docs`](https://github.com/DerwenAI/kglab/tree/main/docs)
subdirectory.

To build the documentation:
```
./bin/nb_md.sh
./pkg_doc.py docs/ref.md
mkdocs build
```

To preview the generated microsite locally:
```
./bin/preview.py
```

Then browse to <http://localhost:8000> to review the generated
documentation.

To package the generated microsite for deployment on a
Flask/WSGI server:
```
tar cvzf kgl.tgz site/
```


## Package Release

To update the [release on PyPi](https://pypi.org/project/kglab/):
```
./bin/push_pypi.sh
```

You can use `grayskull` to generate a
[conda-forge recipe](https://github.com/conda-forge/staged-recipes):
```
grayskull pypi kglab
mv kglab/meta.yaml ./
```
