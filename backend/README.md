# FBA Project - Backend

## Docker

> [!IMPORTANT]
> Due to Docker context limitations, you can't build an image in this directory

1. Make sure you're at the root of the project
2. Run the following Docker command to build container:

   ```shell
   docker build -f backend/Dockerfile -t fba_backend_independent .
   ```

3. Start container

   Native boot needs to change `127.0.0.1` in `.env` to `host.docker.internal`

   ```shell
   docker run -d -p 8000:8000 --name fba_server fba_backend_independent
   ```

## Contributing

1. Prerequisites

   You'll need the following prerequisites:
    - Any python version between Python >= 3.10
    - Git
    - [uv](https://docs.astral.sh/uv/getting-started/installation/)
    - Fork this repository to your GitHub account

2. Installation and setup

   Clone your fork and cd into the repo directory

   ```shell
   git clone https://github.com/<your username>/fastapi_best_architecture.git
   
   cd fastapi_best_architecture/backend
   
   uv venv
   
   uv pip install -r requirements.txt
   ```

3. Checkout a new branch and make your changes

   ```shell
   # Checkout a new branch and make your changes
   git checkout -b your-new-feature-branch
   ```

4. Run linting

   ```shell
   # Run automated code formatting and linting
   pre-commit run --all-files
   ```

5. Commit and push your changes

   Commit your changes, push your branch to GitHub, and create a pull request.

## Scripts

> [!WARNING]
>
> The following script may not apply to the Windows platform
>
> It is recommended to execute under the backend directory, and chmod authorization may be required

- `pre_start.sh`: Perform automatic database migration and create database tables

- `celery-start.sh`: For celery docker script, implementation is not recommended

- `scripts/format.sh`: Perform ruff format check

- `scripts/lint.sh`: Perform pre-commit formatting

- `scripts/export.sh`: Execute uv export dependency package
