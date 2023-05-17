#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing_extensions import Annotated

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.database.base_class import MappedBase

""" 
说明：SqlAlchemy
"""

SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
    f'{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'
)

try:
    # 数据库引擎
    async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DB_ECHO, future=True, pool_pre_ping=True)
    # log.success('数据库连接成功')
except Exception as e:
    log.error('❌ 数据库链接失败 {}', e)
    sys.exit()
else:
    async_db_session = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """
    session 生成器

    :return:
    """
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]


async def create_table():
    """
    创建数据库表
    """
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)
