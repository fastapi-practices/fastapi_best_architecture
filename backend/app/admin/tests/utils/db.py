from __future__ import annotations

from typing import TYPE_CHECKING

from backend.database.db import create_database_url, create_async_engine_and_session

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio.session import AsyncSession

TEST_SQLALCHEMY_DATABASE_URL = create_database_url(unittest=True)

_, async_test_db_session = create_async_engine_and_session(TEST_SQLALCHEMY_DATABASE_URL)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """session 生成器"""
    async with async_test_db_session() as session:
        yield session
