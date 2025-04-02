#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
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
        return await self.select_model(db, pk)

    async def get_list(self, label: str | None = None, value: str | None = None, status: int | None = None) -> Select:
        """
        获取字典数据列表

        :param label: 字典数据标签
        :param value: 字典数据键值
        :param status: 字典状态
        :return:
        """
        stmt = select(self.model).options(noload(self.model.type)).order_by(desc(self.model.sort))

        filters = []
        if label is not None:
            filters.append(self.model.label.like(f'%{label}%'))
        if value is not None:
            filters.append(self.model.value.like(f'%{value}%'))
        if status is not None:
            filters.append(self.model.status == status)

        if filters:
            stmt = stmt.where(and_(*filters))

        return stmt

    async def get_by_label(self, db: AsyncSession, label: str) -> DictData | None:
        """
        通过标签获取字典数据

        :param db: 数据库会话
        :param label: 字典标签
        :return:
        """
        return await self.select_model_by_column(db, label=label)

    async def create(self, db: AsyncSession, obj: CreateDictDataParam) -> None:
        """
        创建字典数据

        :param db: 数据库会话
        :param obj: 创建字典数据参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictDataParam) -> int:
        """
        更新字典数据

        :param db: 数据库会话
        :param pk: 字典数据 ID
        :param obj: 更新字典数据参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除字典数据

        :param db: 数据库会话
        :param pk: 字典数据 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DictData | None:
        """
        获取字典数据及关联数据

        :param db: 数据库会话
        :param pk: 字典数据 ID
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.type)).where(self.model.id == pk)
        dict_data = await db.execute(stmt)
        return dict_data.scalars().first()


dict_data_dao: CRUDDictData = CRUDDictData(DictData)
