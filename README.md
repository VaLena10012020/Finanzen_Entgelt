# Finanzen_Entgelt
Parse Entgelt files

[![Build Status](https://travis-ci.com/VaLena10012020/Finanzen_Entgelt.svg?branch=main)](https://travis-ci.com/VaLena10012020/Finanzen_Entgelt)

## Development
Build docker image with:
```
 docker build -t finanzen-entgelt -f Dockerfile.dev --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} .
```

## Testing
Run tests local with:
```
pytest
```

or within docker image with:
```
docker run finanzen-entgelt pytest
```