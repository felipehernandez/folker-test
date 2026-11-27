# syntax=docker/dockerfile:1

# Single source: .python-version (CI-12). CI passes --build-arg PYTHON_VERSION="$(cat .python-version)";
# the default only matters for plain local builds, and scripts/check_python_version.py keeps it in sync.
ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

WORKDIR /build

# DEP-01: uv installs exactly what uv.lock says (--frozen never re-resolves). The uv version is
# pinned in requirements-uv.txt, shared with CI and the dev container.
ENV UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-uv.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-uv.txt

# Dependencies first: this layer is rebuilt only when pyproject.toml or uv.lock change.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --no-editable

COPY folker/ folker/
RUN uv sync --frozen --no-dev --no-editable


# Published image.
FROM python:${PYTHON_VERSION}-slim-bookworm AS runtime

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["folker-test"]


# Integration-test image: the published runtime plus the example fixtures, so CI tests
# exactly the layers it publishes (CI-04). Never published.
FROM runtime AS integration

COPY example/protos protos
COPY example/code testcode
COPY example/credentials credentials
COPY example/test test
