# FastAPI 最佳架构

简体中文 | [English](./README.md)

这是 FastAPI 框架的一个基础项目，使用伪三层架构，**目前还在制作中**

它的目的是让你可以直接用它作为你的基础架构来开发你的项目，本仓库作为模板库公开，可直接使用

支持 **python3.10** 及以上版本

## 伪三层架构

在 python 的 web 框架中，mvc 架构是最常见的，但是对于 restful 用户，三层架构是不二选择

但是在 python 开发中，三层架构的概念并没有通用标准，所以这里我称之为伪三层架构

| 工作流程 | java           | fastapi_best_architecture |
|------|----------------|---------------------------|
| 视图   | controller     | api / view                |
| 数据验证 | dto            | schema                    |
| 业务逻辑 | service + impl | service                   |
| 数据访问 | dao / mapper   | crud                      |
| 模型   | model / entity | model                     |

## 特征

- [x] FastAPI 新特性
- [x] 异步设计
- [x] RESTful API 规范
- [x] SQLAlchemy 2.0 语法
- [x] Pydantic 数据验证
- [x] Casbin RBAC 权限控制
- [x] APScheduler 定时任务
- [x] JWT 认证
- [x] Redis 缓存
- [x] Docker 部署
- [x] Pytest 测试

## 开始：

### 1：传统模式

1. 安装依赖项
    ```shell
    pip install -r requirements.txt
    ```

2. 创建一个数据库 `fba`，选择 utf8mb4 编码
3. 安装并启动 Redis
4. 在 `backend/app/` 目录下创建一个 `.env` 文件

    ```shell
    cd backend/app/
    touch .env
    ```

5. 复制 `.env.example` 到 `.env`

   ```shell
   cp .env.example .env
   ```

6. 数据库迁移 [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

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

1. 进入 `docker-compose.yml` 文件所在目录，创建环境变量文件`.env`

   ```shell
   cp .env.server ../../backend/app/.env
   
   # 此命令为可选
   cp .env.docker .env
   ```

2. 执行一键启动命令

   ```shell
   docker-compose up -d -build
   ```

3. 等待命令自动完成
4. 浏览器访问：http://127.0.0.1:8000/v1/docs

## 测试数据

执行 `backend/app/init_test_data.py` 文件，自动创建测试数据

## 开发

开发流程，仅供参考

1. 定义数据库模型（model），每次变化记得执行数据库迁移
2. 定义数据验证模型（schema）
3. 定义路由（router）和视图（api）
4. 定义业务逻辑（service）
5. 编写数据库操作（crud）

## 测试

通过 pytest 执行测试

1. 创建测试数据库 `fba_test`，选择 utf8mb4 编码
2. 进入app目录

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

## 鸣谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Casbin](https://casbin.org/zh/)
- [Ruff](https://beta.ruff.rs/docs/)
- ......

## 许可证

本项目根据 MIT 许可证的条款进行许可
