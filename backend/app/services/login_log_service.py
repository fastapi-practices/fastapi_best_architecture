#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NoReturn

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_login_log import LoginLogDao
from backend.app.database.db_mysql import async_db_session
from backend.app.schemas.login_log import CreateLoginLog


class LoginLogService:
    @staticmethod
    async def get_select() -> Select:
        return await LoginLogDao.get_all()

    @staticmethod
    async def create(db: AsyncSession, obj_in: CreateLoginLog) -> NoReturn:
        await LoginLogDao.create(db, obj_in)

    @staticmethod
    async def delete(pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete(db, pk)
            return count

    @staticmethod
    async def delete_all() -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete_all(db)
            return count
