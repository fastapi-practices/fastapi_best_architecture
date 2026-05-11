# SQL Server Support Design

## Goal

Add SQL Server 2019+ as a first-class database option alongside MySQL and PostgreSQL. The support must cover runtime connections, `uv run fba init --auto`, database creation, table/data initialization, plugin SQL installation/removal, Alembic, documentation, and the GitHub PR deliverable.

## Decisions

- SQL Server support will be implemented by extending the existing database-type dispatch pattern, not by introducing a new adapter layer.
- SQL Server will use SQLAlchemy's async `mssql+aioodbc` dialect.
- The project will add a runtime dependency on `aioodbc`.
- Users must install Microsoft ODBC Driver 18 for SQL Server separately in their local or container environment.
- SQL Server connection configuration will be explicit and configurable through `.env`.
- The support baseline is SQL Server 2019+.
- `docker-compose.yml` will include a commented SQL Server service example, matching the existing optional MySQL style.

## Architecture

SQL Server becomes a peer of `mysql` and `postgresql`.

Changes:

- Add `sqlserver` to `DataBaseType`.
- Add `sqlserver` to `Settings.DATABASE_TYPE`.
- Add SQL Server environment variables:
  - `DATABASE_DRIVER='ODBC Driver 18 for SQL Server'`
  - `DATABASE_TRUST_SERVER_CERTIFICATE=true`
- Extend `create_database_url()` to generate `mssql+aioodbc` URLs.
- Extend `create_database()` to create and recreate SQL Server databases through `master`.
- Add `SQLSERVER_SCRIPT_DIR` in `path_conf.py`.
- Update SQL script selection in `get_sql_scripts()`, `get_plugin_sql()`, and `get_plugin_destroy_sql()` to resolve directories for all three database types.
- Add SQL Server SQL directories for the main initialization data and every current plugin.
- Update README files to mention SQL Server 2019+ support.

## Connection Design

For SQL Server, `create_database_url(with_database=False)` connects to `master`. `create_database_url(with_database=True)` connects to `settings.DATABASE_SCHEMA`.

The SQL Server URL uses:

- driver name from `settings.DATABASE_DRIVER`
- `TrustServerCertificate=yes/no` from `settings.DATABASE_TRUST_SERVER_CERTIFICATE`
- `LongAsMax=Yes` for ODBC Driver 18 long string behavior

The existing connection pool settings and SQLAlchemy pool observability listeners continue to be used.

## Initialization Flow

`uv run fba init --auto` keeps the current three-step flow:

1. Configure `.env`.
2. Optionally create or recreate the database.
3. Create tables and execute main and plugin SQL scripts.

SQL Server additions:

- `setup_env_file()` adds `sqlserver` to the database choices.
- SQL Server defaults are port `1433` and user `sa`.
- SQL Server prompts include ODBC Driver and trust-server-certificate configuration.
- `create_database()` uses SQL Server-specific SQL:
  - check `sys.databases`
  - set the target database to `SINGLE_USER WITH ROLLBACK IMMEDIATE` before dropping
  - drop and recreate the target database

## SQL Script Compatibility

Main SQL Server scripts:

- `backend/sql/sqlserver/init_test_data.sql`
- `backend/sql/sqlserver/init_snowflake_test_data.sql`

Each existing plugin receives SQL Server equivalents for init and destroy scripts, including snowflake variants where the MySQL/PostgreSQL plugin already has them.

SQL Server script conversion rules:

- Replace `now()` with `GETDATE()` or fixed timestamp literals.
- Replace PostgreSQL `DO $$ ... RETURNING ... INTO ...` blocks with T-SQL `DECLARE`, `INSERT`, and `SCOPE_IDENTITY()` patterns.
- Replace PostgreSQL `setval(...)` or MySQL auto-increment reseeding with `DBCC CHECKIDENT`.
- Replace `true` and `false` with `1` and `0` for SQL Server `BIT` fields.
- Replace PostgreSQL `gen_random_uuid()` with `NEWID()`.
- Replace PostgreSQL `decode(hex, 'hex')` with `CONVERT(varbinary(max), hex, 2)` if the destination column is binary.
- Quote SQL Server reserved identifiers where needed.

`parse_sql_script()` keeps its whitelist safety model. It will be expanded only for safe initialization prefixes needed by SQL Server, such as `DECLARE` and `DBCC`; destructive prefixes remain limited to destroy scripts.

## Runtime and Alembic

Runtime uses the same `create_database_url()` path as other databases. Existing ORM models should remain shared. If SQL Server exposes type/default incompatibilities, only targeted model-level fixes should be made, such as SQLAlchemy variants or default adjustments.

Alembic continues to read `SQLALCHEMY_DATABASE_URL` from `backend.database.db`. No separate Alembic entrypoint is planned. Online and offline migration flows should work through the generated `mssql+aioodbc` URL.

## Docker Compose

`docker-compose.yml` will add a commented SQL Server service example, similar to the current commented MySQL section. It should include the SQL Server 2019+ image, port `1433`, required acceptance/password environment variables, and comments showing how to switch backend dependencies and wait-for-it targets.

## Documentation

README updates should mention:

- SQL Server 2019+ support.
- Microsoft ODBC Driver 18 requirement.
- The configurable `.env` fields for SQL Server.
- `uv run fba init --auto` can choose `sqlserver`.

## Validation

Static checks:

- `uv run ruff check`
- `uv run pytest`

CLI checks:

- `uv run fba init --help`
- `uv run fba init --auto`, selecting `sqlserver`, verifying generated `.env`.

Database checks:

- Run full initialization against SQL Server 2019+.
- Confirm database creation, ORM table creation, main data initialization, and plugin data initialization.
- Start the app with `uv run fba run`.
- Verify at least one initialized-data path, such as login or a basic endpoint.

Regression checks:

- PostgreSQL remains the default behavior.
- MySQL script lookup still resolves `mysql` directories.
- Plugin install/remove chooses SQL Server scripts when `DATABASE_TYPE=sqlserver`.

## PR Deliverable

After implementation and validation, create a branch, commit the implementation, push to GitHub, and open a PR. The PR description should include:

- Summary of SQL Server support.
- SQL Server 2019+ and ODBC Driver 18 requirements.
- Validation commands and outcomes.
- Any SQL Server database checks that could not be run locally.
