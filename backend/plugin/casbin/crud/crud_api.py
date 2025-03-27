#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from fastapi import Request
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.common.security.permission import filter_data_permission
from backend.plugin.casbin.model import Api
from backend.plugin.casbin.schema.api import CreateApiParam, UpdateApiParam


class CRUDApi(CRUDPlus[Api]):
    """API 数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> Api | None:
        """
        获取 API

        :param db: 数据库会话
        :param pk: API ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, request: Request, name: str = None, method: str = None, path: str = None) -> Select:
        """
        获取 API 列表

        :param request: FastAPI 请求对象
        :param name: API 名称
        :param method: 请求方法
        :param path: API 路径
        :return:
        """
        filters = {}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if method is not None:
            filters.update(method=method)
        if path is not None:
            filters.update(path__like=f'%{path}%')
        stmt = await self.select_order('created_time', 'desc', **filters)
        return stmt.where(filter_data_permission(request))

    async def get_all(self, db: AsyncSession) -> Sequence[Api]:
        """
        获取所有 API

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db)

    async def get_by_name(self, db: AsyncSession, name: str) -> Api | None:
        """
        通过名称获取 API

        :param db: 数据库会话
        :param name: API 名称
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def create(self, db: AsyncSession, obj: CreateApiParam) -> None:
        """
        创建 API

        :param db: 数据库会话
        :param obj: 创建 API 参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateApiParam) -> int:
        """
        更新 API

        :param db: 数据库会话
        :param pk: API ID
        :param obj: 更新 API 参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 API

        :param db: 数据库会话
        :param pk: API ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


api_dao: CRUDApi = CRUDApi(Api)
