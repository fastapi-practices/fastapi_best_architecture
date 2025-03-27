#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.admin.crud.crud_opera_log import opera_log_dao
from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.database.db import async_db_session


class OperaLogService:
    """操作日志服务类"""

    @staticmethod
    async def get_select(*, username: str | None = None, status: int | None = None, ip: str | None = None) -> Select:
        """
        获取操作日志列表查询条件

        :param username: 用户名
        :param status: 状态
        :param ip: IP 地址
        :return:
        """
        return await opera_log_dao.get_list(username=username, status=status, ip=ip)

    @staticmethod
    async def create(*, obj: CreateOperaLogParam) -> None:
        """
        创建操作日志

        :param obj: 操作日志创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            await opera_log_dao.create(db, obj)

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        删除操作日志

        :param pk: 日志 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete(db, pk)
            return count

    @staticmethod
    async def delete_all() -> int:
        """清空所有操作日志"""
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete_all(db)
            return count


opera_log_service: OperaLogService = OperaLogService()
