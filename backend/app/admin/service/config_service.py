#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_config import config_dao
from backend.app.admin.model import Config
from backend.app.admin.schema.config import CreateConfigParam, UpdateConfigParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session
from backend.database.db_redis import redis_client
from backend.utils.serializers import select_as_dict


class ConfigService:
    @staticmethod
    async def get() -> Config | dict:
        async with async_db_session() as db:
            cache_config = await redis_client.hgetall(admin_settings.CONFIG_REDIS_KEY)
            if not cache_config:
                config = await config_dao.get_one(db)
                if not config:
                    raise errors.NotFoundError(msg='系统配置不存在')
                data_map = select_as_dict(config)
                del data_map['created_time']
                del data_map['updated_time']
                await redis_client.hset(admin_settings.CONFIG_REDIS_KEY, mapping=data_map)
                return config
            else:
                return cache_config

    @staticmethod
    async def create(*, obj: CreateConfigParam) -> None:
        async with async_db_session.begin() as db:
            config = await config_dao.get_one(db)
            if config:
                raise errors.ForbiddenError(msg='系统配置已存在')
            await config_dao.create(db, obj)
            await redis_client.hset(admin_settings.CONFIG_REDIS_KEY, mapping=obj.model_dump())

    @staticmethod
    async def update(*, pk: int, obj: UpdateConfigParam) -> int:
        async with async_db_session.begin() as db:
            count = await config_dao.update(db, pk, obj)
            await redis_client.hset(admin_settings.CONFIG_REDIS_KEY, mapping=obj.model_dump())
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            configs = await config_dao.get_all(db)
            if len(configs) == 1:
                raise errors.ForbiddenError(msg='系统配置无法彻底删除')
            count = await config_dao.delete(db, pk)
            await redis_client.delete(admin_settings.CONFIG_REDIS_KEY)
            return count


config_service = ConfigService()
