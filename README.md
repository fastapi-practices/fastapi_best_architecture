# FastAPI Best Architecture

[![GitHub](https://img.shields.io/github/license/fastapi-practices/fastapi_best_architecture)](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE)
[![Static Badge](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

> [!NOTE]
> This repository as a template library open to any person or enterprise can be used for free!

English | [简体中文](./README.zh-CN.md)

FastAPI framework based on the front-end and back-end separation of the middle and back-end solutions, follow
the [pseudo three-tier architecture](#pseudo-three-tier-architecture) design, support for **python3.10** and above
versions

**🔥Continuously updated and maintained🔥**

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

## Online Demo

You can view some of the preview screenshots
in [fastapi_best_architecture_ui](https://github.com/fastapi-practices/fastapi_best_architecture_ui)

Luckily, we now have a demo site: [FBA UI](https://fba.xwboy.top/)

> tester: test / 123456
>
> super: admin / 123456

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
- [x] Code generation: back-end code is automatically generated, supporting preview, write and download.
- [x] Operation log: logging and querying of normal and abnormal system operations.
- [x] Login authentication: graphical captcha backend authentication login
- [x] Logging: logging and querying of normal and abnormal user logins
- [x] Service monitoring: server hardware device information and status
- [x] Timed tasks: automated tasks, asynchronous tasks, support for function calls
- [x] Interface Documentation: Automatically generate online interactive API interface documentation.

## Project structure

```
├─📁 backend--------------- # Backend
│ ├─📁 alembic------------- # DB migration
│ ├─📁 app----------------- # Application
│ │ ├─📁 admin------------- # System admin
│ │ │ ├─📁 api------------- # Interface
│ │ │ ├─📁 crud------------ # CRUD
│ │ │ ├─📁 model----------- # SQLA model
│ │ │ ├─📁 schema---------- # Data transmit
│ │ │ ├─📁 service--------- # Service
│ │ │ └─📁 tests----------- # Pytest
│ │ ├─📁 generator--------- # Code generate
│ │ └─📁 task-------------- # Celery task
│ ├─📁 common-------------- # public resources
│ ├─📁 core---------------- # Core configuration
│ ├─📁 database------------ # Database connection
│ ├─📁 log----------------- # Log
│ ├─📁 middleware---------- # Middlewares
│ ├─📁 scripts------------- # Scripts
│ ├─📁 sql----------------- # SQL files
│ ├─📁 static-------------- # Static files
│ ├─📁 templates----------- # Template files
│ └─📁 utils--------------- # Toolkit
└─📁 deploy---------------- # Server deployment
```

## Local development / Docker deployment

For more details, please check
the [official documentation](https://fastapi-practices.github.io/fastapi_best_architecture_docs/)

## Test data

Initialize the test data using the `backend/sql/init_test_data.sql` file.

## Development Process

(For reference only)

1. define the database model (model)
2. define the data validation model (schema)
3. define the view (api) and routing (router)
4. write business (service)
5. write database operations (crud)

## Testing

Execute unit tests through `pytest`.

1. create a test database `fba_test` with utf8mb4 encoding
2. create database tables using the `backend/sql/create_tables.sql` file
3. initialize the test data using the `backend/sql/init_pytest_data.sql` file
4. Go to the `backend` directory and execute the test commands.

   ```shell
   cd backend/
   
   pytest -vs --disable-warnings
   ```

## Status

![Alt](https://repobeats.axiom.co/api/embed/b2174ef1abbebaea309091f1c998fc97d0c1536a.svg "Repo beats analytics image")

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

[WeChat / QQ](https://wu-clan.github.io/homepage/)

## Sponsor us

If this program has helped you, you can sponsor us with some coffee
beans: [:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)

## License

This project is licensed by the terms of
the [MIT](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE) license

[![Stargazers over time](https://starchart.cc/fastapi-practices/fastapi_best_architecture.svg?variant=adaptive)](https://starchart.cc/fastapi-practices/fastapi_best_architecture)
