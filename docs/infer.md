# Inference

Once you have data organized as a graph, there are several ways to perform *inference*, which is a core capability of AI systems.

A general definition for inference is:
> a conclusion reached on the basis of evidence and reasoning

For the W3C perspective, see 
<https://www.w3.org/standards/semanticweb/inference>

  * improve the quality of data integration
  * discover new relationships
  * indentify potential inconsistencies in the (integrated) data

The integrations within `kglab` to support inference capabilities may be combined to leverage each other's relative strengths, along with potential use of *human-in-the-loop* approaches such as *active learning* and *weak supervision*.
These integrations include:

  * Efforts by [`owlrl`](https://github.com/RDFLib/OWL-RL/) toward [OWL 2 RL](https://www.w3.org/TR/owl2-profiles/#OWL_2_RL) *reasoning*
    * adding axiomatic triples based on 	[OWL](https://www.w3.org/TR/owl-features/) properties
    * forward chaining using [RDF Schema](https://www.w3.org/TR/rdf-schema/)

  * Expanding the semantic relationships in [SKOS](https://www.w3.org/TR/skos-reference/#L881) for inference based on [hierarchical transitivity and associativity](https://www.w3.org/TR/skos-primer/#secrel)

  * Machine learing models in general, and neural networks in particular can be viewed as means for [*function approximation*](https://en.wikipedia.org/wiki/Function_approximation), i.e., generalizing from data patterns to predict values or labels.  In that sense, *graph embedding* approaches such as `node2vec` provides inference capabilities.

  * The *probabilisic soft logic* in [`pslpython`](https://psl.linqs.org/) evaluates systems of rules to infer predicates.  

  * Using [`pgmpy`](https://pgmpy.org/) for *statisical inference* in [Bayesian networks](https://en.wikipedia.org/wiki/Bayesian_network).