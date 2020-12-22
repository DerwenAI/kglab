# What is a Knowledge Graph?

Gartner Research began to acknowledge the term [*knowledge graph*](https://derwen.ai/d/knowledge_graph) in 2018, and in mid-2020 described the importance of KGs for developing [AI applications](https://www.gartner.com/en/documents/3985680/how-to-build-knowledge-graphs-that-enable-ai-driven-ente).
However, it's unlikely that Gartner will acknowledge the breadth of industry adoption for KG approaches in enterprise data management.

To paraphrase [Natasha Noy](https://research.google/people/NatalyaNoy/), a research scientist at Google Research and one of the most highly-regarded practitioners in this field:

> An "enterprise knowledge graph" provides *ground truth* – or ["data context"]( http://cidrdb.org/cidr2017/papers/p111-hellerstein-cidr17.pdf) – through which we can reconcile our queries and other usage of many disparate data stores.
> For example, having *persistent identifiers* with other metadata attached is a great start.
> This also allows for multiple teams to be working concurrently, i.e., with less centralized control.

This is in contrast to the legacy notion of [*one size fits all*](https://en.wikipedia.org/wiki/One_size_fits_all) (OSFA), i.e., the best way to make data consistent is to import *all* of the data sources into a single data management system, with one individual who determines the schema and other data management rules.

In a world where organizations must be resilient in the face of abrupt changes, we must adapt more resilient means for reconciling data from a wide variety of sources: vendors, customers, partners, government agencies, standards bodies, and so on.
KGs provide means for a kind of *abstraction layer* to make the data cohere.
