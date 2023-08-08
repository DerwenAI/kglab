# Acknowledgements

<img src="../assets/nouns/community.png" alt="Community by Aneeque Ahmed from the Noun Project" />

## Contributors

Many thanks to our open source [sponsors](https://github.com/sponsors/ceteri);
and to our contributors:
[@dvsrepo](https://github.com/dvsrepo),
[@Ankush-Chander](https://github.com/Ankush-Chander),
[@louisguitton](https://github.com/louisguitton),
[@tomaarsen](https://github.com/tomaarsen),
[@Mec-iS](https://github.com/Mec-iS),
[@jake-aft](https://github.com/jake-aft),
[@Tpt](https://github.com/Tpt),
[@ArenasGuerreroJulian](https://github.com/ArenasGuerreroJulian),
[@fils](https://github.com/fils),
[@cutterkom](https://github.com/cutterkom),
[@RishiKumarRay](https://github.com/RishiKumarRay),
[@gauravjaglan](https://github.com/gauravjaglan),
[@pebbie](https://github.com/pebbie),
[@CatChenal](https://github.com/CatChenal),
[@dmoore247](https://github.com/dmoore247);
plus general support from [Derwen, Inc.](https://derwen.ai/);
the [Knowledge Graph Conference](https://www.knowledgegraph.tech/)
and [Connected Data World](https://connected-data.world/)
plus an even larger scope of [use cases](../use_case/) represented by their communities;
[Kubuntu Focus](https://kfocus.org/),
the [RAPIDS team @ NVIDIA](https://rapids.ai/),
[Gradient Flow](https://gradientflow.com/),
and
[Manning Publications](https://www.manning.com/).


## Project Lead

[Paco Nathan](https://derwen.ai/paco)
is lead committer on **kglab** and lead author for its documentation and tutorial.
By day he's the Managing Partner at [Derwen, Inc.](https://derwen.ai/)
Paco's formal background is in 
Mathematics (advisor: [Richard Cottle](https://engineering.stanford.edu/people/richard-cottle))
and
Computer Science (advisor: [Douglas Lenat](https://en.wikipedia.org/wiki/Douglas_Lenat)),
with additional work in Design and Linguistics.
His business experience includes: 
Director, VP, and CTO positions leading data teams and machine learning projects;
former CTO/Board member at two publicly-traded tech firms on NASDAQ OTC:BB;
and an equity partner at [Amplify Partners](https://derwen.ai/s/hcxhybks9nbh).
Cited in 2015 as one of the 
[Top 30 People in Big Data and Analytics](http://www.kdnuggets.com/2015/02/top-30-people-big-data-analytics.html)
by Innovation Enterprise.

  * ~40 years tech industry experience, ranging from Bell Labs
    to early-stage start-ups
  * 7+ years R&D in *neural networks* (incl. h/w accelerators) during 1980-90s
  * early "guinea pig" for Amazon AWS (2006), who led the first
    large-scale Hadoop use case on [cloud computing](../glossary/#cloud-computing) (2008)
  * former Director, Community Evangelism at Databricks (2014-2015) for
    [Apache Spark](https://spark.apache.org/)
  * lead committer on [PyTextRank](https://derwen.ai/s/xdw563z8b4gj) ([spaCy](https://spacy.io/) pipeline);
    open source community work on 
    [Jupyter](https://jupyter.org/),
    [Ray](https://ray.io/),
    [Cascading](https://www.cascading.org/)
  * consultant to enterprise organizations for [data strategy](../glossary/#data-strategy);
    advisor to several AI start-ups, including
    [Recognai](https://derwen.ai/s/hk4g),
    [KUNGFU.AI](https://derwen.ai/s/rwg8prbgqp36)

As an author/speaker/instructor, Paco has taught many people (+9000) 
in industry across a range of topics –
[*data science*](../glossary/#data-science),
[*natural language*](../glossary/#natural-language),
[*cloud computing*](../glossary/#cloud-computing),
[*computable content*](../glossary/#computable-content),
etc. –
and through guest lectures at 
Stanford, CMU, UC&nbsp;Berkeley,
U&nbsp;da&nbsp;Coruña, U&nbsp;Manchester,
KTH, NYU, GWU,
U&nbsp;Maryland, Cal&nbsp;Poly, UT/Austin,
Northeastern, U&nbsp;Virginia, CU&nbsp;Boulder.

<a href="https://stackoverflow.com/users/1698443/paco"><img src="https://stackoverflow.com/users/flair/1698443.png" width="208" height="58" alt="profile for Paco at Stack Overflow, Q&amp;A for professional and enthusiast programmers" title="profile for Paco at Stack Overflow, Q&amp;A for professional and enthusiast programmers"/></a>


## Attribution

Please use the following BibTeX entry for citing **kglab** if you use
it in your research or software:

```
@software{kglab,
  author = {Paco Nathan},
  title = {{kglab: a simple abstraction layer in Python for building knowledge graphs}},
  year = 2020,
  publisher = {Derwen},
  doi = {10.5281/zenodo.6360664},
  url = {https://github.com/DerwenAI/kglab}
}
```

**DOI:** <https://doi.org/10.5281/zenodo.6360664>


## License and Copyright

Source code for **kglab** plus its logo, documentation, and examples
have an [MIT license](https://spdx.org/licenses/MIT.html) which is
succinct and simplifies use in commercial applications.

All materials herein are Copyright &copy; 2020-2023 Derwen, Inc.

[![logo for Derwen, Inc.](https://derwen.ai/static/block_logo.png)](https://derwen.ai/)


## Production Use Cases

  * [Derwen](https://derwen.ai/) and its client projects


## Similar Projects

See also:

  * [PheKnowLator](https://github.com/callahantiff/PheKnowLator)
    * *pro:* quite similar to **kglab** in intent; well-written code; sophisticated, opinionate build of biomedical KGs
    * *con:* less integration with data science tools or distributed systems
  * [GraphScope](https://github.com/alibaba/GraphScope)
    * *pro:* loads of features, excellent support, broad adoption
    * *con:* less of a *library* more of a *client/server* architecture; aims to reinvent instead of integrating
  * [LynxKite](https://lynxkite.com/)
    * *pro:* loads of features, lots of adoption
    * *con:* complex tech stack, combines Py/Java/Go; AGPL less-than-business-friendly for production apps
  * [KGTK](https://github.com/usc-isi-i2/kgtk)
    * *pro:* many excellent examples, well-documented in Jupyter notebooks
    * *con:* mostly a CLI tool, primarily based on TSV data
  * [zincbase](https://github.com/complexdb/zincbase)
    * *pro:* probabilistic graph measures, complex simulation suite, leverages GPUs
    * *con:* lacks interchange with RDF or other standard formats

In general, check
<https://github.com/pysemtec/semantic-python-overview> for excellent
curated listings of open source semantic technologies in Python.
