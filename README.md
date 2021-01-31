# Finanzen_Entgelt
Parse Entgelt files

[![Build Status](https://travis-ci.com/VaLena10012020/Finanzen_Entgelt.svg?branch=main)](https://travis-ci.com/VaLena10012020/Finanzen_Entgelt)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Development
**Either:** use a dockerfile as interpreter to work on your local machine. 

Login to aws ecr:
```
docker login -u AWS -p $(aws --region us-east-2 ecr get-login-password) ${ECR_REGISTRY}
```

Build docker image with:
```
docker build -t finanzen-entgelt-dev -f Dockerfile.dev \
  --build-arg ECR_REGISTRY=${ECR_REGISTRY} \
  --build-arg ECR_REPOSITORY=${ECR_REPOSITORY} \
  .
```

**Or:** setup/activate a virtualenv and install dependencies there:
```
./setup_local.sh
```


## Testing and code quality
**Either:** 
run tests from docker image with:
```
docker run finanzen-entgelt-dev pytest
```

**Or:** run tests local with:
```
pytest
```

flake8 is implemented as a pre-commit hook. Hence, it is automatically conducted 
upon each commit. In addition, it is possible to trigger linting manually with the following command:
```
pre-commit run --all-files
```

## Production
Build docker image with:
```
docker build -t finanzen-entgelt-prod -f Dockerfile \
  --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} \
  --build-arg ECR_REGISTRY=${ECR_REGISTRY} \
  --build-arg ECR_REPOSITORY=${ECR_REPOSITORY} \
  .
```