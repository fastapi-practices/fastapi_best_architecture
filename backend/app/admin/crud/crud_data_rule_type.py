#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRuleType
from backend.app.admin.schema.data_rule_type import CreateDataRuleTypeParam, UpdateDataRuleTypeParam


class CRUDDataRuleType(CRUDPlus[DataRuleType]):
    async def get(self, db: AsyncSession, pk: int) -> DataRuleType | None:
        """
        获取数据权限规则类型

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self) -> Select:
        """
        获取数据权限规则类型列表

        :return:
        """
        return await self.select_order('created_time', 'desc')

    async def get_by_name(self, db: AsyncSession, name: str) -> DataRuleType | None:
        """
        通过 name 获取数据权限规则类型

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_all(self, db: AsyncSession) -> Sequence[DataRuleType]:
        """
        获取所有数据权限规则类型

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj_in: CreateDataRuleTypeParam) -> None:
        """
        创建数据权限规则类型

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateDataRuleTypeParam) -> int:
        """
        更新数据权限规则类型

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除数据权限规则类型

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


data_rule_type_dao: CRUDDataRuleType = CRUDDataRuleType(DataRuleType)
