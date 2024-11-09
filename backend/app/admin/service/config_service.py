#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_config import config_dao
from backend.app.admin.model import Config
from backend.app.admin.schema.config import (
    CreateAnyConfigParam,
    SaveConfigParam,
    UpdateAnyConfigParam,
)
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class ConfigService:
    @staticmethod
    async def get_website() -> Sequence[Config]:
        async with async_db_session() as db:
            return await config_dao.get_by_type(db, 'website')

    @staticmethod
    async def save_website(obj: SaveConfigParam):
        async with async_db_session.begin() as db:
            config = await config_dao.get_by_name(db, obj.name)
            if config is None:
                await config_dao.create_models()

    @staticmethod
    async def get_protocol() -> Sequence[Config]:
        async with async_db_session() as db:
            return await config_dao.get_by_type(db, 'protocol')

    @staticmethod
    async def save_protocol(obj: SaveConfigParam):
        pass

    @staticmethod
    async def get_policy() -> Sequence[Config]:
        async with async_db_session() as db:
            return await config_dao.get_by_type(db, 'policy')

    @staticmethod
    async def save_policy(obj: SaveConfigParam):
        pass

    @staticmethod
    async def get(pk) -> Config | dict:
        async with async_db_session() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='参数配置不存在')
            return config

    @staticmethod
    async def get_select(*, name: str = None, type: str = None) -> Select:
        return await config_dao.get_list(name=name, type=type)

    @staticmethod
    async def create(*, obj: CreateAnyConfigParam) -> None:
        async with async_db_session.begin() as db:
            config = await config_dao.get_by_name(db, obj.name)
            if config:
                raise errors.ForbiddenError(msg='参数配置已存在')
            if obj.type in admin_settings.CONFIG_BUILT_IN_TYPES:
                raise errors.ForbiddenError(msg='非法类型参数')
            await config_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateAnyConfigParam) -> int:
        async with async_db_session.begin() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='参数配置不存在')
            count = await config_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await config_dao.delete(db, pk)
            return count


config_service: ConfigService = ConfigService()
