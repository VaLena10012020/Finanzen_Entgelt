#!/bin/bash

set -e # exit immediately in case of error
set -x # print all executed commands (=debug mode)


echo "=== Build Docker Image ==="

: ${ECR_REPO=001328938962.dkr.ecr.us-east-2.amazonaws.com/valena}

# login to aws ecr
eval $(aws ecr get-login --region us-east-2 --no-include-email)

# get latest docker image for caching if available
docker pull ${ECR_REPO}:latest || true


echo "=== Build branch version ==="

docker build --pull=true --cache-from ${ECR_REPO}:latest \
  -t ${ECR_REPO}:${$TRAVIS_BRANCH} --target base .

# TODO: add test script for docker image

echo "=== Pushing branch ${$TRAVIS_BRANCH} to AWS ECR ==="

docker push ${ECR_REPO}:${$TRAVIS_BRANCH}
