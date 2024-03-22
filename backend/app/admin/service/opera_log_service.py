#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.admin.crud.crud_opera_log import opera_log_dao
from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.database.db_mysql import async_db_session


class OperaLogService:
    @staticmethod
    async def get_select(*, username: str | None = None, status: int | None = None, ip: str | None = None) -> Select:
        return await opera_log_dao.get_list(username=username, status=status, ip=ip)

    @staticmethod
    async def create(*, obj_in: CreateOperaLogParam):
        async with async_db_session.begin() as db:
            await opera_log_dao.create(db, obj_in)

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete(db, pk)
            return count

    @staticmethod
    async def delete_all() -> int:
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete_all(db)
            return count


opera_log_service = OperaLogService()
