#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.config.crud.crud_config import config_dao
from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    UpdateConfigParam,
)


class ConfigService:
    """参数配置服务类"""

    @staticmethod
    async def get(*, pk: int) -> Config:
        """
        获取参数配置详情

        :param pk: 参数配置 ID
        :return:
        """
        async with async_db_session() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='参数配置不存在')
            return config

    @staticmethod
    async def get_select(*, name: str | None, type: str | None) -> Select:
        """
        获取参数配置列表查询条件

        :param name: 参数配置名称
        :param type: 参数配置类型
        :return:
        """
        return await config_dao.get_list(name=name, type=type)

    @staticmethod
    async def create(*, obj: CreateConfigParam) -> None:
        """
        创建参数配置

        :param obj: 参数配置创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            config = await config_dao.get_by_key(db, obj.key)
            if config:
                raise errors.ConflictError(msg=f'参数配置 {obj.key} 已存在')
            await config_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateConfigParam) -> int:
        """
        更新参数配置

        :param pk: 参数配置 ID
        :param obj: 参数配置更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            config = await config_dao.get(db, pk)
            if not config:
                raise errors.NotFoundError(msg='参数配置不存在')
            if config.key != obj.key:
                config = await config_dao.get_by_key(db, obj.key)
                if config:
                    raise errors.ConflictError(msg=f'参数配置 {obj.key} 已存在')
            count = await config_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pks: list[int]) -> int:
        """
        批量删除参数配置

        :param pks: 参数配置 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await config_dao.delete(db, pks)
            return count


config_service: ConfigService = ConfigService()
