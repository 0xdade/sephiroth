FROM python:3.8-alpine3.14

LABEL gitrepo="https://github.com/0xdade/sephiroth"

# Build:
# docker build --tag=sephiroth .

# Run:
# docker run --rm -v $(pwd):/app/output sephiroth -s nginx -t aws

WORKDIR /app
COPY LICENSE Pipfile Pipfile.lock /app/
RUN pip install --no-cache-dir pipenv \
    && PIPENV_VENV_IN_PROJECT=1 pipenv sync

COPY sephiroth/ /app/sephiroth
COPY Sephiroth.py .

VOLUME /app/output
ENTRYPOINT [ "pipenv", "run", "python", "Sephiroth.py"]
