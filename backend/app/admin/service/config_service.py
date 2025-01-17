#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_config import config_dao
from backend.app.admin.model import Config
from backend.app.admin.schema.config import (
    CreateConfigParam,
    SaveBuiltInConfigParam,
    UpdateConfigParam,
)
from backend.common.exception import errors
from backend.database.db import async_db_session


class ConfigService:
    @staticmethod
    async def get_built_in_config(type: str) -> Sequence[Config]:
        async with async_db_session() as db:
            return await config_dao.get_by_type(db, type)

    @staticmethod
    async def save_built_in_config(objs: list[SaveBuiltInConfigParam], type: str) -> None:
        async with async_db_session.begin() as db:
            for obj in objs:
                config = await config_dao.get_by_key_and_type(db, obj.key, type)
                if config is None:
                    if await config_dao.get_by_key(db, obj.key, built_in=True):
                        raise errors.ForbiddenError(msg=f'参数配置 {obj.key} 已存在')
                    await config_dao.create_model(db, obj, flush=True, type=type)
                else:
                    await config_dao.update_model(db, config.id, obj, type=type)

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
    async def create(*, obj: CreateConfigParam) -> None:
        async with async_db_session.begin() as db:
            if obj.type in admin_settings.CONFIG_BUILT_IN_TYPES:
                raise errors.ForbiddenError(msg='非法类型参数')
            config = await config_dao.get_by_key(db, obj.key)
            if config:
                raise errors.ForbiddenError(msg=f'参数配置 {obj.key} 已存在')
            await config_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateConfigParam) -> int:
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
