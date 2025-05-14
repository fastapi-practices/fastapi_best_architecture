#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam, UpdateGenBusinessParam


class CRUDGenBusiness(CRUDPlus[GenBusiness]):
    """CODE GENERATION OPERATIONS CRUD CATEGORY"""

    async def get(self, db: AsyncSession, pk: int) -> GenBusiness | None:
        """
        Get code generation business

        :param db: database session
        :param pk: Code Generation Business ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> GenBusiness | None:
        """
        generate business via name

        :param db: database session
        :param name: table name
        :return:
        """
        return await self.select_model_by_column(db, table_name=name)

    async def get_all(self, db: AsyncSession) -> Sequence[GenBusiness]:
        """
        Get all code generation operations

        :param db: database session
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj: CreateGenBusinessParam) -> None:
        """
        Create code generation business

        :param db: database session
        :param obj: create code generation business parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        Update code generation operations

        :param db: database session
        :param pk: Code Generation Business ID
        :param obj: update code generation business parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        Remove Code Generation Operations

        :param db: database session
        :param pk: Code Generation Business ID
        :return:
        """
        return await self.delete_model(db, pk)


gen_business_dao: CRUDGenBusiness = CRUDGenBusiness(GenBusiness)
