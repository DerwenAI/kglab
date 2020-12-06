import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kglab",
    version="0.1.4",
    author="Paco Nathan",
    author_email="paco@derwen.ai",
    description="A simple abstraction layer in Python for building and using knowledge graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/DerwenAI/kglab",
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
    install_requires=[
          "rdflib",
          "rdflib-jsonld",
          "pandas",
          "numpy",
          "pyarrow",
          "networkx",
          "python-dateutil",
          "pyvis",
          "matplotlib",
          "pslpython",
          "gensim",
          "pylev",
          "pyshacl",
    ],
    keywords="knowledge graph, graph algorithms, interactive visualization, inference, rdf, skos, owl, controlled vocabulary, managing namespaces, serialization, n3, turtle, json-ld, parquet, psl, probabilistic soft logic, sparql, shacl",
    license="MIT",
    zip_safe=False,
)
