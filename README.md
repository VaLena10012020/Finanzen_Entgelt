# Finanzen_Entgelt
Parse Entgelt files

[![Build Status](https://travis-ci.com/VaLena10012020/Finanzen_Entgelt.svg?branch=main)](https://travis-ci.com/VaLena10012020/Finanzen_Entgelt)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Development
Build docker image with:
```
 docker build -t finanzen-entgelt -f Dockerfile.dev --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} .
```

## Testing and code quality
Run tests local with:
```
pytest
```

or within docker image with:
```
docker run finanzen-entgelt pytest
```

flake8 is implemented as a pre-commit hook. Hence, it is automatically conducted 
upon each commit. In addition, it is possible to trigger linting manually with the following command:
```
pre-commit run --all-files
```