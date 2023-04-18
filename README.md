# FastAPI Best Architecture

This is a base project of the FastAPI framework.

It‘s purpose is to allow you to develop your project directly with it
as your base project

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
4. Copy .env.example to .env and view `backend/app/core/conf.py`, update database configuration information
5. Perform a database migration [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
    ```shell
    cd backend/app/
    
    # Generate the migration file
    alembic revision --autogenerate
    
    # Perform the migration
    alembic upgrade head
    ```
6. Execute the backend/app/main.py file startup service
7. Browser access: http://127.0.0.1:8000/v1/docs

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

