#!/bin/bash

set -e # exit immediately in case of error
set -x # print all executed commands (=debug mode)


echo "=== Get latest docker image ==="

# get latest docker image for caching if available
docker pull ${ECR_REGISTRY}/${ECR_REPOSITORY}:main || true


echo "=== Build new docker image ==="

docker build --pull=true --cache-from ${ECR_REGISTRY}/${ECR_REPOSITORY}:main \
  -t ${ECR_REGISTRY}/${ECR_REPOSITORY}:entgelt_${TRAVIS_BRANCH} \
  --build-arg ECR_REGISTRY=${ECR_REGISTRY} --build-arg ECR_REPOSITORY=${ECR_REPOSITORY} .

# to do add test script for docker image

echo "=== Push docker image ${TRAVIS_BRANCH} to AWS ECR ==="

docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:$entgelt_{TRAVIS_BRANCH}
