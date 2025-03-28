<div align="center">

<img alt="The logo includes the abstract combination of the three letters FBA, forming a lightning bolt that seems to spread out from the ground" width="320" src="https://wu-clan.github.io/picx-images-hosting/logo/fba.png">

# FastAPI Best Architecture

English | [简体中文](./README.zh-CN.md)

Enterprise-level backend architecture solution

**🔥Continuously updated and maintained🔥**

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
> This repository as a template library open to any person or enterprise can be used for free!

## Pseudo 3-tier architecture

The mvc architecture is a common design pattern in python web, but the 3-tier architecture is even more fascinating

In python web development, there is no common standard for the concept of 3-tier architecture, so we'll call it a
pseudo 3-tier architecture here

But please note that we don't have a traditional multi-app structure (django, springBoot...) If you don't like this
pattern, use templates to transform it to your heart's content!

| workflow       | java           | fastapi_best_architecture |
|----------------|----------------|---------------------------|
| view           | controller     | api                       |
| data transmit  | dto            | schema                    |
| business logic | service + impl | service                   |
| data access    | dao / mapper   | crud                      |
| model          | model / entity | model                     |

## Features

- [x] Global FastAPI PEP 593 Annotated parameter style
- [x] Comprehensive async/await + asgiref asynchronous design
- [x] Adheres to RESTful API specifications
- [x] Uses SQLAlchemy 2.0 with new syntax
- [x] Uses Pydantic v2 version
- [x] Implements role-menu RBAC access control
- [x] Integrates Casbin RBAC access control
- [x] Supports Celery asynchronous tasks
- [x] Custom-developed JWT authentication middleware
- [x] Supports global custom time zones
- [x] Supports Docker / Docker-compose deployment
- [x] Integrates Pytest unit testing

## Built-in Functions

- [x] User Management: Assign roles and permissions
- [x] Department Management: Configure organizational structure (company, department, team, etc.)
- [x] Menu Management: Set up menus and button-level permissions
- [x] Role Management: Configure roles, assign menus and permissions
- [x] Dictionary Management: Maintain common parameters and configurations
- [x] Parameter Management: Dynamically configure commonly used system parameters
- [x] Notification Announcements: Publish and maintain system notification and announcement information
- [x] Token Management: Detect online status, support forced logout
- [x] Multi-device Login: Support one-click switching between multi-device login modes
- [x] OAuth 2.0: Built-in custom-developed OAuth 2.0 authorization login
- [x] Plugin System: Hot-swappable plugin design to reduce coupling
- [x] Scheduled Tasks: Support scheduled, asynchronous tasks, and function calls
- [x] Code Generation: Automatically generate code with preview, write, and download support
- [x] Operation Logs: Record and query normal and abnormal operations
- [x] Login Logs: Record and query normal and abnormal logins
- [x] Cache Monitoring: Query system cache information and command statistics
- [x] Service Monitoring: View server hardware information and status
- [x] API Documentation: Automatically generate online interactive API documentation

## Development and deployment

For more details, please check
the [official documentation](https://fastapi-practices.github.io/fastapi_best_architecture_docs/)

## Contributors

<a href="https://github.com/fastapi-practices/fastapi_best_architecture/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fastapi-practices/fastapi_best_architecture"/>
</a>

## Special thanks

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Casbin](https://casbin.org/zh/)
- [Ruff](https://beta.ruff.rs/docs/)
- ...

## Interactivity

[Discord](https://wu-clan.github.io/homepage/)

## Sponsor us

If this program has helped you, you can sponsor us with some coffee
beans: [:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)

## License

This project is licensed by the terms of
the [MIT](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE) license

[![Stargazers over time](https://starchart.cc/fastapi-practices/fastapi_best_architecture.svg?variant=adaptive)](https://starchart.cc/fastapi-practices/fastapi_best_architecture)
