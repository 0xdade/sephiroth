FROM python:3.10.4-alpine3.14

# Build:
# docker build --tag=sephiroth .

# Run:
# docker run --rm -v $(pwd):/app/output sephiroth -s nginx -t aws

COPY --from=ghcr.io/astral-sh/uv:0.6.0 /uv /uvx /bin/

WORKDIR /app
COPY LICENSE /app/
COPY src/ /app/src/
RUN \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=README.md,target=/app/README.md \
    --mount=type=cache,target=/root/.cache \
    uv sync --frozen
VOLUME "/app/output"
ENTRYPOINT [ "uv", "run", "sephiroth", "--output-dir", "/app/output"]
