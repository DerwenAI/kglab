FROM python:3.8-slim

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN pip install jupyterlab

COPY . /app
WORKDIR /app

RUN pip install -e .

CMD [ "jupyter-lab", "--allow-root"]
