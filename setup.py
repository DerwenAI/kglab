# type: ignore

import importlib.util
import pathlib
import setuptools
import typing


KEYWORDS = [
    "knowledge graph",
    "graph algorithms",
    "interactive visualization",
    "validation",
    "inference",
    "rdf",
    "owl",
    "skos",
    "sparql",
    "shacl",
    "controlled vocabulary",
    "managing namespaces",
    "serialization",
    "n3",
    "turtle",
    "json-ld",
    "parquet",
    "psl",
    "probabilistic soft logic",
    "pandas",
    "roam research",
    "networkx",
    "igraph",
    "pytorch",
    "embedding",
    "deep learning",
    ]


def parse_requirements_file (filename: str) -> typing.List:
    """read and parse a Python `requirements.txt` file, returning as a list of str"""
    with pathlib.Path(filename).open() as f:
        return [ l.strip().replace(" ", "") for l in f.readlines() ]


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("kglab.version", "kglab/version.py")
    kglab_version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kglab_version)
    kglab_version._check_version()  # pylint: disable=W0212

    base_packages = parse_requirements_file("requirements.txt")
    docs_packages = parse_requirements_file("requirements-dev.txt")

    setuptools.setup(
        name = "kglab",
        version = kglab_version.__version__,

        python_requires = ">=" + kglab_version._versify(kglab_version.MIN_PY_VERSION),  # pylint: disable=W0212
        packages = setuptools.find_packages(exclude=[ "docs", "examples" ]),
        install_requires = base_packages,
        extras_require = {
            "base": base_packages,
            "docs": docs_packages,
            },

        author = "Paco Nathan",
        author_email = "paco@derwen.ai",
        license = "MIT",

        description = "A simple abstraction layer in Python for building knowledge graphs",
        long_description = pathlib.Path("README.md").read_text(),
        long_description_content_type = "text/markdown",

        keywords = ", ".join(KEYWORDS),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Human Machine Interfaces",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Text Processing :: Indexing",
            ],

        url = "https://derwen.ai/docs/kgl/",
        project_urls = {
            "Source Code": "https://github.com/DerwenAI/kglab",
            "Issue Tracker": "https://github.com/DerwenAI/kglab/issues",
            "Community Survey": "https://forms.gle/FMHgtmxHYWocprMn6",
            "Discussion Forum": "https://www.linkedin.com/groups/6725785/",
            "Hands-on Tutorial": "https://derwen.ai/docs/kgl/tutorial/",
            },

        zip_safe = False,
        )
