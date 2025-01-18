#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, UpdateDataRuleParam


class CRUDDataRule(CRUDPlus[DataRule]):
    async def get(self, db: AsyncSession, pk: int) -> DataRule | None:
        """
        获取数据权限规则

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, name: str = None) -> Select:
        """
        获取数据权限规则列表

        :return:
        """
        stmt = select(self.model).options(noload(self.model.roles)).order_by(desc(self.model.created_time))
        where_list = []
        if name is not None:
            where_list.append(self.model.name.like(f'%{name}%'))
        if where_list:
            stmt = stmt.where(*where_list)
        return stmt

    async def get_by_name(self, db: AsyncSession, name: str):
        """
        通过 name 获取数据权限规则

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_all(self, db: AsyncSession) -> Sequence[DataRule]:
        """
        获取所有数据权限规则

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj_in: CreateDataRuleParam) -> None:
        """
        创建数据权限规则

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateDataRuleParam) -> int:
        """
        更新数据权限规则

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除数据权限规则

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


data_rule_dao: CRUDDataRule = CRUDDataRule(DataRule)
