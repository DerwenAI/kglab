# Getting Started

<img src="../assets/nouns/tutorial.png" alt="Video Tutorial by artworkbean from the Noun Project" />

## Installation

To install from [PyPi](https://pypi.python.org/pypi/kglab):
```
python3 -m pip install kglab
```

If you work directly from this Git repo, be sure to install the 
[dependencies](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format):
```
python3 -m pip install -r requirements.txt
```

Alternatively, to install dependencies using `conda`:
```
conda env create -f environment.yml
conda activate kglab
```

See the [*Dependencies*](../depend/#troubleshooting) section for more
information about troubleshooting installation issues.


## Sample Usage

To use **kglab** in its simplest form:
```python
import kglab

kg = kglab.KnowledgeGraph()
kg.load_rdf("https://storage.googleapis.com/kglab-tutorial/foaf.rdf", format="xml")

measure = kglab.Measure()
measure.measure_graph(kg)

print("edges: {}\n".format(measure.get_edge_count()))
print("nodes: {}\n".format(measure.get_node_count()))

ttl = kg.save_rdf_text()
print(ttl)
```

## Using Docker

1. For a simple approach to running our tutorials, see use of [_docker compose_](tutorial/#use-docker-compose).

2. Alternatively, container images for each release are available on DockerHub: <https://hub.docker.com/repository/docker/derwenai/kglab>

3. To build a container image and run it for the tutorials:
```bash
docker build --pull --rm -f "docker/Dockerfile" -t kglab:latest .
docker run -p 8888:8888 -it kglab
```


## Hands-on Coding Tutorial

See the [*Tutorial*](../tutorial/) notebooks for sample code and
patterns to use when integrating **kglab** with other related
libraries in Python.
