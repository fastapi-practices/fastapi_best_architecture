#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ruff: noqa: F403, F401, I001, RUF100
import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

sys.path.append('../')

from backend.common.model import MappedBase
from backend.core import path_conf
from backend.database.db import SQLALCHEMY_DATABASE_URL
from backend.plugin.tools import get_plugin_models

# import your new model here
from backend.app.admin.model import *  # noqa: F401
from backend.app.generator.model import *  # noqa: F401

# import plugin model
for cls in get_plugin_models():
    class_name = cls.__name__
    if class_name in globals():
        print(f'\nWarning: Class "{class_name}" already exists in global namespace.')
    else:
        globals()[class_name] = cls

if not os.path.exists(path_conf.ALEMBIC_VERSION_DIR):
    os.makedirs(path_conf.ALEMBIC_VERSION_DIR)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# model's MetaData object
# for 'autogenerate' support
target_metadata = MappedBase.metadata

# other values from the config, defined by the needs of env.py,
alembic_config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL.render_as_string(hide_password=False))


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = alembic_config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        compare_type=True,
        compare_server_default=True,
        transaction_per_migration=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    # 当迁移无变化时，不生成迁移记录
    def process_revision_directives(context, revision, directives):
        if alembic_config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                print('\nNo changes in model detected')

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        transaction_per_migration=True,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
