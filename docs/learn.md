# A Grammar of Learning

Let's talk briefly about how to design and present learning materials.
What are we doing here?
In another sense, consider the following as a very brief exercise in
*design thinking*, focused on how to improve software documentation
and tutorials.

As described in the [guidance](#guidance) below, there's a growing
movement toward more structured approaches to how documentation gets
presented.
Arguably, a lack of quality or effectivenes in documentation creates
major impediments for open source libraries.
Much the same goes for tutorials, which are often written from the
perspective of someone who's already familiar with the material – thus
defeating its purpose for those who aren't.

Divio, Cloudflare, Stripe, and other firms have fostered *writing
cultures* internally, while applying more structured approaches to
presenting their learning materials externally.
That shouldn't be surprising: software developers tend to write in
volume – generally much more text than they produce as source code –
since the processing of planning projects and maintaining them over
time usually involves lots of written communications.
That said, good editing for developers' text is much less common.
That's why the examples set by Stripe and others are important.

Our team has iterated on these approaches, blending key insights and
practices from prior roles, to create design patterns for
documentation and tutorials.
The outline of this documentation follows these patterns.


## How to use these materials

The objective for these learning materials is to help people learn how
to leverage **kglab** effectively, gain confidence working with
graph-based data science, plus have examples to repurpose for their
own use cases.

You'll find a mix of topics throughout:
data science, business context, AI applications, data management, 
data strategy, design patterns, distributed systems 
– plus explorations of how to leverage the math, where appropriate.

This work builds on the ["Graph-Based Data
Science"](https://derwen.ai/s/kcgh) talks at conferences and meetups,
which experiment with the content – collecting feedback, critiques,
suggestions, etc.
The results eventually land here.

<img src="https://derwen.ai/docs/kgl/assets/learning.png" width="500" />

The intention is to make these materials useful to a wide audience.
So we provide multiple entry points, depending on what you need...


### Discovery

 > Design affordances for navigation, indexing, search, and recommendations.

Much effort has gone into making sure this material is thoroughly
hyper-linked together, to help with both navigation and indexing.
Even so, suggestions for improvement are highly welcomed!

The left sidebar provides an overall outline of sections, while the
right sidebar links to sections within the current section.

Start at any point, for whatever info is most immediately useful.

!!! note
    It may be helpful to run [JupyterLab](https://jupyterlab.readthedocs.io/) for the coding examples in one browser tab, while navigating through this documentation in another browser tab.

The search features implemented in documentation frameworks such as
[`MkDocs`](https://www.mkdocs.org/),
[`Sphinx`](https://www.sphinx-doc.org/en/master/),
etc., leave much to be desired.
Consequently the search features have been disabled here, for now,
while a replacement is in development.
Meanwhile, contextual links based on the KG-powered [Derwen
search/discovery](https://derwen.ai/d/) services help provide
recommendations.
More of that is getting integrated directly into this documentation.


### HowTo

> Present problem-oriented directions for getting things done.

  * [*Getting Started*](../start/) with enough code to start.
  * Specific "howto" articles, generated from notebooks.


### Tutorial

> Learning-oriented practice through hands-on coding exercises.
 
  * [*Tutorial*](../tutorial/) generated from notebooks, which provide reusable sample code plus supplemental exercises.
  * using a *progressive example*.
  * including a *learning promise* styled syllabus.


### Explanation

> Provide explanations that introduce concepts, exploring the theory and processes behind their usage.

  * [*What's a Knowledge Graph?*](../what/), attempting to get shared definitions in place – for a subject that has been somewhat difficult to define.
  * [*Concepts*](../concepts/) – exploring the abstractions used in this library, leading to best practices for how to leverage it.


### Evidence

> Where does this kind of technology meet business needs?

  * [*Use Cases*](../use_case/) exploring case studies for KG use in industry applications.
  * Other industry analysis, articles.


### Technical Reference

>  Each type, class, and parameter in the library which is intended for public use gets listed and explained, with plenty of whitespace for readability.

  * [*Package Reference*](../ref/) generated from *apidocs* customized for improved readability, corrected type annotations, etc.
  * [*Dependencies*](../depend/) links to all required libraries, with caveats.
  * [*Build Instructions*](..build/) for building from source (not necessary in most cases).


### Community

> Directing people toward how to engage with the developer community and related support.

  * [*Community Resources*](../community/) for more information about using this library, troubleshooting issues, and getting involved as a contributor.
  * [*Acknowledgements*](../ack/) to the developers, sponsors, and organizations which help to support this project.


### Research Guides

> Clarify terminology with shared definitions and their supporting links, and identify original papers, histories, notable authors, and other materials for context

  * [*Glossary*](../glossary/), which define terms and also provides a basis for indexing.
  * [*Bibliography*](../biblio/) of primary sources cited within this work.


### Feedback

> Helpful feedback, both from the community to the developers, and also for learners who are new to working in this field.

  * *surveys* for feedback about improving the learning material
  * *self-assessments* for personal feedback (WIP)
  * *certification exam* (WIP)
  * coding examples that lead into a *capstone project* (WIP)
  * instructor's personal recommendation on social media, following successful completion of the above


## Guidance

The strategy for structuring documentation which is used here has been
guided by some highly recommended resources.
Kudos to [@louisguitton](https://github.com/louisguitton) for pointing
out these practices and initiating this dialogue for **kglab**.

First, check out [[victorino2020]](../biblio/#victorino2020) for a
description of Stripe:

> Their strong writing culture benefits the organization in several areas:

1. Time efficiency. Sharing ideas through writing eliminates the need for repetitive verbal updates to disseminate ideas and information.
2. Knowledge sharing. Documenting important ideas forces clarity of thought and makes information more accessible to everyone in the company, versus slide decks that are ephemeral and require less rigor of thought.
3. Communication. Clear writing requires clear thinking, meaning employees invest more time shaping their ideas before sharing them.

The majority of the guidance comes from
[[procida2020]](../biblio/#procida2020) at Divio:
 
 > There is a secret that needs to be understood in order to write good software documentation: there isn’t one thing called documentation, there are *four*.
 > They are: *tutorials*, *how-to guides*, *technical reference* and *explanation*. They represent four different purposes or functions, and require four different approaches to their creation. Understanding the implications of this will help improve most documentation – often immensely.

In particular, the implementation of this approach by
[[song2020]](../biblio/#song2020) for Cloudflare documentation served
as a key inspiration.

Other major influences include 
<https://calmcode.io/> by [@koaning](https://github.com/koaning)
and
<https://calmtech.com/> by [@caseorganic](https://github.com/caseorganic),
both highly recommended.

The notion of a *grammar of graphics* was introduced by
[[wilkinson1999]](../biblio/#wilkinson1999)
then implemented in the [`ggplot2`](https://ggplot2.tidyverse.org/) by
[[wickham2010layered]](../biblio/#wickham2010layered).
To some extent, this work can borrow from that, attempting to
articulate design patterns to be used as a *grammar of learning*.
