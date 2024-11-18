# FastAPI 最佳架构

[![GitHub](https://img.shields.io/github/license/fastapi-practices/fastapi_best_architecture)](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE)
[![Static Badge](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

> [!NOTE]
> 此仓库作为模板库公开，任何人或企业均可免费使用！

简体中文 | [English](./README.md)

基于 FastAPI 框架的前后端分离中后台解决方案，遵循[伪三层架构](#伪三层架构)设计， 支持 **python3.10** 及以上版本

**🔥持续更新维护中🔥**

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

## 在线预览

你可以在 [fastapi_best_architecture_ui](https://github.com/fastapi-practices/fastapi_best_architecture_ui) 中查看部分预览截图

演示入口请查看 [官方文档](https://fastapi-practices.github.io/fastapi_best_architecture_docs/)

> 测试员：tester / 123456
>
> 管理员：admin / 123456

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

- [x] 用户管理：系统用户角色管理，权限分配
- [x] 部门管理：配置系统组织机构（公司、部门、小组...）
- [x] 菜单管理：配置系统菜单，用户菜单，按钮权限标识
- [x] 角色管理：角色菜单权限分配，角色路由权限分配
- [x] 字典管理：维护系统内部常用固定数据或参数
- [x] 代码生成：后端代码自动生成，支持预览，写入及下载
- [x] 操作日志：系统正常和异常操作的日志记录与查询
- [x] 登录认证：图形验证码后台认证登录
- [x] 登录日志：用户正常和异常登录的日志记录与查询
- [x] 服务监控：服务器硬件设备信息与状态
- [x] 定时任务：自动化任务，异步任务，支持函数调用
- [x] 接口文档：自动生成在线交互式 API 接口文档

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

[TG / Discord](https://wu-clan.github.io/homepage/)

## 赞助我们

如果此项目能够帮助到你，你可以赞助作者一些咖啡豆表示鼓励：[:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)

## 许可证

本项目由 [MIT](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE) 许可证的条款进行许可

[![Stargazers over time](https://starchart.cc/fastapi-practices/fastapi_best_architecture.svg?variant=adaptive)](https://starchart.cc/fastapi-practices/fastapi_best_architecture)
