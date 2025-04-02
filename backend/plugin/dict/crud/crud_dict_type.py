#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.dict.model import DictType
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam


class CRUDDictType(CRUDPlus[DictType]):
    """字典类型数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> DictType | None:
        """
        获取字典类型详情

        :param db: 数据库会话
        :param pk: 字典类型 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, *, name: str | None = None, code: str | None = None, status: int | None = None) -> Select:
        """
        获取字典类型列表

        :param name: 字典类型名称
        :param code: 字典类型编码
        :param status: 字典状态
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
        通过编码获取字典类型

        :param db: 数据库会话
        :param code: 字典编码
        :return:
        """
        return await self.select_model_by_column(db, code=code)

    async def create(self, db: AsyncSession, obj: CreateDictTypeParam) -> None:
        """
        创建字典类型

        :param db: 数据库会话
        :param obj: 创建字典类型参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictTypeParam) -> int:
        """
        更新字典类型

        :param db: 数据库会话
        :param pk: 字典类型 ID
        :param obj: 更新字典类型参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除字典类型

        :param db: 数据库会话
        :param pk: 字典类型 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


dict_type_dao: CRUDDictType = CRUDDictType(DictType)
