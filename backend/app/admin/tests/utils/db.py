#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.db import create_database_url, create_engine_and_session

TEST_SQLALCHEMY_DATABASE_URL = create_database_url(unittest=True)

_, async_test_db_session = create_engine_and_session(TEST_SQLALCHEMY_DATABASE_URL)


async def override_get_db() -> AsyncSession:
    """session 生成器"""
    session = async_test_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()
