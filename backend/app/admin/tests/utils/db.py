#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.conf import settings
from backend.database.db import create_engine_and_session

TEST_SQLALCHEMY_DATABASE_URL = None

# 数据库连接
if settings.DATABASE_TYPE == 'mysql':
    TEST_SQLALCHEMY_DATABASE_URL = URL.create(
        drivername='mysql+asyncmy',
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DATABASE,
        query={'charset': settings.MYSQL_CHARSET},
    )
elif settings.DATABASE_TYPE == 'pgsql':
    TEST_SQLALCHEMY_DATABASE_URL = URL.create(
        drivername='postgresql+asyncpg',
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DATABASE,
    )

_, test_async_db_session = create_engine_and_session(TEST_SQLALCHEMY_DATABASE_URL)


async def override_get_db() -> AsyncSession:
    """session 生成器"""
    session = test_async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()
