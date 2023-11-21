#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.crud.base import CRUDBase
from backend.app.models.sys_dict_data import DictData
from backend.app.schemas.dict_data import CreateDictData, UpdateDictData


class CRUDDictData(CRUDBase[DictData, CreateDictData, UpdateDictData]):
    async def get(self, db: AsyncSession, pk: int) -> DictData | None:
        return await self.get_(db, pk=pk)

    async def get_all(self, label: str = None, value: str = None, status: int = None) -> Select:
        se = select(self.model).options(selectinload(self.model.type)).order_by(desc(self.model.sort))
        where_list = []
        if label:
            where_list.append(self.model.label.like(f'%{label}%'))
        if value:
            where_list.append(self.model.value.like(f'%{value}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_by_label(self, db: AsyncSession, label: str) -> DictData | None:
        api = await db.execute(select(self.model).where(self.model.label == label))
        return api.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateDictData) -> None:
        await self.create_(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateDictData) -> int:
        return await self.update_(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        apis = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return apis.rowcount

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DictData | None:
        where = [self.model.id == pk]
        dict_data = await db.execute(select(self.model).options(selectinload(self.model.type)).where(*where))
        return dict_data.scalars().first()


DictDataDao: CRUDDictData = CRUDDictData(DictData)
