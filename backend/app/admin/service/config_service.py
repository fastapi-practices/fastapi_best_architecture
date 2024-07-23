#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.app.admin.crud.crud_config import config_dao
from backend.app.admin.model import Config
from backend.app.admin.schema.config import CreateConfigParam, UpdateConfigParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class ConfigService:
    @staticmethod
    async def get(*, pk: int) -> Config:
        async with async_db_session() as db:
            sys_config = await config_dao.get(db, pk)
            if not sys_config:
                raise errors.NotFoundError(msg='接口不存在')
            return sys_config

    @staticmethod
    async def get_all() -> Sequence[Config]:
        async with async_db_session() as db:
            sys_configs = await config_dao.get_all(db)
            return sys_configs

    @staticmethod
    async def create(*, obj: CreateConfigParam) -> None:
        async with async_db_session.begin() as db:
            sys_config = await config_dao.get_by_name(db, obj.name)
            if sys_config:
                raise errors.ForbiddenError(msg='系统配置已存在')
            await config_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateConfigParam) -> int:
        async with async_db_session.begin() as db:
            count = await config_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await config_dao.delete(db, pk)
            return count


sys_config_service = ConfigService()
