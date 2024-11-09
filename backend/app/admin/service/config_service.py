#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.admin.crud.crud_config import config_dao
from backend.app.admin.model import Config
from backend.app.admin.schema.config import CreateConfigParam, UpdateConfigParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class ConfigService:
    @staticmethod
    async def get() -> Config | dict:
        async with async_db_session() as db:
            config = await config_dao.get(db)
            if not config:
                raise errors.NotFoundError(msg='配置不存在')
            return config

    @staticmethod
    async def get_select(): ...

    @staticmethod
    async def create(*, obj: CreateConfigParam) -> None:
        async with async_db_session.begin():
            ...

    @staticmethod
    async def update(*, pk: int, obj: UpdateConfigParam) -> int:
        async with async_db_session.begin():
            ...

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin():
            ...


config_service: ConfigService = ConfigService()
