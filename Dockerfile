FROM python

ENV PYTHONPATH=/app
WORKDIR /app

ARG GITHUB_TOKEN
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

RUN python setup.py install

# Install JVM
RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes default-jdk


# Fix certificate issues
RUN apt-get update && \
    apt-get install --yes ca-certificates-java && \
    update-ca-certificates -f;

RUN apt-get clean --yes

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

