#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DictType
from backend.app.admin.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam


class CRUDDictType(CRUDPlus[DictType]):
    async def get(self, db: AsyncSession, pk: int) -> DictType | None:
        """
        获取字典类型

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, *, name: str = None, code: str = None, status: int = None) -> Select:
        """
        获取所有字典类型

        :param name:
        :param code:
        :param status:
        :return:
        """
        filters = {}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if code is not None:
            filters.update(code__like=f'%{code}%')
        if status is not None:
            filters.update(status=status)
        return await self.select_order('created_time', 'desc', **filters)

    async def get_by_code(self, db: AsyncSession, code: str) -> DictType | None:
        """
        通过 code 获取字典类型

        :param db:
        :param code:
        :return:
        """
        return await self.select_model_by_column(db, code=code)

    async def create(self, db: AsyncSession, obj_in: CreateDictTypeParam) -> None:
        """
        创建字典类型

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateDictTypeParam) -> int:
        """
        更新字典类型

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除字典类型

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


dict_type_dao: CRUDDictType = CRUDDictType(DictType)
