ARG ECR_REGISTRY
ARG ECR_REPOSITORY
FROM ${ECR_REGISTRY}/${ECR_REPOSITORY}:pyjava AS base

FROM base as builder

WORKDIR /tmp

COPY . .

ARG GITHUB_TOKEN

RUN pip install --prefix=/install .

FROM base

COPY --from=builder /install /usr/local

WORKDIR /app/

COPY lambda_function.py .

CMD ["python", "main.py"]

