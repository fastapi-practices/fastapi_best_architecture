# FastAPI Best Architecture

This is a base project of the FastAPI framework.

It‘s purpose is to allow you to develop your project directly with it
as your base project

Support python3.10 and above

## Skill

- [x] FastAPI
- [x] Pydantic
- [x] SQLAlchemy
- [x] Alembic
- [x] MySQL
- [x] Redis
- [x] APScheduler
- [x] Docker

## Clone

```shell
git clone https://github.com/wu-clan/fastapi_best_architecture.git
```

## Use:

### 1：Tradition

1. Install dependencies
    ```shell
    pip install -r requirements.txt
    ```

2. Create a database `fba`, choose utf8mb4 encode
3. Install and start Redis
4. create a `.env` file in the `backend/app/` directory
    ```shell
    cd backend/app/
    touch .env
    ```
5. Copy .env.example to .env and view `backend/app/core/conf.py`, update database configuration information
6. Perform a database migration [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
    ```shell
    cd backend/app/
    
    # Generate the migration file
    alembic revision --autogenerate
    
    # Perform the migration
    alembic upgrade head
    ```
7. Execute the backend/app/main.py file startup service
8. Browser access: http://127.0.0.1:8000/v1/docs

---

### 2：Docker

1. Run the one-click start command in the directory where the `docker-compose.yml` file is located

    ```shell
    docker-compose up -d --build
    ```
2. Wait for the command to finish automatically

3. Browser access: http://127.0.0.1:8000/v1/docs

## Init the test data

Execute the `backend/app/init_test_data.py` file

## Test

Perform tests via pytest

**Tip**: Before the test starts, please execute init the test data first, also, the fastapi service needs to be started

1. First, go to the app directory

   ```shell
   cd backend/app/
   ```

2. Execute the test command

   ```shell
   pytest -vs --disable-warnings
   ```
