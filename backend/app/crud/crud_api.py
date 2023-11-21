#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.base import CRUDBase
from backend.app.models import Api
from backend.app.schemas.api import CreateApi, UpdateApi


class CRUDApi(CRUDBase[Api, CreateApi, UpdateApi]):
    async def get(self, db: AsyncSession, pk: int) -> Api | None:
        return await self.get_(db, pk=pk)

    async def get_list(self, name: str = None, method: str = None, path: str = None) -> Select:
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
        apis = await db.execute(select(self.model))
        return apis.scalars().all()

    async def get_by_name(self, db: AsyncSession, name: str) -> Api | None:
        api = await db.execute(select(self.model).where(self.model.name == name))
        return api.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateApi) -> None:
        await self.create_(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateApi) -> int:
        return await self.update_(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        apis = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return apis.rowcount


ApiDao: CRUDApi = CRUDApi(Api)
