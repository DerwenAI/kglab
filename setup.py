import importlib.util
import pathlib
import setuptools
import sys
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
    "networkx",
    "igraph",
    ]


def parse_requirements_file (filename: str) -> typing.List:
    """read and parse a Python `requirements.txt` file, returning as a list of str"""
    with pathlib.Path(filename).open() as f:
        return [ l.strip().replace(" ", "") for l in f.readlines() ]


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("kglab.version", "kglab/version.py")
    kglab_version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kglab_version)
    kglab_version._check_version()

    base_packages = parse_requirements_file("requirements.txt")
    docs_packages = parse_requirements_file("requirements_build.txt")

    setuptools.setup(
        name = "kglab",
        version = "0.1.7",

        python_requires = ">=" + kglab_version._versify(kglab_version.MIN_PY_VERSION),
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
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Human Machine Interfaces",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Text Processing :: Indexing",
            ],

        url = "https://github.com/DerwenAI/kglab",
        project_urls = {
            "Bug Tracker": "https://github.com/DerwenAI/kglab/issues",
            "Documentation": "https://derwen.ai/docs/kgl/",
            "Source Code": "https://github.com/DerwenAI/kglab",
            },

        zip_safe = False,
        )
