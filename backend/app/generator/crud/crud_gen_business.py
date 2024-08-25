#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.generator.model import GenBusiness
from backend.app.generator.schema.gen_business import CreateGenBusinessParam, UpdateGenBusinessParam


class CRUDGenBusiness(CRUDPlus[GenBusiness]):
    async def get(self, db: AsyncSession, pk: int) -> GenBusiness | None:
        """
        获取代码生成业务表

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> GenBusiness | None:
        """
        通过 name 获取代码生成业务表

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, table_name_en=name)

    async def get_all(self, db: AsyncSession) -> Sequence[GenBusiness]:
        """
        获取所有代码生成业务表

        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj_in: CreateGenBusinessParam) -> None:
        """
        创建代码生成业务表

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateGenBusinessParam) -> int:
        """
        更新代码生成业务表

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除代码生成业务表

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model(db, pk)


gen_business_dao: CRUDGenBusiness = CRUDGenBusiness(GenBusiness)
