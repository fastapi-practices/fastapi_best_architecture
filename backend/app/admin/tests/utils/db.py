#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.database.db import create_async_engine_and_session, create_database_url

TEST_SQLALCHEMY_DATABASE_URL = create_database_url(unittest=True)

_, async_test_db_session = create_async_engine_and_session(TEST_SQLALCHEMY_DATABASE_URL)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """session 生成器"""
    async with async_test_db_session() as session:
        yield session
