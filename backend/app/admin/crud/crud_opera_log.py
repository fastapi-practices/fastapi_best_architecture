#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import OperaLog
from backend.app.admin.schema.opera_log import CreateOperaLogParam


class CRUDOperaLogDao(CRUDPlus[OperaLog]):
    """Operation log database operating class"""

    async def get_list(self, username: str | None, status: int | None, ip: str | None) -> Select:
        """
        Get Operations Log List

        :param username:
        :param status: operational status
        :param ip: IP address
        :return:
        """
        filters = {}
        if username is not None:
            filters.update(username__like=f'%{username}%')
        if status is not None:
            filters.update(status=status)
        if ip is not None:
            filters.update(ip__like=f'%{ip}%')
        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateOperaLogParam) -> None:
        """
        Create Operations Log

        :param db: database session
        :param obj: create operational log parameters
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Remove Operation Log

        :param db: database session
        :param pk: Operations log ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)

    async def delete_all(self, db: AsyncSession) -> int:
        """
        Delete All Logs

        :param db: database session
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True)


opera_log_dao: CRUDOperaLogDao = CRUDOperaLogDao(OperaLog)
