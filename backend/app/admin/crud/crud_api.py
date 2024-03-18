#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import Api
from backend.app.admin.schema.api import CreateApiParam, UpdateApiParam
from backend.common.msd.crud import CRUDBase


class CRUDApi(CRUDBase[Api, CreateApiParam, UpdateApiParam]):
    async def get(self, db: AsyncSession, pk: int) -> Api | None:
        """
        获取 API

        :param db:
        :param pk:
        :return:
        """
        return await self.get_(db, pk=pk)

    async def get_list(self, name: str = None, method: str = None, path: str = None) -> Select:
        """
        获取 API 列表

        :param name:
        :param method:
        :param path:
        :return:
        """
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if method:
            where_list.append(self.model.method == method)
        if path:
            where_list.append(self.model.path.like(f'%{path}%', escape='/'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_all(self, db: AsyncSession) -> Sequence[Api]:
        """
        获取所有 API

        :param db:
        :return:
        """
        apis = await db.execute(select(self.model))
        return apis.scalars().all()

    async def get_by_name(self, db: AsyncSession, name: str) -> Api | None:
        """
        通过 name 获取 API

        :param db:
        :param name:
        :return:
        """
        api = await db.execute(select(self.model).where(self.model.name == name))
        return api.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateApiParam) -> None:
        """
        创建 API

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateApiParam) -> int:
        """
        更新 API

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 API

        :param db:
        :param pk:
        :return:
        """
        apis = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return apis.rowcount


api_dao: CRUDApi = CRUDApi(Api)
