#!/bin/bash

set -e # exit immediately in case of error
set -x # print all executed commands (=debug mode)


echo "=== Get latest docker image ==="

: ${REGISTRY=001328938962.dkr.ecr.us-east-2.amazonaws.com}
: ${REPOSITORY=valena}

# login to aws ecr
docker login -u AWS -p $(aws --region us-east-2 ecr get-login-password) ${REGISTRY}

# get latest docker image for caching if available
docker pull ${REGISTRY}/${REPOSITORY}:main || true


echo "=== Build new docker image ==="

docker build --pull=true --cache-from ${REGISTRY}/${REPOSITORY}:main \
  -t ${REGISTRY}/${REPOSITORY}:${TRAVIS_BRANCH} .

# to do add test script for docker image

echo "=== Push docker image ${TRAVIS_BRANCH} to AWS ECR ==="

docker push ${REGISTRY}/${REPOSITORY}:${TRAVIS_BRANCH}
