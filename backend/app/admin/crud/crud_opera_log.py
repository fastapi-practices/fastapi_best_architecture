#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import OperaLog
from backend.app.admin.schema.opera_log import CreateOperaLogParam


class CRUDOperaLogDao(CRUDPlus[OperaLog]):
    """操作日志数据库操作类"""

    async def get_list(self, username: str | None, status: int | None, ip: str | None) -> Select:
        """
        获取操作日志列表

        :param username: 用户名
        :param status: 操作状态
        :param ip: IP 地址
        :return:
        """
        filters = {}

        if username is not None:
            filters['username__like'] = f'%{username}%'
        if status is not None:
            filters['status__eq'] = status
        if ip is not None:
            filters['ip__like'] = f'%{ip}%'

        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateOperaLogParam) -> None:
        """
        创建操作日志

        :param db: 数据库会话
        :param obj: 创建操作日志参数
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除操作日志

        :param db: 数据库会话
        :param pks: 操作日志 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    @staticmethod
    async def delete_all(db: AsyncSession) -> None:
        """
        删除所有日志

        :param db: 数据库会话
        :return:
        """
        await db.execute(sa_delete(OperaLog))


opera_log_dao: CRUDOperaLogDao = CRUDOperaLogDao(OperaLog)
