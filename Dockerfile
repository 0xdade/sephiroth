FROM docker.io/python:3.8.1-buster

LABEL gitrepo="https://github.com/0xdade/sephiroth"

# Build:
# docker build --tag=sephiroth .

# Run:
# docker run --rm -v $(pwd):/app/output sephiroth -s nginx -c aws

WORKDIR /app
COPY LICENSE requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY templates /app/templates
COPY providers /app/providers
COPY sephiroth.py .
RUN chmod +x sephiroth.py && \
    sed -i 's/\r//' sephiroth.py

VOLUME /app/output
ENTRYPOINT [ "./sephiroth.py"]
