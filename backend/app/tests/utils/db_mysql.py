#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.conf import settings
from backend.app.database.db_mysql import create_engine_and_session

TEST_DB_DATABASE = settings.DB_DATABASE + '_test'

TEST_SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
    f'{settings.DB_PORT}/{TEST_DB_DATABASE}?charset={settings.DB_CHARSET}'
)

test_async_engine, test_async_db_session = create_engine_and_session(TEST_SQLALCHEMY_DATABASE_URL)


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
