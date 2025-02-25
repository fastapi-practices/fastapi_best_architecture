FROM python:3.10-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.2 /uv /uvx /bin/

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev\
    && rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_CACHE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-default-groups --group server


FROM python:3.10-slim

SHELL ["/bin/bash", "-c"]

ENV TZ="Asia/Shanghai"

WORKDIR /fba

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update \
    && apt-get install -y --no-install-recommends supervisor procps iproute2 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/log/fastapi_server \
    && mkdir -p /var/log/celery

COPY . .
RUN chmod +x backend/*.sh
COPY --from=builder /usr/local /usr/local
COPY deploy/backend/supervisord.conf /etc/supervisor/supervisord.conf
ARG SERVICE_TYPE=fastapi_server
COPY deploy/backend/${SERVICE_TYPE}.conf /etc/supervisor/conf.d/

EXPOSE 8001
EXPOSE 8555

CMD ["backend/${SERVICE_TYPE}-start.sh"]
