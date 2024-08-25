#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Config
from backend.app.admin.schema.config import CreateConfigParam, UpdateConfigParam


class CRUDConfig(CRUDPlus[Config]):
    async def get_one(self, db: AsyncSession) -> Config | None:
        """
        获取 Config

        :param db:
        :return:
        """
        query = await db.execute(select(self.model).limit(1))
        return query.scalars().first()

    async def get_all(self, db: AsyncSession) -> Sequence[Config]:
        """
        获取所有 Config

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj_in: CreateConfigParam) -> None:
        """
        创建 Config

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateConfigParam) -> int:
        """
        更新 Config

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 Config

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


config_dao: CRUDConfig = CRUDConfig(Config)
