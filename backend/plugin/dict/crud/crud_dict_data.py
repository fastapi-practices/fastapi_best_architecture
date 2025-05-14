#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.dict.model import DictData
from backend.plugin.dict.schema.dict_data import CreateDictDataParam, UpdateDictDataParam


class CRUDDictData(CRUDPlus[DictData]):
    """Dictionary Data Database Operating Category"""

    async def get(self, db: AsyncSession, pk: int) -> DictData | None:
        """
        Get Dictionary Data Details

        :param db: database session
        :param pk: Dictionary data ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, label: str | None, value: str | None, status: int | None) -> Select:
        """
        Fetch Dictionary Data List

        :param label: dictionary data tag
        :param value: dictionary data keys
        :param status: dictionary status
        :return:
        """
        stmt = select(self.model).options(noload(self.model.type)).order_by(desc(self.model.sort))

        filters = []
        if label is not None:
            filters.append(self.model.label.like(f'%{label}%'))
        if value is not None:
            filters.append(self.model.value.like(f'%{value}%'))
        if status is not None:
            filters.append(self.model.status == status)

        if filters:
            stmt = stmt.where(and_(*filters))

        return stmt

    async def get_by_label(self, db: AsyncSession, label: str) -> DictData | None:
        """
        Get Dictionary Data Through Tabs

        :param db: database session
        :param label: dictionary label
        :return:
        """
        return await self.select_model_by_column(db, label=label)

    async def create(self, db: AsyncSession, obj: CreateDictDataParam) -> None:
        """
        Create Dictionary Data

        :param db: database session
        :param obj: create dictionary data parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictDataParam) -> int:
        """
        Update Dictionary Data

        :param db: database session
        :param pk: Dictionary data ID
        :param obj: update dictionary data parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Delete Dictionary Data

        :param db: database session
        :param pk: dictionary data ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DictData | None:
        """
        Get dictionary data and associated data

        :param db: database session
        :param pk: Dictionary data ID
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.type)).where(self.model.id == pk)
        dict_data = await db.execute(stmt)
        return dict_data.scalars().first()


dict_data_dao: CRUDDictData = CRUDDictData(DictData)
