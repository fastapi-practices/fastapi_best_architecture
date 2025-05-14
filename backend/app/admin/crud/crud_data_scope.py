#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule, DataScope
from backend.app.admin.schema.data_scope import CreateDataScopeParam, UpdateDataScopeParam, UpdateDataScopeRuleParam


class CRUDDataScope(CRUDPlus[DataScope]):
    """Data Range Database Operating Category"""

    async def get(self, db: AsyncSession, pk: int) -> DataScope | None:
        """
        Details on the extent of data acquisition

        :param db: database session
        :param pk: Range ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> DataScope | None:
        """
        Acquiring data ranges by name

        :param db: database session
        :param name: range name
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DataScope:
        """
        Access to data range correlation data

        :param db: database session
        :param pk: Range ID
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.rules)).where(self.model.id == pk)
        data_scope = await db.execute(stmt)
        return data_scope.scalars().first()

    async def get_list(self, name: str | None, status: int | None) -> Select:
        """
        List of data ranges obtained

        :param name: range name
        :param status: range status
        :return:
        """
        stmt = (
            select(self.model)
            .options(noload(self.model.rules), noload(self.model.roles))
            .order_by(desc(self.model.created_time))
        )

        filters = []
        if name is not None:
            filters.append(self.model.name.like(f'%{name}%'))
        if status is not None:
            filters.append(self.model.status == status)

        if filters:
            stmt = stmt.where(and_(*filters))

        return stmt

    async def create(self, db: AsyncSession, obj: CreateDataScopeParam) -> None:
        """
        Create Data Range

        :param db: database session
        :param obj: create data range parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDataScopeParam) -> int:
        """
        Update data ranges

        :param db: database session
        :param pk: Range ID
        :param obj: update data range parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def update_rules(self, db: AsyncSession, pk: int, rule_ids: UpdateDataScopeRuleParam) -> int:
        """
        Update data coverage rules

        :param db: database session
        :param pk: Range ID
        :param rule ID list
        :return:
        """
        current_data_scope = await self.get_with_relation(db, pk)
        stmt = select(DataRule).where(DataRule.id.in_(rule_ids.rules))
        rules = await db.execute(stmt)
        current_data_scope.rules = rules.scalars().all()
        return len(current_data_scope.rules)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Delete Data Range

        :param db: database session
        :param pk: Range ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


data_scope_dao: CRUDDataScope = CRUDDataScope(DataScope)
