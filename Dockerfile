# Use the official n8n image as base
FROM docker.n8n.io/n8nio/n8n

# Switch to root to install packages
USER root

# Install Python3, pip, and other useful packages for Alpine Linux
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-virtualenv \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers

# Create a virtual environment for Python packages
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install common Python packages including scrapy
RUN pip install --no-cache-dir \
    scrapy \
    requests \
    beautifulsoup4 \
    pandas \
    numpy \
    lxml

# Switch back to the node user
USER node

# Expose the default n8n port
EXPOSE 5678

# Use the original entrypoint
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]
