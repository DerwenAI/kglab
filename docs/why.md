# Why create another graph library?

The `kglab` library is a simple *abstraction layer* in Python for building and using knowledge graphs.

> FAQ: Why build yet another graph library, when there are already so many available?

There were several initial intentions for `kglab`, including:
  
  * Integrate many popular graph-based libraries with [PyData](https://pydata.org/)-esque data science tools including [`pandas`](https://pandas.pydata.org/), [`scikit-learn`](https://scikit-learn.org/stable/), [`NumPy`](https://numpy.org/), and so on – as an idiomatic Python *library*, not another graph database *framework*.

  * Incorporate graph-based methods and semantic technologies into [`spaCy`](https://spacy.io/) pipelines, e.g., through [`pytextrank`](https://github.com/DerwenAI/pytextrank/), in addition to customized natural language pipelines such as [`biome.text`](https://www.recogn.ai/biome-text/).
  
  * Interface efficiently with *big data* tools and practices such as [`Apache Arrow`](https://arrow.apache.org/), [`Apache Parquet`](https://parquet.apache.org/), [`Apache Spark`](http://spark.apache.org/), [`Ray`](https://ray.io/), and so on – to support scalable graph-based work in data engineering and distributed infrastructure.

  * Explore "hybrid" approaches that combine machine learning with symbolic, rule-based processing – including probabilistic methods.
    
  * Develop material for a follow-up edition (seven years later) of [*Just Enough Math*](https://derwen.ai/jem) – since the field of *data science* has changed so much.

