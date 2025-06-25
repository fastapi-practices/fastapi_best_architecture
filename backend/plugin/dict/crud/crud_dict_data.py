#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.dict.model import DictData
from backend.plugin.dict.schema.dict_data import CreateDictDataParam, UpdateDictDataParam


class CRUDDictData(CRUDPlus[DictData]):
    """字典数据数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> DictData | None:
        """
        获取字典数据详情

        :param db: 数据库会话
        :param pk: 字典数据 ID
        :return:
        """
        return await self.select_model(db, pk, load_strategies={'type': 'noload'})

    async def get_all(self, db: AsyncSession) -> Sequence[DictData]:
        """
        获取所有字典数据

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db, load_strategies={'type': 'noload'})

    async def get_list(
        self, type_code: str | None, label: str | None, value: str | None, status: int | None, type_id: int | None
    ) -> Select:
        """
        获取字典数据列表

        :param type_code: 字典类型编码
        :param label: 字典数据标签
        :param value: 字典数据键值
        :param status: 字典状态
        :param type_id: 字典类型 ID
        :return:
        """
        filters = {}

        if type_code is not None:
            filters['type_code'] = type_code
        if label is not None:
            filters['label__like'] = f'%{label}%'
        if value is not None:
            filters['value__like'] = f'%{value}%'
        if status is not None:
            filters['status'] = status
        if type_id is not None:
            filters['type_id'] = type_id

        return await self.select_order('id', 'desc', load_strategies={'type': 'noload'}, **filters)

    async def get_by_label(self, db: AsyncSession, label: str) -> DictData | None:
        """
        通过标签获取字典数据

        :param db: 数据库会话
        :param label: 字典标签
        :return:
        """
        return await self.select_model_by_column(db, label=label)

    async def create(self, db: AsyncSession, obj: CreateDictDataParam, type_code: str) -> None:
        """
        创建字典数据

        :param db: 数据库会话
        :param obj: 创建字典数据参数
        :param type_code: 字典类型编码
        :return:
        """
        dict_obj = obj.model_dump()
        dict_obj.update({'type_code': type_code})
        new_data = self.model(**dict_obj)
        db.add(new_data)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictDataParam, type_code: str) -> int:
        """
        更新字典数据

        :param db: 数据库会话
        :param pk: 字典数据 ID
        :param obj: 更新字典数据参数
        :param type_code: 字典类型编码
        :return:
        """
        dict_obj = obj.model_dump()
        dict_obj.update({'type_code': type_code})
        return await self.update_model(db, pk, dict_obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除字典数据

        :param db: 数据库会话
        :param pks: 字典数据 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DictData | None:
        """
        获取字典数据及关联数据

        :param db: 数据库会话
        :param pk: 字典数据 ID
        :return:
        """
        return await self.select_model(db, pk, load_strategies=['type'])


dict_data_dao: CRUDDictData = CRUDDictData(DictData)
