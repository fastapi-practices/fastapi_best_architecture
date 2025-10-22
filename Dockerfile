# Select the image to build based on SERVER_TYPE, defaulting to fba_server, or docker-compose build args
ARG SERVER_TYPE=fba_server

# === Python environment from uv ===
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder

# Used for build Python packages
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /fba

WORKDIR /fba

# Configure uv environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local

# Install dependencies with cache
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-default-groups --group server

# === Runtime base server image ===
FROM python:3.10-slim AS base_server

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /fba /fba

COPY --from=builder /usr/local /usr/local

COPY deploy/backend/supervisord.conf /etc/supervisor/supervisord.conf

WORKDIR /fba/backend

# === FastAPI server image ===
FROM base_server AS fba_server

COPY deploy/backend/fba_server.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fba

EXPOSE 8001

CMD ["/usr/local/bin/granian", "main:app", "--interface", "asgi", "--host", "0.0.0.0", "--port","8000"]

# === Celery server image ===
FROM base_server AS fba_celery

COPY deploy/backend/fba_celery.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fba

RUN chmod +x celery-start.sh

EXPOSE 8555

CMD ["./celery-start.sh"]

# Build image
FROM ${SERVER_TYPE}
