import sys

from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.common.log import log
from backend.common.model import MappedBase
from backend.core.conf import settings


def create_database_url(unittest: bool = False) -> URL:
    """
    创建数据库链接

    :param unittest: 是否用于单元测试
    :return:
    """
    url = URL.create(
        drivername='mysql+asyncmy' if settings.DATABASE_TYPE == 'mysql' else 'postgresql+asyncpg',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_SCHEMA if not unittest else f'{settings.DATABASE_SCHEMA}_test',
    )
    if settings.DATABASE_TYPE == 'mysql':
        url.update_query_dict({'charset': settings.DATABASE_CHARSET})
    return url


def create_engine_and_session(url: str | URL):
    """创建数据库引擎和 Session"""
    try:
        # 数据库引擎
        engine = create_async_engine(url, echo=settings.DATABASE_ECHO, future=True, pool_pre_ping=True)
        # log.success('数据库连接成功')
    except Exception as e:
        log.error('❌ 数据库链接失败 {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session


async def get_db():
    """session 生成器"""
    async with async_db_session() as session:
        yield session


async def create_table():
    """创建数据库表"""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid4())


SQLALCHEMY_DATABASE_URL = create_database_url()
async_engine, async_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL)
# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]
