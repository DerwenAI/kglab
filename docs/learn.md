# A Grammar of Learning

Let's talk briefly about how to design and present learning materials.
What are we doing here?
In another sense, consider the following as a very brief exercise in *design thinking*, focused on how to improve software documentation and tutorials.

As we describe in the [guidance](#guidance) below, there's a growing movement toward more structured approaches to how documentation gets presented.
Arguably, a lack of quality or effectivenes in their documentation is a major impediment for many otherwise popular open source libraries.
Much the same goes for tutorials, which are often written from the perspective of someone who's already familiar with the material – thus defeating its purpose for those who aren't.
Divio, Cloudflare, Stripe, and other firms have fostered *writing cultures* internally, while applying more structured approaches to presenting their learning materials externally.
That shouldn't be surprising: software developers tend to write in volume – generally much more text than they produce as source code – since the processing of planning projects and maintaining them over time usually involves lots of written communications.
That said, good editing for developers' text is much less common.
That's why the examples set by Stripe and others are important.

Our developer team has iterated on these emerging approaches, blending key insights and practices from our prior roles, to create design patterns for documentation and tutorials.

The notion of a *grammar of graphics* was introduced by
[[wilkinson1999]](../biblio/#wilkinson1999)
then implemented in the [`ggplot2`](https://ggplot2.tidyverse.org/) by
[[wickham2010layered]](../biblio/#wickham2010layered).
Our work borrows from their approach, attempting to articulate a set of design patterns to be used as a *grammar of learning*.
The outline of this documentation follows these design patterns, and more specifically so does the syllabus structure used within our [hands-on tutorial](../tutorial/).


## How to use these materials

The objective for these learning materials is to help people learn how to leverage **kglab** effectively, gain confidence working with graph-based data science, plus have examples to repurpose for their own use cases.

You'll find a mix of topics throughout:
data science, business context, AI applications, data management, 
data strategy, design patterns, distributed systems – plus explorations of how to leverage the math, where appropriate.
This work builds on the ["Graph-Based Data Science"](https://derwen.ai/s/kcgh) talks at conferences and meetups, which experiment with the content – collecting feedback, critiques, suggestions, etc.
The results eventually go here.

The overall structure and dynamics of our documentation are shown in the following figure:

<img src="https://derwen.ai/docs/kgl/assets/learning.png" width="500" />

The intention is to make these materials useful to a wide audience.
So we provide multiple entry points, depending on what you need:


### Discovery

 > Affordances for navigation, indexing, search, recommendations

Much effort has gone into making sure this material is thoroughly hyper-linked together, to help with both navigation and indexing.
Even so, suggestions for improvement are highly welcomed!
The left sidebar provides an overall outline of sections, while the right sidebar links to sections within the current section.
Start at any point, for whatever info is most immediately useful.

!!! note
    It may be helpful to run [JupyterLab](https://jupyterlab.readthedocs.io/) for the coding examples in one browser tab, while navigating through this documentation in another browser tab.

The search features implemented in documentation frameworks such as
[`MkDocs`](https://www.mkdocs.org/),
[`Sphinx`](https://www.sphinx-doc.org/en/master/),
etc., leave much to be desired.
Consequently the search features are disabled here, for now, while a replacement is in development.
Meanwhile, contextual links based on the KG-powered [Derwen search/discovery](https://derwen.ai/d/) services online help provide recommendations.
More of that is getting integrated directly into this documentation.


### Explanation

> Provide explanations that introduce concepts, exploring the theory and processes behind their usage

  * [*What's a Knowledge Graph?*](../what)
  * [*Concepts*](../concepts)


### Technical Reference

>  Each type, class, and parameter in the library which is intended for public use gets listed and explained, with plenty of whitespace for readability

  * [*Package Reference*](../ref): generated from *apidocs* (customized for improved readability, corrected type annotations, etc.)
  * *Dependencies*


### HowTo

> Present problem-oriented directions for getting things done

  * *Getting Started*
  * *Build Instructions*
  * specific "howto" articles, generated from notebooks


### Tutorial

> Learning-oriented practice through hands-on coding exercises
 
  * based on *learning promise* styled syllabus
  * [tutorials](../tutorial/) based on a *progressive example*, generated from notebooks, which provide reusable sample code plus supplemental exercises


### Evidence

  * [use cases](../use_case): explore use cases and link to related case studies for grounding in industry applications
  * industry analysis


### Glossary

> Clarify terminology with shared definitions and their supporting links

  * [glossary](../glossary), which also provides the basis for indexing


### Primary Sources

> Point toward original papers, histories, notable authors, and other materials for context

  * [primary sources](../biblio) cited within this work, generated from a KG


### Community Support

> Directing people toward how to engage with the developer community and related support

  * open source governance, focused on discussions on the GitHub repo [Issue Tracker](https://github.com/DerwenAI/kglab/issues)
  * [*Graph-Based Data Science*](https://www.linkedin.com/groups/6725785/) group on LinkedIn – join to receive related updates, news, conference coupons, etc.
  * [community Slack](https://knowledgegraphconf.slack.com/ssb/redirect) discussions
  * [Knowledge Tech Q&A site](https://answers.knowledgegraph.tech/) for extended discussions
  * [monthly office hours](https://www.notion.so/KG-Community-Events-Calendar-8aacbe22efa94d9b8b39b7288e22c2d3) with [Paco Nathan](ack/#project-lead) and others involved in this open source project


### Feedback

> Helpful feedback, both from the community to the developers, and also for learners who are working with this material

  * *surveys* for feedback about improving the learning material
  * *self-assessments* for personal feedback (WIP)
  * *certification exam* (WIP)
  * coding examples that lead into a *capstone project* (WIP)
  * instructor's personal recommendation on social media, following successful completion of the above


## Guidance

The strategy for structuring documentation which is used here has been guided by some highly recommended resources.
Kudos to [@louisguitton](https://github.com/louisguitton) for pointing out these practices and initiating this dialogue for **kglab**.

First, check out [[victorino2020]](../biblio/#victorino2020) for a description of Stripe:

> Their strong writing culture benefits the organization in several areas:

1. Time efficiency. Sharing ideas through writing eliminates the need for repetitive verbal updates to disseminate ideas and information.
2. Knowledge sharing. Documenting important ideas forces clarity of thought and makes information more accessible to everyone in the company, versus slide decks that are ephemeral and require less rigor of thought.
3. Communication. Clear writing requires clear thinking, meaning employees invest more time shaping their ideas before sharing them.

The majority of the guidance comes from [[procida2020]](../biblio/#procida2020) at Divio:
 
 > There is a secret that needs to be understood in order to write good software documentation: there isn’t one thing called documentation, there are *four*.
 > They are: *tutorials*, *how-to guides*, *technical reference* and *explanation*. They represent four different purposes or functions, and require four different approaches to their creation. Understanding the implications of this will help improve most documentation – often immensely.

In particular, the implementation of this by [[song2020]](../biblio/#song2020) for Cloudflare documentation served as a key inspiration.

Other major influences include 
<https://calmcode.io/> by [@koaning](https://github.com/koaning)
and
<https://calmtech.com/> by [@caseorganic](https://github.com/caseorganic),
both highly recommended.