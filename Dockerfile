# Select the image to build based on SERVER_TYPE, defaulting to fastapi_server, or docker-compose build args
ARG SERVER_TYPE=fastapi_server

# === Python environment from uv ===
FROM python:3.10-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Used for build Python packages
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Configure uv environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local

# Install dependencies with cache
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-default-groups --group server

# === Runtime base server image ===
FROM python:3.10-slim AS base_server

SHELL ["/bin/bash", "-c"]

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY . /fba

COPY --from=builder /usr/local /usr/local

# Install plugin dependencies
WORKDIR /fba
ENV PYTHONPATH=/fba
RUN python3 backend/scripts/init_plugin.py

# === FastAPI server image ===
FROM base_server AS fastapi_server

WORKDIR /fba

COPY deploy/backend/supervisord.conf /etc/supervisor/supervisord.conf
COPY deploy/backend/fastapi_server.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fastapi_server

EXPOSE 8001

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port","8000"]

# === Celery server image ===
FROM base_server AS celery

WORKDIR /fba/backend/

COPY deploy/backend/supervisord.conf /etc/supervisor/supervisord.conf
COPY deploy/backend/celery.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/celery

RUN chmod +x celery-start.sh

EXPOSE 8555

CMD ["./celery-start.sh"]

# Build image
FROM ${SERVER_TYPE}
