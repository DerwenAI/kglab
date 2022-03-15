# type: ignore

import importlib.util
import pathlib
import setuptools
import typing


KEYWORDS = [
    "controlled vocabulary",
    "cugraph",
    "deep learning",
    "embedding",
    "gpu",
    "graph algorithms",
    "igraph",
    "inference",
    "interactive visualization",
    "json-ld",
    "knowledge graph",
    "managing namespaces",
    "morph-kgc",
    "n3",
    "networkx",
    "owl",
    "pandas",
    "parquet",
    "probabilistic soft logic",
    "psl",
    "pyvis",
    "rapids",
    "rdf",
    "rml",
    "roam research",
    "serialization",
    "shacl",
    "skos",
    "sparql",
    "statistical relational learning",
    "topology",
    "turtle",
    "validation",
    ]


def parse_requirements_file (
    filename: str,
    ) -> typing.List[ str ]:
    """read and parse a Python `requirements.txt` file, returning as a list of strings"""
    with pathlib.Path(filename).open() as f:
        results: list = [
            l.strip().replace(" ", "").split("#")[0]
            for l in f.readlines()
        ]

        return results


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("kglab.version", "kglab/version.py")
    kglab_version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kglab_version)
    kglab_version._check_version()  # pylint: disable=W0212

    base_packages = parse_requirements_file("requirements.txt")
    docs_packages = parse_requirements_file("requirements-dev.txt")
    tut_packages = parse_requirements_file("requirements-tut.txt")

    setuptools.setup(
        name = "kglab",
        version = kglab_version.__version__,

        license = "MIT",
        description = "A simple abstraction layer in Python for building knowledge graphs",
        long_description = pathlib.Path("README.md").read_text(),
        long_description_content_type = "text/markdown",

        python_requires = ">=" + kglab_version._versify(kglab_version.MIN_PY_VERSION),  # pylint: disable=W0212
        packages = setuptools.find_packages(exclude=[ "docs", "examples" ]),
        zip_safe = False,

        install_requires = base_packages,
        extras_require = {
            "base": base_packages,
            "docs": docs_packages,
            "tutorial": tut_packages,
        },

        author = "Paco Nathan",
        author_email = "paco@derwen.ai",

        keywords = ", ".join(KEYWORDS),
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: MIT License",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Human Machine Interfaces",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Text Processing :: Indexing",
            ],

        url = "https://derwen.ai/docs/kgl/",
        project_urls = {
            "DOI": "https://doi.org/10.5281/zenodo.6360664",
            "Community Survey": "https://forms.gle/FMHgtmxHYWocprMn6",
            "Discussion Forum": "https://www.linkedin.com/groups/6725785/",
            "DockerHub": "https://hub.docker.com/r/derwenai/kglab",
            "Hands-on Tutorial": "https://derwen.ai/docs/kgl/tutorial/",
            "Issue Tracker": "https://github.com/DerwenAI/kglab/issues",
            "Source Code": "https://github.com/DerwenAI/kglab",
        },

        entry_points = {
            "rdf.plugins.store": [
                "kglab = kglab:PropertyStore",
            ],
        },
    )
