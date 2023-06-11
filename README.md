# FastAPI Best Architecture

English | [简体中文](./README.zh-CN.md)

This is a base project for the FastAPI framework, using a pseudo three-tier architecture, **still in production**.

It is intended to allow you to use it directly as your infrastructure to develop your project, this repository as a
template library public, can be used directly

Support **python3.10** and above

## Pseudo three-tier architecture

In python web frameworks, the mvc architecture is the most common, but for restful users, the three-tier architecture is
the way to go

But in python development, there is no universal standard for the concept of a three-tier architecture, so here I call
it a pseudo three-tier architecture

| workflow        | java           | fastapi_best_architecture |
|-----------------|----------------|---------------------------|
| view            | controller     | api / view                |
| data validation | dto            | schema                    |
| business logic  | service + impl | service                   |
| data access     | dao / mapper   | crud                      |
| model           | model / entity | model                     |

## Features

- [x] FastAPI New Features
- [x] Asynchronous design
- [x] RESTful API specification
- [x] SQLAlchemy 2.0 syntax
- [x] Pydantic Data Validation
- [x] Casbin RBAC Permission Control
- [x] APScheduler Timed Tasks
- [x] JWT Authentication
- [x] Redis Caching
- [x] Docker Deployment
- [x] Pytest testing

## Getting started:

### 1: Legacy mode

1. Install dependencies
    ```shell
    pip install -r requirements.txt
    ```

2. Create a database ``fba``, choose utf8mb4 encoding
3. Install and start Redis
4. Create a `.env` file in the `backend/app/` directory

    ```shell
    cd backend/app/
    touch .env
    ```

5. Copy `.env.example` to `.env`

   ```shell
   cp .env.example .env
   ```

6. Database migration [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

   ```shell
   cd backend/app/

   # Generate migration file
   alembic revision --autogenerate

   # Execute the migration
   alembic upgrade head
    ```

7. Execute the `backend/app/main.py` file to start the service
8. Browser access: http://127.0.0.1:8000/v1/docs

---

### 2: Docker

1. Go to the directory where the ``docker-compose.yml`` file is located and create the environment variable
   file ``.env``

   ```shell
   cp .env.server ../../backend/app/.env
   
   # This command is optional
   cp .env.docker .env
   ```

2. Execute the one-click boot command

   ```shell
   docker-compose up -d -build
   ```

3. Wait for the command to complete automatically
4. Visit the browser: http://127.0.0.1:8000/v1/docs

## Test data

Execute ``backend/app/init_test_data.py`` file to automatically create test data

## Development

Development process, for reference only

1. Define the database model (model) and remember to perform database migration for each change
2. Define the data validation model (schema)
3. Define the business logic (service)
4. Define routes (router) and views (api)
5. Write database operations (crud)

## Test

Execute tests via pytest

1. Create the test database `fba_test`, select utf8mb4 encoding
2. Enter the app directory

   ```shell
   cd backend/app/
   ```

3. Initialize the test data

   ```shell
   python tests/init_test_data.py
   ```

4. Execute the test command

   ```shell
   pytest -vs --disable-warnings
   ```

## Thanks

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Casbin](https://casbin.org/zh/)
- [Ruff](https://beta.ruff.rs/docs/)
- ......

## License

This project is licensed under the terms of the MIT license
