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
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-default-groups --group server --no-install-project

# Preinstall plugin dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    python -c "from backend.plugin.requirements import install_requirements; install_requirements(None)"

# === Runtime base server image ===
FROM python:3.10-slim-bookworm AS base_server

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates supervisor \
    && rm -rf /var/lib/apt/lists/*

# Optional: Install SQL Server ODBC Driver 18 for SQL Server support
# Uncomment the lines below or build with --build-arg INSTALL_MSSQL_ODBC=true
ARG INSTALL_MSSQL_ODBC=false
RUN if [ "$INSTALL_MSSQL_ODBC" = "true" ]; then \
    sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends gnupg unixodbc \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && apt-get purge -y --auto-remove gnupg \
    && rm -rf /var/lib/apt/lists/*; \
    fi

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

COPY --from=builder /fba /fba

COPY --from=builder /usr/local /usr/local

COPY deploy/backend/supervisor/supervisord.conf /etc/supervisor/supervisord.conf

# === FastAPI server image ===
FROM base_server AS fba_server

COPY deploy/backend/supervisor/fba_server.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fba

EXPOSE 8001

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# === Celery Worker image ===
FROM base_server AS fba_celery_worker

COPY deploy/backend/supervisor/fba_celery_worker.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fba

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# === Celery Beat image ===
FROM base_server AS fba_celery_beat

COPY deploy/backend/supervisor/fba_celery_beat.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fba

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# === Celery Flower image ===
FROM base_server AS fba_celery_flower

COPY deploy/backend/supervisor/fba_celery_flower.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fba

EXPOSE 8555

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

# Build image
FROM ${SERVER_TYPE}
