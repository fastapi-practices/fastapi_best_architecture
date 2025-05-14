#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.dict.model import DictType
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam


class CRUDDictType(CRUDPlus[DictType]):
    """Dictionary Type Database Operator Category"""

    async def get(self, db: AsyncSession, pk: int) -> DictType | None:
        """
        Get dictionary type details

        :param db: database session
        :param pk: dictionary type ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self, *, name: str | None, code: str | None, status: int | None) -> Select:
        """
        Fetch list of dictionary types

        :param name: dictionary type name
        :param code: dictionary type encoding
        :param status: dictionary status
        :return:
        """
        stmt = select(self.model).options(noload(self.model.datas)).order_by(desc(self.model.created_time))

        filters = []
        if name is not None:
            filters.append(self.model.name.like(f'%{name}%'))
        if code is not None:
            filters.append(self.model.code.like(f'%{code}%'))
        if status is not None:
            filters.append(self.model.status == status)

        if filters:
            stmt = stmt.where(and_(*filters))

        return stmt

    async def get_by_code(self, db: AsyncSession, code: str) -> DictType | None:
        """
        Get Dictionary Type By Encoding

        :param db: database session
        :param code: dictionary encoding
        :return:
        """
        return await self.select_model_by_column(db, code=code)

    async def create(self, db: AsyncSession, obj: CreateDictTypeParam) -> None:
        """
        Create dictionary type

        :param db: database session
        :param obj: create dictionary type parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictTypeParam) -> int:
        """
        Update dictionary type

        :param db: database session
        :param pk: dictionary type ID
        :param obj: update dictionary type parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Remove Dictionary Type

        :param db: database session
        :param pk: dictionary type ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


dict_type_dao: CRUDDictType = CRUDDictType(DictType)
