FROM python

ENV PYTHONPATH=/app
WORKDIR /app

ARG GITHUB_TOKEN
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

RUN python setup.py install