#!/bin/bash

set -e # exit immediately in case of error
set -x # print all executed commands (=debug mode)


echo "=== Build Docker Image ==="

: ${REPOSITORY_PATH=001328938962.dkr.ecr.us-east-2.amazonaws.com}
: ${APP_NAME=valena}
: ${APP_BRANCH=$TRAVIS_BRANCH}

# login to aws ecr
eval $(aws ecr get-login --region us-east-2 --no-include-email)

# Get latest docker image for caching if available
docker pull ${REPOSITORY_PATH}/${APP_NAME}:latest || true


echo "=== Build branch version ==="

docker build \
  --pull=true \
  --cache-from ${REPOSITORY_PATH}/${APP_NAME}:latest \
  -t ${REPOSITORY_PATH}/${APP_NAME}:${APP_BRANCH} \
  --target base \
  .

# TODO: add test script for docker image
# Run the test script within the docker container
# docker run --rm -t --entrypoint deployment/test-docker.sh ${REPOSITORY_PATH}/${APP_NAME}:${APP_BRANCH}


echo "=== Pushing branch ${APP_BRANCH} to AWS ECR ==="

docker push ${REPOSITORY_PATH}/${APP_NAME}:${APP_BRANCH}

# TODO: only push image if master branch (maybe this can be even configured in travis deploy config)
# If the commit is tagged with a version also build that and latest
#if [[ $(git name-rev --name-only --tags --no-undefined HEAD) ]]; then
#  echo "=== Pushing tagged version ==="
#
#  GIT_TAG=${1:-$(git name-rev --name-only --tags --no-undefined HEAD)}
#  : ${APP_VERSION=${GIT_TAG:1}}
#
#  echo "VERSION = \"$APP_VERSION\"" > config/version.py
#
#  docker build \
#    --pull=true \
#    --cache-from ${REPOSITORY_PATH}/${APP_NAME}:latest \
#    -t ${REPOSITORY_PATH}/${APP_NAME}:${APP_VERSION} \
#    -t ${REPOSITORY_PATH}/${APP_NAME}:latest \
#    --target base \
#    .
#
#  # Check that version was set correctly
#  if [[ ! $(docker run --rm ${REPOSITORY_PATH}/${APP_NAME}:latest version) =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
#    echo "The version was not set properly. Check whether version.py was committed accidentally"
#  fi
#
#  echo "=== Checking version ==="
#  echo "Version:" $APP_VERSION
#  # check if APP_VERSION is final release
#  # one of: v{num}.{num}.{num}, {num}.{num}.{num}
#  # but not one of: vv2.3.4, 2.3.4.5, 2.3.4-my-ft, v5.6.7-beta, my-branch, etc.
#  if [[ $APP_VERSION =~ ^v?[0-9]+\.[0-9]+\.[0-9]+$ ]]
#  then
#    echo "This is a final release. Pushing as latest'"
#    docker push ${REPOSITORY_PATH}/${APP_NAME}:latest
#  else
#    echo "This is a prerelease. Skipping push as 'latest'"
#  fi
#
#  docker push ${REPOSITORY_PATH}/${APP_NAME}:${APP_VERSION}
#fi
