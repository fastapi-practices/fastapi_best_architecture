FROM python:3.10-slim

WORKDIR /fba

COPY . .

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

ENV TZ = Asia/Shanghai

RUN mkdir -p /var/log/celery

WORKDIR /fba/backend/app

RUN chmod +x celery-start.sh

# 这里不使用脚本启动 celery, 而是使用 supervisor
# 因为 celery 脚本包含 worker 和 beat, 但是并不推荐它们在一条命令中启动
#CMD ["./celery-start.sh"]
