#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.generator.model import GenModel
from backend.app.generator.schema.gen_model import CreateGenModelParam, UpdateGenModelParam


class CRUDGenModel(CRUDPlus[GenModel]):
    async def get(self, db: AsyncSession, pk: int) -> GenModel | None:
        """
        获取代码生成模型列

        :return:
        """
        return await self.select_model(db, pk)

    async def get_all_by_business_id(self, db: AsyncSession, business_id: int) -> Sequence[GenModel]:
        """
        获取所有代码生成模型列

        :param db:
        :param business_id:
        :return:
        """
        return await self.select_models_order(db, sort_columns='sort', gen_business_id=business_id)

    async def create(self, db: AsyncSession, obj_in: CreateGenModelParam, pd_type: str | None = None) -> None:
        """
        创建代码生成模型表

        :param db:
        :param obj_in:
        :param pd_type:
        :return:
        """
        await self.create_model(db, obj_in, pd_type=pd_type)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateGenModelParam, pd_type: str | None = None) -> int:
        """
        更细代码生成模型表

        :param db:
        :param pk:
        :param obj_in:
        :param pd_type:
        :return:
        """
        return await self.update_model(db, pk, obj_in, pd_type=pd_type)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除代码生成模型表

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model(db, pk)


gen_model_dao: CRUDGenModel = CRUDGenModel(GenModel)
