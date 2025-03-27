#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.generator.model import GenModel
from backend.app.generator.schema.gen_model import CreateGenModelParam, UpdateGenModelParam


class CRUDGenModel(CRUDPlus[GenModel]):
    """代码生成模型 CRUD 类"""

    async def get(self, db: AsyncSession, pk: int) -> GenModel | None:
        """
        获取代码生成模型列

        :param db: 数据库会话
        :param pk: 代码生成模型 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_all_by_business(self, db: AsyncSession, business_id: int) -> Sequence[GenModel]:
        """
        获取所有代码生成模型列

        :param db: 数据库会话
        :param business_id: 业务 ID
        :return:
        """
        return await self.select_models_order(db, sort_columns='sort', gen_business_id=business_id)

    async def create(self, db: AsyncSession, obj: CreateGenModelParam, pd_type: str | None = None) -> None:
        """
        创建代码生成模型

        :param db: 数据库会话
        :param obj: 创建代码生成模型参数
        :param pd_type: Pydantic 类型
        :return:
        """
        await self.create_model(db, obj, pd_type=pd_type)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateGenModelParam, pd_type: str | None = None) -> int:
        """
        更新代码生成模型

        :param db: 数据库会话
        :param pk: 代码生成模型 ID
        :param obj: 更新代码生成模型参数
        :param pd_type: Pydantic 类型
        :return:
        """
        return await self.update_model(db, pk, obj, pd_type=pd_type)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除代码生成模型

        :param db: 数据库会话
        :param pk: 代码生成模型 ID
        :return:
        """
        return await self.delete_model(db, pk)


gen_model_dao: CRUDGenModel = CRUDGenModel(GenModel)
