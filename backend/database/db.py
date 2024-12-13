import sys

from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.common.log import log
from backend.common.model import MappedBase
from backend.core.conf import settings

# 数据库连接
SQLALCHEMY_DATABASE_URL = None
if settings.DATABASE_TYPE == 'mysql':
    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername='mysql+asyncmy',
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DATABASE,
        query={'charset': settings.MYSQL_CHARSET},
    )
elif settings.DATABASE_TYPE == 'pgsql':
    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername='postgresql+asyncpg',
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DATABASE,
    )
else:
    raise ValueError(f'不支持的数据库类型: {settings.DATABASE_TYPE}')


def create_engine_and_session(url: str | URL):
    try:
        # 数据库引擎
        engine = create_async_engine(url, echo=settings.DATABASE_ECHO, future=True, pool_pre_ping=True)
        # log.success('数据库连接成功')
    except Exception as e:
        log.error('❌ 数据库链接失败 {}', e)
        sys.exit()
    else:
        session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, session


async def get_db():
    """session 生成器"""
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


async_engine, async_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL)


# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]


async def create_table():
    """创建数据库表"""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid4())
