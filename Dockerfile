# Ref: https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html
# Ref: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html
FROM jupyter/base-notebook:python-3.8.8

# 'igraph' python library requires 'libcairo2-dev' to be installed
# 'pslpython' python library requires Java 7 or 8
USER root

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
        python3.8-dev \
        libcairo2-dev \
        openjdk-11-jre-headless \
        ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_UID
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt
