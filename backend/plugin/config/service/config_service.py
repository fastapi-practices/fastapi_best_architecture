#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.config.conf import config_settings
from backend.plugin.config.crud.crud_config import config_dao
from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    SaveBuiltInConfigParam,
    UpdateConfigParam,
)


class ConfigService:
    """Parameter Configuration Service Class"""

    @staticmethod
    async def get_built_in_config(type: str) -> Sequence[Config]:
        """
        Get Internal Parameter Configuration

        :param type: parameter configuration type
        :return:
        """
        async with async_db_session() as db:
            return await config_dao.get_by_type(db, type)

    @staticmethod
    async def save_built_in_config(objs: list[SaveBuiltInConfigParam], type: str) -> None:
        """
        Save Internal Parameter Configuration

        :param objs: list of parameter configuration parameters
        :param type: parameter configuration type
        :return:
        """
        async with async_db_session.begin() as db:
            for obj in objs:
                config = await config_dao.get_by_key_and_type(db, obj.key, type)
                if config is None:
                    if await config_dao.get_by_key(db, obj.key):
                        raise errors.ForbiddenError(msg=f'parameter configuration {obj.key} exists')
                    await config_dao.create_model(db, obj, flush=True, type=type)
                else:
                    await config_dao.update_model(db, config.id, obj, type=type)

    @staticmethod
    async def get(pk: int) -> Config:
        """
        Get Parameter Configuration Details

        :param pk: Parameter Configuration ID
        :return:
        """
        async with async_db_session() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='Parameter Configuration does not exist')
            return config

    @staticmethod
    async def get_select(*, name: str | None, type: str | None) -> Select:
        """
        Get Parameter Configuration List Query Conditions

        :param name: parameter configuration name
        :param type: parameter configuration type
        :return:
        """
        return await config_dao.get_list(name=name, type=type)

    @staticmethod
    async def create(*, obj: CreateConfigParam) -> None:
        """
        Create Parameter Configuration

        :param obj: parameter configuration create parameters
        :return:
        """
        async with async_db_session.begin() as db:
            if obj.type in config_settings.CONFIG_BUILT_IN_TYPES:
                raise errors.ForbiddenError(msg='Invalid Type Parameters')
            config = await config_dao.get_by_key(db, obj.key)
            if config:
                raise errors.ForbiddenError(msg=f'parameter configuration {obj.key} exists')
            await config_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateConfigParam) -> int:
        """
        Update Parameter Configuration

        :param pk: Parameter Configuration ID
        :param obj: parameter configuration update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='Parameter Configuration does not exist')
            if config.key != obj.key:
                config = await config_dao.get_by_key(db, obj.key)
                if config:
                    raise errors.ForbiddenError(msg=f'parameter configuration {obj.key} exists')
            count = await config_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        Remove Parameter Configuration

        :param pk: Parameter Configuration ID list
        :return:
        """
        async with async_db_session.begin() as db:
            count = await config_dao.delete(db, pk)
            return count


config_service: ConfigService = ConfigService()
