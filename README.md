# FastAPI Best Architecture

[![GitHub](https://img.shields.io/github/license/fastapi-practices/fastapi_best_architecture)](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE)
[![Static Badge](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

> [!CAUTION]
> **For 2024-3-22 (announcement)**
>
> The master branch has completed the app architecture refactoring, please pay extra attention to sync fork operations
> to avoid irreparable damage!
>
> We have kept and locked the original branch (legacy-single-app-pydantic-v2), which you can get in the branch selector

English | [简体中文](./README.zh-CN.md)

FastAPI framework based on the front-end and back-end separation of the middle and back-end solutions, follow
the [pseudo three-tier architecture](#pseudo-three-tier-architecture) design, support for **python3.10** and above
versions

Its purpose is to allow you to use it directly as the infrastructure of your new project, this repository as a template
library open to any person or enterprise can be used for free!

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
> username / password: admin / 123456

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

1. [x] User management: system user role management, permission assignment
2. [x] Department Management: Configure the system organization (company, department, group...)
3. [x] Menu Management: Configuration of system menus, user menus, button privilege identification
4. [x] Role Management: Assign role menu privileges, assign role routing privileges
5. [x] Dictionary Management: Maintain common fixed data or parameters within the system.
6. [x] Operation Logs: logging and querying of normal and abnormal system operations.
7. [x] Login Authentication: graphical authentication code background authentication login
8. [x] Login Logs: Logging and querying of normal and abnormal user logins
9. [x] Service Monitoring: server hardware device information and status
10. [x] Scheduled tasks: automated tasks, asynchronous tasks, and function invocation are supported
11. [x] Interface Documentation: Automatically generate online interactive API interface documentation.

## Local development

* Python: 3.10+
* Mysql: 8.0+
* Redis: The latest stable version is recommended
* Nodejs: 14.0+

### Backend

1. Enter the `backend` directory

   ```shell
   cd backend
   ```

2. Install the dependencies

   ```shell
   pip install -r requirements.txt
   ```

3. Create a database `fba` with utf8mb4 encoding.
4. Install and start Redis
5. Create a `.env` file in the `backend` directory.

   ```shell
   touch .env
   
   cp .env.example .env
   ```

6. Modify the configuration files `core/conf.py` and `.env` as needed.
7. database migration [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

   ```shell
   # Generate the migration file
   alembic revision --autogenerate
   
   # Execute the migration
   alembic upgrade head
   ```

8. Start celery worker, beat and flower

   ```shell
   celery -A app.task.celery worker -l info
   
   # Scheduled tasks (optional)
   celery -A app.task.celery beat -l info
   
   # Web monitor (optional)
   celery -A app.task.celery flower --port=8555 --basic-auth=admin:123456
   ```

9. [Initialize test data](#test-data) (Optional)
10. Start fastapi service

   ```shell
   # Help
   fastapi --help
   
   # dev mode
   fastapi dev main.py
   ```

11. Open a browser and visit: http://127.0.0.1:8000/api/v1/docs

### Front end

Jump to [fastapi_best_architecture_ui](https://github.com/fastapi-practices/fastapi_best_architecture_ui) View details

---

### Docker Deployment

> [!WARNING]
>
> Default port conflicts: 8000, 3306, 6379, 5672.
>
> It is recommended to shut down local services: mysql, redis, rabbitmq... before deployment.

1. Go to the `deploy/backend/docker-compose` directory, and create the environment variable file `.env`.

   ```shell
   cd deploy/backend/docker-compose
   
   touch .env.server ../../../backend/.env
   
   cp .env.server ../../../backend/.env
   ```

2. Modify the configuration files `backend/core/conf.py` and `.env` as needed.
3. Execute the one-click startup command

   ```shell
   docker-compose up -d --build
   ```

4. Wait for the command to complete.
5. Open a browser and visit: http://127.0.0.1:8000/api/v1/docs

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

[WeChat / QQ](https://github.com/wu-clan)

## Sponsor us

If this program has helped you, you can sponsor us with some coffee
beans: [:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)

## License

This project is licensed by the terms of
the [MIT](https://github.com/fastapi-practices/fastapi_best_architecture/blob/master/LICENSE) license

[![Stargazers over time](https://starchart.cc/fastapi-practices/fastapi_best_architecture.svg?variant=adaptive)](https://starchart.cc/fastapi-practices/fastapi_best_architecture)
