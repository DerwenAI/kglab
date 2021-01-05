import setuptools
import sys

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


def parse_requirements_file (filename):
    with open(filename) as f:
        requires = [l.strip().split(" ")[0] for l in f.readlines() if l]

    return requires


if __name__ == "__main__":
    if sys.version_info[:2] < (3, 6):
        error = "kglab requires Python 3.6 or later (%d.%d detected). \n"
        sys.stderr.write(error.format(sys.version_info[:2]))
        sys.exit(1)

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="kglab",
        version="0.1.5",
        author="Paco Nathan",
        author_email="paco@derwen.ai",
        description="A simple abstraction layer in Python for building and using knowledge graphs",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/DerwenAI/kglab",
        project_urls={
            "Bug Tracker": "https://github.com/DerwenAI/kglab/issues",
            "Documentation": "https://derwen.ai/docs/kgl/",
            "Source Code": "https://github.com/DerwenAI/kglab",
            },
        packages=setuptools.find_packages(),
        classifiers=[
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
        python_requires=">=3.6",
        install_requires=parse_requirements_file("requirements.txt"),
        keywords=", ".join(KEYWORDS),
        license="MIT",
        zip_safe=False,
        )
