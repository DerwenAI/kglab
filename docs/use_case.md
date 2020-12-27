# Use Cases

For several KG projects, we kept reusing a similar working set of libraries:

  * [`rdflib`](https://rdflib.readthedocs.io/)
  * [`networkx`](https://networkx.org/)
  * [`pyvis`](https://pyvis.readthedocs.io/)
  * [`pytextrank`](https://pypi.org/project/pytextrank/)
  * [`richcontext.scholapi`](https://pypi.org/project/richcontext-scholapi/)
  * [`skosify`](https://skosify.readthedocs.io/)

Each of these libraries provides a useful piece of the puzzle when you need
to leverage *knowledge representation*, *graph algorithms*, *entity linking*,
*interactive visualization*, *metadata queries*, *axioms*, etc.
However, some of them are relatively low-level (e.g., `rdflib`) or perhaps not
maintained as much (e.g., `skosify`) and there are challenges integrating them.
Challenges we kept having to reinvent work-arounds to resolve.

There are general operations that one must perform on knowledge graphs:

  * building triples
  * managing a mix of namespaces
  * serialization to/from multiple formats
  * queries
  * interactive visualization
  * transitivity and other forms of enriching a graph
  * graph algorithms
  * inference (e.g., PSL, Bayesian Networks, Causal, MLN, etc.)
  * quality assurance (e.g., axioms)
  * parallel processing across a cluster
  * embedding (deep learning integration)
  * other ML integrations

