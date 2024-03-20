FROM python:3.10-slim

WORKDIR /fba

COPY . .

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 某些包可能存在同步不及时导致安装失败的情况，可更改为官方源：https://pypi.org/simple
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install -r backend/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

ENV TZ = Asia/Shanghai

RUN mkdir -p /var/log/fastapi_server

COPY deploy/backend/fastapi_server.conf /etc/supervisor/conf.d/

EXPOSE 8001

CMD ["uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"]
