# syntax=docker/dockerfile:1

# Single source: .python-version (CI-12). CI passes --build-arg PYTHON_VERSION="$(cat .python-version)";
# the default only matters for plain local builds, and scripts/check_python_version.py keeps it in sync.
ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

COPY setup.py .
COPY folker/ folker/

RUN pip install --no-cache-dir --prefix=/install .


# Published image.
FROM python:${PYTHON_VERSION}-slim-bookworm AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

ENTRYPOINT ["folker-test"]


# Integration-test image: the published runtime plus the example fixtures, so CI tests
# exactly the layers it publishes (CI-04). Never published.
FROM runtime AS integration

COPY example/protos protos
COPY example/code testcode
COPY example/credentials credentials
COPY example/test test
