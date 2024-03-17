#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.conf import settings
from backend.database.db_mysql import create_engine_and_session

TEST_SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
    f'{settings.DB_PORT}/{settings.DB_DATABASE}_test?charset={settings.DB_CHARSET}'
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
