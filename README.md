# kglab

UNDER CONSTRUCTION - prior to "KG 101" tutorial at https://www.knowledgeconnexions.world/talks/kg-101/

See [wiki](https://github.com/DerwenAI/kglab/wiki) for further details

## Outline

1. Building a graph in RDF using `rdflib`
  * [`ex01_0.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_0.ipynb)
    * examine the dataset
  * [`ex01_1.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_1.ipynb)
    * construct a graph from RDF triples
    * using multiple namespaces
    * proper handling of literals
    * seralization to strings and files using `Turtle` and `JSON-LD`
2. Leveraging the `kglab` abstraction layer
  * [`ex01_2.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_2.ipynb)
    * construct and serialize the same graph using  `kglab`
3. Interactive graph visualization with `pyvis`
  * [`ex01_3.ipynb`](https://github.com/DerwenAI/kglab/blob/main/ex01_3.ipynb)
    * render triples as an interactive graph
