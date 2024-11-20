#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, UpdateDataRuleParam


class CRUDDataRule(CRUDPlus[DataRule]):
    async def get(self, db: AsyncSession, pk: int) -> DataRule | None:
        """
        获取 DataRule

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self) -> Select:
        """
        获取 DataRule 列表

        :return:
        """
        return await self.select_order('created_time', 'desc')

    async def get_all(self, db: AsyncSession) -> Sequence[DataRule]:
        """
        获取所有 DataRule

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj_in: CreateDataRuleParam) -> None:
        """
        创建 DataRule

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateDataRuleParam) -> int:
        """
        更新 DataRule

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 DataRule

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


data_rule_dao: CRUDDataRule = CRUDDataRule(DataRule)
