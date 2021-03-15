# Tutorial Setup

The coding exercises in the following tutorial are based on
progressive examples based on cooking recipes, which illustrate the
use of **kglab** and related libraries in Python for *graph-based data
science*.


## Prerequisites

  * Some coding experience in Python (you can read a 20-line program)
  * Interest in use cases that require *knowledge graph representation*

Additionally, if you've completed *Algebra 2* in secondary school and
have some business experience working with data analytics – both can
come in handy.


## Audience

  * Python developers who need to work with KGs
  * Data Scientists, Data Engineers, Machine Learning Engineers
  * Technical Leaders who want hands-on KG implementation experience


## Key Takeaways

  * Hands-on experience with popular open source libraries in Python for building KGs
  * Coding examples that can be used as starting points for your own KG projects
  * Understanding trade-offs for different approaches to building KGs


## Installation

You can run the notebooks locally on a recent laptop.
First clone the Git repository:
```
git clone https://github.com/DerwenAI/kglab.git
cd kglab
```

To install the dependencies using `pip`:
```
pip install -r requirements.txt
```

Alternatively, to install the dependencies using `conda`:
```
conda env create -f environment.yml
conda activate kglab
```

Also make sure to install
[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/).
To install using `pip`:
```
pip install jupyterlab
```

Or if you use `conda` you can install it with:
```
conda install -c conda-forge jupyterlab
```

Note: for installing via `pip install --user` you must add the
user-level `bin` directory to your `PATH` environment variable in
order to launch JupyterLab.
If you're using a Unix derivative (FreeBSD, GNU/Linux, OS X), you can
achieve this by using the `export PATH="$HOME/.local/bin:$PATH"`
command.

Once installed, launch JupyterLab with:
```
jupyter-lab
```

Then open the `examples` subdirectory to launch the notebooks featured
in the following sections of this tutorial.
