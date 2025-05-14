#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from typing import Annotated, AsyncGenerator
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from backend.common.log import log
from backend.common.model import MappedBase
from backend.core.conf import settings


def create_database_url(unittest: bool = False) -> URL:
    """
    Create Database Link

    :param unit: for unit testing
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


def create_async_engine_and_session(url: str | URL) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """
    Create database engines and Session

    :param uRL: Database Connection URL
    :return:
    """
    try:
        # Database engine
        engine = create_async_engine(
            url,
            echo=settings.DATABASE_ECHO,
            echo_pool=settings.DATABASE_POOL_ECHO,
            future=True,
            # Medium intermingled
            pool_size=10,  # Low: - High：+
            max_overflow=20,  # Low: - High：+
            pool_timeout=30,  # Low: + High：-
            pool_recycle=3600,  # Low: + High：-
            pool_pre_ping=True,  # Low: False High：True
            pool_use_lifo=False,  # Low: False High：True
        )
    except Exception as e:
        log.error('Database Link Failed', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,  # Disable Auto Refresh
            expire_on_commit=False,  # Expire when submitting disabled
        )
        return engine, db_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session"""
    async with async_db_session() as session:
        yield session


async def create_table() -> None:
    """Create database table"""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    """DATABASE ENGINE UUD TYPE COMPATIBILITY SOLUTION"""
    return str(uuid4())


SQLALCHEMY_DATABASE_URL = create_database_url()
async_engine, async_db_session = create_async_engine_and_session(SQLALCHEMY_DATABASE_URL)
# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]
