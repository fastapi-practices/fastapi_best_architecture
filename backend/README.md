# FastAPI Best Architecture - Backend

## Docker

1. Make sure you're at the root of the project
2. Run the following Docker command to build container:

   ```shell
   docker build -f Dockerfile -t fba_backend_independent .
   ```

3. Start container

   Native boot needs to change `127.0.0.1` in `.env` to `host.docker.internal`

   ```shell
   docker run -d -p 8000:8000 --name fba_server fba_backend_independent
   ```

## Contributing

1. Prerequisites

    - Python >= 3.10
    - Git
    - [uv](https://docs.astral.sh/uv/getting-started/installation/)
    - Fork this repository to your GitHub account

2. Installation and setup

   Clone your forked repository:

   ```shell
   git clone https://github.com/<your account>/fastapi_best_architecture.git
   ```

   Go to the root directory of the project, open the terminal, and run the following command:

   ```sh
   uv sync --frozen
   ```

3. Checkout

   Checkout a new branch and make your changes

   ```shell
   git checkout -b your-new-feature-branch
   ```

4. Format and Lint

   Auto-formatting and lint via `pre-commit`

   ```shell
   pre-commit run --all-files
   ```

5. Commit and push

   Commit your changes and push your branch to the GitHub.

6. PR

   Create a PR via GitHub

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
