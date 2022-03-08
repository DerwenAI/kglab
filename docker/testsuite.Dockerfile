FROM ubuntu:20.04 as base
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

######################################################################
## build essential libraries

FROM base as libs
USER root
WORKDIR /opt/kglab

RUN set -eux; \
	apt-get update ; \
	apt-get upgrade -y ; \
	apt-get install -y --no-install-recommends \
		tzdata build-essential software-properties-common \		
		wget git gpg-agent apt-transport-https ca-certificates apt-utils \
		python3.8 python3-pytest python3.8-distutils python3.8-dev python3.8-venv \
		openjdk-11-jre-headless ca-certificates-java \
		libcairo2-dev ; \
	rm -rf /var/lib/apt/lists/*

## setup Python 3.8 and Pip
RUN set -eux; \
	wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py ; \
	python3.8 get-pip.py ; \
	python3.8 -m pip install -U pip

######################################################################
## build kglab

FROM libs as kglab

## copy source
COPY ./kglab /opt/kglab/kglab
COPY ./dat /opt/kglab/dat
COPY ./examples /opt/kglab/examples
COPY ./requirements*.txt /opt/kglab/
COPY ./tests/ /opt/kglab/tests/
COPY ./sample.py /opt/kglab/

## create a known user ID
RUN set -eux; \
	groupadd -g 999 appuser ; \
	useradd -r -u 999 -g appuser appuser ; \
	usermod -d /opt/kglab appuser ; \
	chown -R appuser:appuser /opt/kglab ; \
	chmod -R u+rw /opt/kglab

USER appuser

## install Python dependencies in a venv to maintain same binary path as system
WORKDIR /opt/kglab

RUN set -eux; \
	python3.8 -m venv /opt/kglab/venv ; \
	source /opt/kglab/venv/bin/activate ; \
	/opt/kglab/venv/bin/python3.8 -m pip install -U pip wheel setuptools ; \
	/opt/kglab/venv/bin/python3.8 -m pip install -r /opt/kglab/requirements.txt
######################################################################
## specific for test suite:

FROM kglab as testsuite

WORKDIR /opt/kglab
USER appuser

RUN set -eux; \
	source /opt/kglab/venv/bin/activate ; \
	/opt/kglab/venv/bin/python3.8 -m pip install -r /opt/kglab/requirements-dev.txt

CMD /opt/kglab/venv/bin/python3.8 -m pytest tests/