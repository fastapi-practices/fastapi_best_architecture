#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from typing import TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing_extensions import Annotated

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.database.base_class import MappedBase

""" 
说明：SqlAlchemy
"""

SQLALCHEMY_DATABASE_URL = f'mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:' \
                          f'{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'

try:
    # 数据库引擎
    async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DB_ECHO, future=True)
    # log.success('数据库连接成功')
except Exception as e:
    log.error('❌ 数据库链接失败 {}', e)
    sys.exit()
else:
    async_session_maker = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False)


async def _get_db() -> AsyncSession:
    """
    session 生成器

    :return:
    """
    session = async_session_maker()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


# Session 依赖注入
CurrentSession = Annotated[AsyncSession, Depends(_get_db)]

# Session 装饰器 db 参数类型
AsyncSessionNotInput = TypeVar('AsyncSessionNotInput', bound=AsyncSession)


def async_session(func):
    """
    session 装饰器

    :param func:
    :return:
    """

    async def wrapper(*args, **kwargs):
        async with async_session_maker() as db:
            return await func(db, *args, **kwargs)

    return wrapper


def async_session_transaction(func):
    """
    session 事务装饰器

    :param func:
    :return:
    """

    async def wrapper(*args, **kwargs):
        async with async_session_maker.begin() as db:
            return await func(db, *args, **kwargs)

    return wrapper


async def create_table():
    """
    创建数据库表
    """
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)
