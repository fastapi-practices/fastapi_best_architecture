#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam, UpdateGenBusinessParam


class CRUDGenBusiness(CRUDPlus[GenBusiness]):
    """代码生成业务 CRUD 类"""

    async def get(self, db: AsyncSession, pk: int) -> GenBusiness | None:
        """
        获取代码生成业务

        :param db: 数据库会话
        :param pk: 代码生成业务 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> GenBusiness | None:
        """
        通过 name 获取代码生成业务

        :param db: 数据库会话
        :param name: 表名
        :return:
        """
        return await self.select_model_by_column(db, table_name=name)

    async def get_all(self, db: AsyncSession) -> Sequence[GenBusiness]:
        """
        获取所有代码生成业务

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db)

    async def get_list(self, table_name: str | None) -> Select:
        """
        获取所有代码生成业务

        :param table_name: 业务表名
        :return:
        """
        filters = {}

        if table_name is not None:
            filters['table_name__like'] = f'%{table_name}%'

        return await self.select_order('id', 'desc', load_strategies={'gen_column': 'noload'}, **filters)

    async def create(self, db: AsyncSession, obj: CreateGenBusinessParam) -> None:
        """
        创建代码生成业务

        :param db: 数据库会话
        :param obj: 创建代码生成业务参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        更新代码生成业务

        :param db: 数据库会话
        :param pk: 代码生成业务 ID
        :param obj: 更新代码生成业务参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除代码生成业务

        :param db: 数据库会话
        :param pk: 代码生成业务 ID
        :return:
        """
        return await self.delete_model(db, pk)


gen_business_dao: CRUDGenBusiness = CRUDGenBusiness(GenBusiness)
