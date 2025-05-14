#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, UpdateDataRuleParam


class CRUDDataRule(CRUDPlus[DataRule]):
    """Data Rules Database Operating Category"""

    async def get(self, db: AsyncSession, pk: int) -> DataRule | None:
        """
        Access rule details

        :param db: database session
        :param pk: Rule ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, name: str | None) -> Select:
        """
        Get Rules List

        :param name: rule name
        :return:
        """
        stmt = select(self.model).options(noload(self.model.scope)).order_by(desc(self.model.created_time))

        filters = []
        if name is not None:
            filters.append(self.model.name.like(f'%{name}%'))

        if filters:
            stmt = stmt.where(and_(*filters))

        return stmt

    async def get_by_name(self, db: AsyncSession, name: str) -> DataRule | None:
        """
        Access rules by name

        :param db: database session
        :param name: rule name
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_all(self, db: AsyncSession) -> Sequence[DataRule]:
        """
        Get All Rules

        :param db: database session
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj: CreateDataRuleParam) -> None:
        """
        Create rules

        :param db: database session
        :param obj: create rule parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDataRuleParam) -> int:
        """
        Update rules

        :param db: database session
        :param pk: Rule ID
        :param obj: update rule parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Delete Rule

        :param db: database session
        :param pk: Rule ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


data_rule_dao: CRUDDataRule = CRUDDataRule(DataRule)
