FROM python:3.8-slim

WORKDIR /fba

COPY . /fba

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV TZ = Asia/Shanghai

RUN mkdir -p /var/log/fastapi_server

EXPOSE 8001

CMD ["uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"]
