# Ref: https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html
FROM jupyter/base-notebook:python-3.8.8

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt

