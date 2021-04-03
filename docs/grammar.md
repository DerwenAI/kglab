
# A Grammar of Learning

## How to use these materials

The objective for these learning materials is to help people learn how to leverage **kglab** effectively, gain confidence working with graph-based data science, plus have examples to repurpose for their own use cases.

You'll find a mix of topics throughout:
data science, business context, AI applications, data management, 
data strategy, design patterns, distributed systems – plus explorations of how to leverage the math, where appropriate.

This builds on the ["Graph-Based Data Science"](https://derwen.ai/s/kcgh) talks at conferences and meetups, which experiment with the content that eventually goes here.


## Structure

Based on the [guidance described below](#strategy), our documentation leverages the structure and dynamics shown in the following figure:

<img src="https://derwen.ai/docs/kgl/assets/learning.png" width="500" />

To make these materials useful to a wide audience, we've provided
multiple entry points, depending on what you need:

  * [discovery](../disc): navigation, indexing, search, recommendations
    - Much effort has gone into making sure this material is hyper-linked together
    - The left sidebar provides an overall outline of sections, while the right sidebar links to sections within the current section
    - Start at any point, for whatever info is most immediately useful
    - It may be helpful to run JupyterLab for the coding examples in one browser tab, while reading this documentation in another browser tab
    - Search in the `MkDocs` framework has much to be desired. It's disabled now, and a replacement is in development
    - Contextual links to the Derwen website provide recommendations, and more of that is getting integrated directly into this documentation.

  * [explanation](../concepts): explanations that introduce concepts, exploring the theory and processes behind their usage
	- *What's a Knowledge Graph?*
	- *Concepts*

  * [technical reference](../ref): each type, class, and parameter is listed and explained with plenty of whitespace for readability
	- *Package Reference*: generated from *apidocs* (which probably need customizing)
	- *Dependencies*

  * [how-to guides](../howto): problem-oriented directions for getting things done
	- *Getting Started*
	- *Build Instructions*
	- specific "howto" articles, generated from notebooks

  * [tutorials](../tutorial/): learning-oriented practice through hands-on coding exercises, based on a *progressive example*
	- based on *learning promise* styled syllabus
	- generated from notebooks, which provide reusable sample code and supplemental exercises

  * [use cases](../use_case): explore use cases and link to related case studies for grounding in industry applications

  * [glossary](../glossary): clarify terminology with shared definitions and their supporting links

  * [primary sources](../biblio): point toward original papers, histories, notable authors, and other materials for context
	- generated from a KG

   * [community support](../foo):
	- open source governance, focused on discussions on the GitHub repo [Issue Tracker](https://github.com/DerwenAI/kglab/issues)
	- [*Graph-Based Data Science*](https://www.linkedin.com/groups/6725785/) group on LinkedIn – join to receive related updates, news, conference coupons, etc.
	- [community Slack](https://knowledgegraphconf.slack.com/ssb/redirect) discussions
	- [Knowledge Tech Q&A site](https://answers.knowledgegraph.tech/) for extended discussions
	- ["knowledge espresso"](https://www.notion.so/KG-Community-Events-Calendar-8aacbe22efa94d9b8b39b7288e22c2d3) (monthly office hours) with [Paco Nathan](ack/#project-lead) and others involved in this open source project

  * [feedback](../foo):
	- *surveys* for feedback about improving the learning material
	- *self-assessments* for personal feedback
	- *certification exam*
	- coding examples that lead into a *capstone project*
	-  instructor personal recommendation on social media


---

## Strategy

Our strategy for documentation which is used here has been guided by some highly recommended resources:

  * <https://documentation.divio.com/>
  * <https://slab.com/blog/stripe-writing-culture/>
  * <https://blog.cloudflare.com/new-and-improved-workers-docs/>
  * <https://calmtech.com/>

Kudos to [@louisguitton](https://github.com/louisguitton) for developing this part.

["Divio: The documentation system"](https://documentation.divio.com/)  
 **Daniele Procida**  
 Divio (2020)
 
 > There is a secret that needs to be understood in order to write good software documentation: there isn’t one thing called documentation, there are *four*.
 > They are: *tutorials*, *how-to guides*, *technical reference* and *explanation*. They represent four different purposes or functions, and require four different approaches to their creation. Understanding the implications of this will help improve most documentation - often immensely.

["New and improved Workers Docs"](https://blog.cloudflare.com/new-and-improved-workers-docs/)  
**David Song**  
CloudFlare (2020-08-19)

["How Stripe Built a Writing Culture"](https://slab.com/blog/stripe-writing-culture/)  
**RC Victorino**  
*Slab*, (2020-09-02)

> Their strong writing culture benefits the organization in several areas:

  1. Time efficiency. Sharing ideas through writing eliminates the need for repetitive verbal updates to disseminate ideas and information.
  2. Knowledge sharing. Documenting important ideas forces clarity of thought and makes information more accessible to everyone in the company, versus slide decks that are ephemeral and require less rigor of thought.
  3. Communication. Clear writing requires clear thinking, meaning employees invest more time shaping their ideas before sharing them.

[*The Grammar of Graphics*](https://www.goodreads.com/book/show/20182493-the-grammar-of-graphics)  
**Leland Wilkinson**, et al.  
Springer (1999-08-19)

["A layered grammar of graphics"](http://dx.doi.org/10.1198/jcgs.2009.07098)  
**Hadley Wickham**  
*Journal of Computational and Graphical Statistics*, vol. 19, no. 1, pp. 3–28 (2010)

