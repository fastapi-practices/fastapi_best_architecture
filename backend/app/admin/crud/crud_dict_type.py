#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import DictType
from backend.app.admin.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam
from backend.common.msd.crud import CRUDBase


class CRUDDictType(CRUDBase[DictType, CreateDictTypeParam, UpdateDictTypeParam]):
    async def get(self, db: AsyncSession, pk: int) -> DictType | None:
        """
        获取字典类型

        :param db:
        :param pk:
        :return:
        """
        return await self.get_(db, pk=pk)

    async def get_list(self, *, name: str = None, code: str = None, status: int = None) -> Select:
        """
        获取所有字典类型

        :param name:
        :param code:
        :param status:
        :return:
        """
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if code:
            where_list.append(self.model.code.like(f'%{code}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(*where_list)
        return se

    async def get_by_code(self, db: AsyncSession, code: str) -> DictType | None:
        """
        通过 code 获取字典类型

        :param db:
        :param code:
        :return:
        """
        dept = await db.execute(select(self.model).where(self.model.code == code))
        return dept.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateDictTypeParam) -> None:
        """
        创建字典类型

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateDictTypeParam) -> int:
        """
        更新字典类型

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除字典类型

        :param db:
        :param pk:
        :return:
        """
        apis = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return apis.rowcount


dict_type_dao: CRUDDictType = CRUDDictType(DictType)
