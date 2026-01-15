from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.database.db import create_database_async_engine, create_database_async_session, create_database_url

# SQLA 数据库链接
TEST_SQLALCHEMY_DATABASE_URL = create_database_url(unittest=True)

# SALA 异步引擎和会话
async_test_engine = create_database_async_engine(TEST_SQLALCHEMY_DATABASE_URL)
async_test_db_session = create_database_async_session(async_test_engine)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    async with async_test_db_session() as session:
        yield session
