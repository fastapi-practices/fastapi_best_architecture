# FastAPI 最佳架构

[![GitHub](https://img.shields.io/github/license/fastapi-practices/fastapi_best_architecture)](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE)
[![Static Badge](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

> [!CAUTION]
> **2023-12-21 (公告)**
>
> 主分支已完全迁移到 pydantic-v2，请格外注意 sync fork 操作，以免造成不可挽回的损失！
> 我们保留并锁定了原始分支（pydantic-v1），您可以在分支选择器中找到它

Pydantic-V2 完工 🎉

简体中文 | [English](./README.md)

基于 FastAPI 框架的前后端分离中后台解决方案，遵循[伪三层架构](#伪三层架构)设计， 支持 **python3.10** 及以上版本

它的目的是让你可以直接用它作为你新项目的基础架构，本仓库作为模板库公开，任何人或企业均可免费使用

**持续更新维护中**

## 伪三层架构

mvc 架构作为常规设计模式，在 python web 中也很常见，但是三层架构更令人着迷

在 python web 开发中，三层架构的概念并没有通用标准，所以这里我们称之为伪三层架构

| 工作流程 | java           | fastapi_best_architecture |
|------|----------------|---------------------------|
| 视图   | controller     | api                       |
| 数据传输 | dto            | schema                    |
| 业务逻辑 | service + impl | service                   |
| 数据访问 | dao / mapper   | crud                      |
| 模型   | model / entity | model                     |

## 在线预览

遗憾的是，我们没有资金提供在线预览，您可以通过查看[本地开发](#本地开发)进行部署，或直接使用 [Docker](#docker-部署)
进行部署，或者在 [fastapi_best_architecture_ui](https://github.com/fastapi-practices/fastapi_best_architecture_ui)
查看部分截图预览

## 特征

- [x] 使用 FastAPI PEP 593 Annotated 参数设计
- [x] async/await + asgiref 的全局异步设计
- [x] 遵循 Restful API 规范
- [x] 全局 SQLAlchemy 2.0 语法
- [x] Pydantic v1 和 v2 (不同分支)
- [x] Casbin RBAC 访问控制模型
- [x] 角色菜单 RBAC 访问控制模型
- [x] Celery 异步任务
- [x] JWT 中间件白名单认证
- [x] 全局自定义时区时间
- [x] Docker / Docker-compose 部署
- [x] Pytest 单元测试

## 内置功能

1. [x] 用户管理：系统用户角色管理，权限分配
2. [x] 部门管理：配置系统组织机构（公司、部门、小组...）
3. [x] 菜单管理：配置系统菜单，用户菜单，按钮权限标识
4. [x] 角色管理：角色菜单权限分配，角色路由权限分配
5. [x] 字典管理：维护系统内部常用固定数据或参数
6. [x] 操作日志：系统正常操作和异常操作日志记录和查询
7. [x] 登录认证：图形验证码后台认证登录
8. [x] 登录日志：用户正常登录和异常登录的日志记录与查询
9. [x] 服务监控：服务器硬件设备信息与状态
10. [x] 定时任务：自动化任务，异步任务，支持函数调用
11. [x] 接口文档：自动生成在线交互式 API 接口文档

## 本地开发

* Python 3.10+
* Mysql 8.0+
* Redis 推荐最新稳定版
* Nodejs 14.0+

### 后端

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

7. 启动 celery worker 和 beat

   ```shell
   celery -A tasks worker --loglevel=INFO
   # 可选，如果您不需要使用计划任务
   celery -A tasks beat --loglevel=INFO
   ```

8. 按需修改配置文件
9. 执行 `backend/app/main.py` 文件启动服务
10. 浏览器访问：http://127.0.0.1:8000/api/v1/docs

---

### 前端

跳转 [fastapi_best_architecture_ui](https://github.com/fastapi-practices/fastapi_best_architecture_ui) 查看详情

### Docker 部署

> [!WARNING]
> 默认端口冲突：8000，3306，6379，5672
>
> 最佳做法是在部署之前关闭本地服务：mysql，redis，rabbitmq...

1. 进入 `docker-compose.yml` 文件所在目录，创建环境变量文件`.env`

   ```shell
   cd deploy/docker-compose/
   
   cp .env.server ../../backend/app/.env
   
   # 此命令为可选
   cp .env.docker .env
   ```

2. 按需修改配置文件
3. 执行一键启动命令

   ```shell
   docker-compose up -d --build
   ```

4. 等待命令自动完成
5. 浏览器访问：http://127.0.0.1:8000/api/v1/docs

## 测试数据

使用 `backend/sql/init_test_data.sql` 文件初始化测试数据

## 开发流程

仅供参考

### 后端：

1. 定义数据库模型（model），每次变化记得执行数据库迁移
2. 定义数据验证模型（schema）
3. 定义路由（router）和视图（api）
4. 定义业务逻辑（service）
5. 编写数据库操作（crud）

### 前端

跳转 [fastapi_best_architecture_ui](https://github.com/fastapi-practices/fastapi_best_architecture_ui) 查看详情

## 测试

通过 pytest 执行单元测试

1. 创建测试数据库 `fba_test`，选择 utf8mb4 编码
2. 使用 `backend/sql/create_tables.sql` 文件创建数据库表
3. 使用 `backend/sql/init_pytest_data.sql` 文件初始化测试数据
4. 进入app目录

   ```shell
   cd backend/app/
   ```

5. 执行测试命令

   ```shell
   pytest -vs --disable-warnings
   ```

## 状态

![Alt](https://repobeats.axiom.co/api/embed/b2174ef1abbebaea309091f1c998fc97d0c1536a.svg "Repo beats analytics image")

## 贡献者

<span style="margin: 0 5px;" ><a href="https://github.com/wu-clan" ><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/52145145?v=4&h=60&w=60&fit=cover&mask=circle&maxage=7d" /></a></span>
<span style="margin: 0 5px;" ><a href="https://github.com/downdawn" ><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/41266749?v=4&h=60&w=60&fit=cover&mask=circle&maxage=7d" /></a></span>

## 特别鸣谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Casbin](https://casbin.org/zh/)
- [Ruff](https://beta.ruff.rs/docs/)
- ...

## 互动

有且仅有当前一个频道，请注意辨别真伪

| [直链跳转](https://t.me/+ZlPhIFkPp7E4NGI1) |
|----------------------------------------|
| Telegram（科学上网）                         |

## 赞助我们

如果此项目能够帮助到你，你可以赞助作者一些咖啡豆表示鼓励 :coffee:

<table>
  <tr>
    <td><img src="https://github.com/wu-clan/image/blob/master/pay/weixin.jpg?raw=true" width="180px" alt="Wechat"/>
    <td><img src="https://github.com/wu-clan/image/blob/master/pay/zfb.jpg?raw=true" width="180px" alt="Alipay"/>
    <td><img src="https://github.com/wu-clan/image/blob/master/pay/ERC20.jpg?raw=true" width="180px" alt="0x40D5e2304b452256afD9CE2d3d5531dc8d293138"/>
  </tr>
  <tr>
    <td align="center">微信</td>
    <td align="center">支付宝</td>
    <td align="center">ERC20</td>
  </tr>
</table>

## 许可证

本项目根据 [MIT](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE) 许可证的条款进行许可
