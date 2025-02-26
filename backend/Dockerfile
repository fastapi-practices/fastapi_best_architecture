ARG SERVICE_TYPE=fastapi_server

# ===== Build Stage =====
FROM python:3.10-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.2 /uv /uvx /bin/

# Install dependencies for building Python packages
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Configure uv environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local

# COPY backend/plugin/casbin/requirements.txt plugin_casbin_requirements.txt

# Install dependencies using uv (with cache optimization)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-default-groups --group server
    # uv sync --frozen --no-install-project --no-default-groups --group server \
    # && uv pip install --system -r plugin_casbin_requirements.txt


# ===== Runtime Base Image =====
FROM python:3.10-slim AS runtime
SHELL ["/bin/bash", "-c"]
ENV TZ="Asia/Shanghai"

# Install runtime dependencies
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends supervisor procps iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Copy application and Python packages
COPY . /fba
COPY --from=builder /usr/local /usr/local

# ===== FastAPI Server Image =====
FROM runtime AS fastapi_server
WORKDIR /fba/backend
RUN mkdir -p /var/log/fastapi_server
COPY deploy/backend/supervisord.conf /etc/supervisor/supervisord.conf
COPY deploy/backend/fastapi_server.conf /etc/supervisor/conf.d/
EXPOSE 8001
ENV PYTHONPATH=/fba
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port","8000"]

# ===== Celery Worker Image =====
FROM runtime AS celery
WORKDIR /fba/backend
RUN mkdir -p /var/log/celery && chmod +x /fba/backend/*.sh
COPY deploy/backend/supervisord.conf /etc/supervisor/supervisord.conf
COPY deploy/backend/celery.conf /etc/supervisor/conf.d/
EXPOSE 8555
CMD ["./celery-start.sh"]

# Select the image type based on SERVICE_TYPE build arg
FROM ${SERVICE_TYPE}
