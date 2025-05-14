#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.core.conf import settings
from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import CreateConfigParam, UpdateConfigParam


class CRUDConfig(CRUDPlus[Config]):
    """System Parameter Configuration Database Operator Category"""

    async def get(self, db: AsyncSession, pk: int) -> Config | None:
        """
        Get Parameter Configuration Details

        :param db: database session
        :param pk: Parameter Configuration ID
        :return:
        """
        return await self.select_model_by_column(db, id=pk, type__not_in=settings.CONFIG_BUILT_IN_TYPES)

    async def get_by_type(self, db: AsyncSession, type: str) -> Sequence[Config]:
        """
        Get Parameter Configuration Through Type

        :param db: database session
        :param type: parameter configuration type
        :return:
        """
        return await self.select_models(db, type=type)

    async def get_by_key_and_type(self, db: AsyncSession, key: str, type: str) -> Config | None:
        """
        Get Parameter Configuration with Keyname and Type

        :param db: database session
        :param key: parameter configuration keyname
        :param type: parameter configuration type
        :return:
        """
        return await self.select_model_by_column(db, key=key, type=type)

    async def get_by_key(self, db: AsyncSession, key: str) -> Config | None:
        """
        Get Parameter Configuration Through Keyname

        :param db: database session
        :param key: parameter configuration keyname
        :return:
        """
        return await self.select_model_by_column(db, key=key)

    async def get_list(self, name: str | None, type: str | None) -> Select:
        """
        Get Parameter Configuration List

        :param name: parameter configuration name
        :param type: parameter configuration type
        :return:
        """
        filters = {'type__not_in': settings.CONFIG_BUILT_IN_TYPES}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if type is not None:
            filters.update(type__like=f'%{type}%')
        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateConfigParam) -> None:
        """
        Create Parameter Configuration

        :param db: database session
        :param obj: create parameter configuration parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateConfigParam) -> int:
        """
        Update Parameter Configuration

        :param db: database session
        :param pk: Parameter Configuration ID
        :param obj: update parameter configuration parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Remove Parameter Configuration

        :param db: database session
        :param pk: Parameter Configuration ID list
        :return:
        """
        return await self.delete_model_by_column(
            db, allow_multiple=True, id__in=pk, type__not_in=settings.CONFIG_BUILT_IN_TYPES
        )


config_dao: CRUDConfig = CRUDConfig(Config)
