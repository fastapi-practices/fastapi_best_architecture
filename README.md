<div align="center">

<img alt="The logo includes the abstract combination of the three letters FBA, forming a lightning bolt that seems to spread out from the ground" width="320" src="https://wu-clan.github.io/picx-images-hosting/logo/fba.png">

# FastAPI Best Architecture

English | [简体中文](./README.zh-CN.md)

A backend and frontend separation solution based on the FastAPI framework, following
the [pseudo three-tier architecture](#pseudo-three-tier-architecture) design, supporting **Python 3.10** and above
versions

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

## Pseudo three-tier architecture

The mvc architecture is a common design pattern in python web, but the three-tier architecture is even more fascinating

In python web development, there is no common standard for the concept of three-tier architecture, so we'll call it a
pseudo three-tier architecture here

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

- [x] Design with FastAPI PEP 593 Annotated Parameters
- [x] Global asynchronous design with async/await + asgiref
- [x] Follows Restful API specification
- [x] Global SQLAlchemy 2.0 syntax
- [x] Pydantic v1 and v2 (different branches)
- [x] Casbin RBAC access control model
- [x] Role menu RBAC access control model
- [x] Celery asynchronous tasks
- [x] JWT middleware whitelist authentication
- [x] Global customizable time zone time
- [x] Docker / Docker-compose deployment
- [x] Pytest Unit Testing

## Built-in features

- [x] User management: management of system user roles, assignment of permissions
- [x] Departmental management: Configuration of the system organization (company, department, group, ...)
- [x] Menu management: Configuration of system menus, user menus, button permission labels
- [x] Role management: assignment of role menu privileges, assignment of role routing privileges
- [x] Dictionary management: maintenance of commonly used fixed data or parameters within the system
- [x] Token management：System user online status detection, supports kicking user offline
- [x] Code generation: back-end code is automatically generated, supporting preview, write and download.
- [x] Operation log: logging and querying of normal and abnormal system operations.
- [x] Login authentication: graphical captcha backend authentication login
- [x] Logging: logging and querying of normal and abnormal user logins
- [x] Service monitoring: server hardware device information and status
- [x] Timed tasks: automated tasks, asynchronous tasks, support for function calls
- [x] Interface Documentation: Automatically generate online interactive API interface documentation.

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

[TG / Discord](https://wu-clan.github.io/homepage/)

## Sponsor us

If this program has helped you, you can sponsor us with some coffee
beans: [:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)

## License

This project is licensed by the terms of
the [MIT](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE) license

[![Stargazers over time](https://starchart.cc/fastapi-practices/fastapi_best_architecture.svg?variant=adaptive)](https://starchart.cc/fastapi-practices/fastapi_best_architecture)
