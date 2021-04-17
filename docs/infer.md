# Inference capabilities

<img src="../assets/nouns/concepts.png" alt="concept by Nithinan Tatah from the Noun Project" />

Once you have data organized as a graph, there are several ways to
perform *inference*, which is a core capability of AI systems.

A general definition for inference is:
> a conclusion reached on the basis of evidence and reasoning

For the W3C perspective, see 
<https://www.w3.org/standards/semanticweb/inference>

  * improve the quality of data integration
  * discover new relationships
  * identify potential inconsistencies in the (integrated) data

The integrations within **kglab** to support inference capabilities
may be combined to leverage each other's relative strengths, along
with potential use of *human-in-the-loop* (or "machine teaching")
approaches such as *active learning* and *weak supervision*.

These integrations include:

  * Efforts by [`owlrl`](https://github.com/RDFLib/OWL-RL/) toward [OWL 2 RL](https://www.w3.org/TR/owl2-profiles/#OWL_2_RL) *reasoning*
    * adding axiomatic triples based on 	[OWL](https://www.w3.org/TR/owl-features/) properties
    * forward chaining using [RDF Schema](https://www.w3.org/TR/rdf-schema/)

  * Expanding the semantic relationships in [SKOS](https://www.w3.org/TR/skos-reference/#L881) for inference based on [hierarchical transitivity and associativity](https://www.w3.org/TR/skos-primer/#secrel)

  * Machine learing models in general, and neural networks in particular can be viewed as means for [*function approximation*](https://en.wikipedia.org/wiki/Function_approximation), i.e., generalizing from data patterns to predict values or labels.  In that sense, *graph embedding* approaches such as `node2vec` provides inference capabilities.

  * The *probabilisic soft logic* in [`pslpython`](https://psl.linqs.org/) evaluates systems of rules to infer predicates.  

  * Using [`pgmpy`](https://pgmpy.org/) for *statistical inference* in [Bayesian networks](https://en.wikipedia.org/wiki/Bayesian_network).


## Statistical Relational Learning

There are several ways to work with graph-based data, including: SPARQL queries, graph algorithms traversals, ML embedding, etc.
These respective methods make trade-offs in terms of:

  * computational costs as the graph size scales
  * robustness when there is uncertainty or conflicting information in the graph
  * formalism (i.e., *analytic solutions*) vs. empirical approaches (i.e., data-driven, machine learning)

One way to visualize some of these trade-offs is in the following diagram:

<img src="https://github.com/DerwenAI/kglab/blob/main/docs/assets/tradeoffs.png?raw=true" width="400"/>

Note in the top/right corner of the diagram that a relatively formal category of graph-based approaches is called [*statistical relational learning*](../glossary/#statistical-relational-learning).
The gist is that so much of the *network analysis* that we want to perform can be describe mathematically as [*markov networks*](https://en.wikipedia.org/wiki/Markov_random_field), in terms of probabilistic models.
Sometimes these can be quite computationally expensive; for example, hedge funds on Wall Street tend to burn lots of cloud computing on markov models.
They are *robust* in terms of being able to work well even with lots of missing or conflicting data, and the *formalism* implies that we can infer mathematical guarantees from the analysis.
That's quite the opposite of deep learning models, which are great at predicting sequences of things, but terrible at providing guarantees.

Clearly, there's been much emphasis in industry recently that equates "artificial intelligence" with "deep learning", although we are also recognizing [*diminishing returns*](https://derwen.ai/s/zf43#33) for methods that rely purely on ever-larger data rates and ever-larger ML models.
One path forward will be to combine machine learning with use of *structured knowledge* (i.e., KGs) such that we can avoid "boiling the oceans" with purely data-driven approaches when in so many use cases we can leverage domain expertise.

One form of statistical relational learning called [*probabilistic soft logic*](../glossary/#probabilistic-soft-logic) (PSL) is essentially a kind of "fuzzy logic" for probabilistic graphs that has interesting computational qualities.
Whereas many kinds of formal graph analysis (e.g., "traveling salesman problem") are provably hard and quite expensive in practice, PSL can be solved with a *convex optimization* (e.g., like so many machine learning algorithms).

Consider this: we can describe "rules" about nodes and relations in a KG, then assign probabilities to specific instances of those rules that are found within our graph.
If the probabilities are all *zero* then the system is consistent.
As some of the assigned probabilities are increased, then some of the rules become inconsistent.
How high (i.e., optimal) of a set of probabilities can we assign while still keeping the system consistent?
Alternatively, if we apply a set of rules, then how "far away" (probabilistically speaking) is a graph from being logically consistent?

This comes in quite handy when we want to combine *semantic technologies* and *machine learning*, or rather when we have explicit rules plus lots of empirical data.
Data quality is a persistent problem, so we can leverage PSL to identify which parts of the graph seem the least "logically consistent", and therefore need some review and curation.