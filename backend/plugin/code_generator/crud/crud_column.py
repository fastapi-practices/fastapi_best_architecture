#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.code_generator.model import GenColumn
from backend.plugin.code_generator.schema.column import CreateGenModelParam, UpdateGenModelParam


class CRUDGenModel(CRUDPlus[GenColumn]):
    """CODE GENERATION MODEL CRUD CLASS"""

    async def get(self, db: AsyncSession, pk: int) -> GenColumn | None:
        """
        Get Code Generation Model Bar

        :param db: database session
        :param pk: Code Generation Model ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_all_by_business(self, db: AsyncSession, business_id: int) -> Sequence[GenColumn]:
        """
        Fetch all code generation model columns

        :param db: database session
        :param business_id: Business ID
        :return:
        """
        return await self.select_models_order(db, sort_columns='sort', gen_business_id=business_id)

    async def create(self, db: AsyncSession, obj: CreateGenModelParam, pd_type: str | None) -> None:
        """
        Create code generation model

        :param db: database session
        :param obj: create code generation model parameters
        :param pd_type: Pydantic type
        :return:
        """
        await self.create_model(db, obj, pd_type=pd_type)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateGenModelParam, pd_type: str | None) -> int:
        """
        Update code generation model

        :param db: database session
        :param pk: Code Generation Model ID
        :param obj: update code generation model parameters
        :param pd_type: Pydantic type
        :return:
        """
        return await self.update_model(db, pk, obj, pd_type=pd_type)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        Remove Code Generation Model

        :param db: database session
        :param pk: Code Generation Model ID
        :return:
        """
        return await self.delete_model(db, pk)


gen_model_dao: CRUDGenModel = CRUDGenModel(GenColumn)
