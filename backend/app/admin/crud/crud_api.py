#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Api
from backend.app.admin.schema.api import CreateApiParam, UpdateApiParam


class CRUDApi(CRUDPlus[Api]):
    async def get(self, db: AsyncSession, pk: int) -> Api | None:
        """
        获取 API

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, name: str = None, method: str = None, path: str = None) -> Select:
        """
        获取 API 列表

        :param name:
        :param method:
        :param path:
        :return:
        """
        filters = {}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if method is not None:
            filters.update(method=method)
        if path is not None:
            filters.update(path__like=f'%{path}%')
        return await self.select_order('created_time', 'desc', **filters)

    async def get_all(self, db: AsyncSession) -> Sequence[Api]:
        """
        获取所有 API

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def get_by_name(self, db: AsyncSession, name: str) -> Api | None:
        """
        通过 name 获取 API

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def create(self, db: AsyncSession, obj_in: CreateApiParam) -> None:
        """
        创建 API

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateApiParam) -> int:
        """
        更新 API

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 API

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


api_dao: CRUDApi = CRUDApi(Api)
