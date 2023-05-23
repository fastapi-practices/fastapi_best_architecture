# FastAPI 最佳架构

简体中文 | [English](./README.md)

这是 FastAPI 框架的一个基础项目，在制作中

它的目的是让你直接用它作为你的基础项目来开发你的项目

支持 python3.10 及以上版本

## 技术栈

- [x] FastAPI
- [x] Pydantic
- [x] SQLAlchemy
- [x] Alembic
- [x] MySQL
- [x] Redis
- [x] APScheduler
- [x] Docker

## 克隆

```shell
git clone https://github.com/wu-clan/fastapi_best_architecture.git
```

## 使用：

### 1：传统

1. 安装依赖项
    ```shell
    pip install -r requirements.txt
    ```

2. 创建一个数据库`fba`，选择 utf8mb4 编码
3. 安装并启动 Redis
4. 在`backend/app/`目录下创建一个`.env`文件
    ```shell
    cd backend/app/
    touch .env
    ```
5. 复制 `.env.example` 到 `.env` 并查看`backend/app/core/conf.py`，更新数据库配置信息
6. 进行数据库迁移[alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
   ```shell
   cd backend/app/

   # 生成迁移文件
   alembic revision --autogenerate

   # 执行迁移
   alembic upgrade head
    ```
7. 执行 `backend/app/main.py` 文件启动服务
8. 浏览器访问：http://127.0.0.1:8000/v1/docs

---

### 2：Docker

1. 在 `docker-compose.yml` 文件所在的目录中运行一键启动命令

   ```shell
   docker-compose up -d -build
   ```
   
2. 等待命令自动完成

3. 浏览器访问：http://127.0.0.1:8000/v1/docs

## 初始化测试数据

执行 `backend/app/init_test_data.py` 文件

## 测试

通过 pytest 进行测试

1. 创建一个数据库`fba_test`，选择 utf8mb4 编码

2. 首先，进入app目录

   ```shell
   cd backend/app/
   ```
   
3. 初始化测试数据

   ```shell
   python tests/init_test_data.py
   ```

4. 执行测试命令

   ```shell
   pytest -vs --disable-warnings
   ```
