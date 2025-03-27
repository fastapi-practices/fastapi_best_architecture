<div align="center">

<img alt="Logo 包含了 FBA 三个字母抽象结合，形成了一个类似从地面扩散投影上来的闪电" width="320" src="https://wu-clan.github.io/picx-images-hosting/logo/fba.png">

# FastAPI Best Architecture

简体中文 | [English](./README.md)

企业级后端架构解决方案

**🔥持续更新维护中🔥**

[![GitHub](https://img.shields.io/github/license/fastapi-practices/fastapi_best_architecture)](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-%2300758f)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0%2B-%23336791)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-%23778877)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![Docker](https://img.shields.io/badge/Docker-%232496ED?logo=docker&logoColor=white)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white)](https://discord.com/invite/yNN3wTbVAC)
![Discord](https://img.shields.io/discord/1185035164577972344)

</div>

> [!NOTE]
> 此仓库作为模板库公开，任何人或企业均可免费使用！

## 伪三层架构

mvc 架构作为常规设计模式，在 python web 中也很常见，但是三层架构更令人着迷

在 python web 开发中，三层架构的概念并没有通用标准，所以这里我们称之为伪三层架构

但请注意，我们并没有传统的多应用程序结构（django、springBoot...），如果您不喜欢这种模式，可以使用模板对其进行随意改造！

| 工作流程 | java           | fastapi_best_architecture |
|------|----------------|---------------------------|
| 视图   | controller     | api                       |
| 数据传输 | dto            | schema                    |
| 业务逻辑 | service + impl | service                   |
| 数据访问 | dao / mapper   | crud                      |
| 模型   | model / entity | model                     |

## 特性

- [x] 全局 FastAPI PEP 593 Annotated 参数风格
- [x] 全面 async/await + asgiref 异步设计
- [x] 遵循 RESTful API 规范
- [x] 使用 SQLAlchemy 2.0 全新语法
- [x] 使用 Pydantic v2 版本
- [x] 实现角色菜单 RBAC 访问控制
- [x] 集成 Casbin RBAC 访问控制
- [x] 支持 Celery 异步任务
- [x] 自研 JWT 认证中间件
- [x] 支持全局自定义时间时区
- [x] 支持 Docker / Docker-compose 部署
- [x] 集成 Pytest 单元测试

## 内置功能

- [x] 用户管理：分配角色和权限
- [x] 部门管理：配置组织架构（公司、部门、小组等）
- [x] 菜单管理：设置菜单及按钮级权限
- [x] 角色管理：配置角色、分配菜单和权限
- [x] 字典管理：维护常用参数和配置
- [x] 参数管理：系统常用参数动态配置
- [x] 通知公告：发布和维护系统通知公告信息
- [x] 令牌管理：检测在线状态，支持强制下线
- [x] 多端登录：支持一键切换多端登录模式
- [x] OAuth 2.0：内置自研 OAuth 2.0 授权登录
- [x] 插件系统：热插拔插件设计，降低耦合
- [x] 定时任务：支持定时，异步任务及函数调用
- [x] 代码生成：自动生成代码，支持预览、写入和下载
- [x] 操作日志：记录和查询正常和异常操作
- [x] 登录日志：记录和查询正常和异常登录
- [x] 缓存监控：查询系统缓存信息和命令统计
- [x] 服务监控：查看服务器硬件信息和状态
- [x] 接口文档：自动生成在线交互式 API 文档

## 开发部署

更多详情请查看 [官方文档](https://fastapi-practices.github.io/fastapi_best_architecture_docs/)

## 贡献者

<a href="https://github.com/fastapi-practices/fastapi_best_architecture/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fastapi-practices/fastapi_best_architecture"/>
</a>

## 特别鸣谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Casbin](https://casbin.org/zh/)
- [Ruff](https://beta.ruff.rs/docs/)
- ...

## 互动

[Discord](https://wu-clan.github.io/homepage/)

## 赞助我们

如果此项目能够帮助到你，你可以赞助作者一些咖啡豆表示鼓励：[:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)

## 许可证

本项目由 [MIT](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE) 许可证的条款进行许可

[![Stargazers over time](https://starchart.cc/fastapi-practices/fastapi_best_architecture.svg?variant=adaptive)](https://starchart.cc/fastapi-practices/fastapi_best_architecture)
