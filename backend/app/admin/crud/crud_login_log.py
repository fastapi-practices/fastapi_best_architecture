#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import LoginLog
from backend.app.admin.schema.login_log import CreateLoginLogParam


class CRUDLoginLog(CRUDPlus[LoginLog]):
    async def get_list(self, username: str | None = None, status: int | None = None, ip: str | None = None) -> Select:
        """
        获取登录日志列表

        :param username:
        :param status:
        :param ip:
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

    async def create(self, db: AsyncSession, obj_in: CreateLoginLogParam) -> None:
        """
        创建登录日志

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in, commit=True)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除登录日志

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)

    async def delete_all(self, db: AsyncSession) -> int:
        """
        删除所有登录日志

        :param db:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True)


login_log_dao: CRUDLoginLog = CRUDLoginLog(LoginLog)
