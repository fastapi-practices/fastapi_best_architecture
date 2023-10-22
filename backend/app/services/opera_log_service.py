#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.crud.crud_opera_log import OperaLogDao
from backend.app.database.db_mysql import async_db_session
from backend.app.schemas.opera_log import CreateOperaLog


class OperaLogService:
    @staticmethod
    async def get_select(*, username: str | None = None, status: int | None = None, ip: str | None = None) -> Select:
        return await OperaLogDao.get_all(username=username, status=status, ip=ip)

    @staticmethod
    async def create(*, obj_in: CreateOperaLog):
        async with async_db_session.begin() as db:
            await OperaLogDao.create(db, obj_in)

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await OperaLogDao.delete(db, pk)
            return count

    @staticmethod
    async def delete_all() -> int:
        async with async_db_session.begin() as db:
            count = await OperaLogDao.delete_all(db)
            return count
