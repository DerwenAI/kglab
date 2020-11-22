import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kglab",
    version="0.1.1",
    author="Paco Nathan",
    author_email="paco@derwen.ai",
    description="Python wrapper for knowledge graph construction tools",
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
    python_requires=">=3.5",
    install_requires=[
          "grave",
          "matplotlib",
          "networkx",
          "pandas",
          "pslpython",
          "python-dateutil",
          "pyvis",
          "rdflib",
          "rdflib-jsonld",
    ],
    keywords="knowledge graph, graph algorithms, interactive visualization, rdf, skos, owl, controlled vocabulary, managing namespaces, serialization, n3, turtle, json-ld",
    license="MIT",
    zip_safe=False,
)
