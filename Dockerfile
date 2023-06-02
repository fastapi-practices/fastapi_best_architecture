FROM python:3.10-slim

WORKDIR /fba

COPY . .

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 某些包可能存在同步不及时导致安装失败的情况，可选择备用源
# 清华源（国内快，也可能同步不及时）：https://pypi.tuna.tsinghua.edu.cn/simple
# 官方源（国外慢，但永远都是最新的）：https://pypi.org/simple
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

ENV TZ = Asia/Shanghai

RUN mkdir -p /var/log/fastapi_server

EXPOSE 8001

CMD ["uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"]
