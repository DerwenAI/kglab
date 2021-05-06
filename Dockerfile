# Ref: https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html
FROM jupyter/base-notebook:python-3.8.8

# 'igraph' python library requires 'libcairo2-dev' to be installed
# ref: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#manpage-installation
USER root
RUN sudo apt-get update && \
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3.8-dev \
        libcairo2-dev

USER $NB_UID
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt
