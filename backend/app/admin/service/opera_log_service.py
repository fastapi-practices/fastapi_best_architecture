#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.admin.crud.crud_opera_log import opera_log_dao
from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.database.db import async_db_session


class OperaLogService:
    """Operation log service class"""

    @staticmethod
    async def get_select(*, username: str | None, status: int | None, ip: str | None) -> Select:
        """
        Fetch operational log list query conditions

        :param username:
        :param status: status
        :param ip: IP address
        :return:
        """
        return await opera_log_dao.get_list(username=username, status=status, ip=ip)

    @staticmethod
    async def create(*, obj: CreateOperaLogParam) -> None:
        """
        Create Operations Log

        :param obj: operational log creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            await opera_log_dao.create(db, obj)

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        Remove Operation Log

        :param pk: Log ID list
        :return:
        """
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete(db, pk)
            return count

    @staticmethod
    async def delete_all() -> int:
        """Empty all operations logs"""
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete_all(db)
            return count


opera_log_service: OperaLogService = OperaLogService()
