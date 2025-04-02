#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.config.conf import config_settings
from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import CreateConfigParam, UpdateConfigParam


class CRUDConfig(CRUDPlus[Config]):
    """系统参数参数配置数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> Config | None:
        """
        获取参数配置详情

        :param db: 数据库会话
        :param pk: 参数配置 ID
        :return:
        """
        return await self.select_model_by_column(db, id=pk, type__not_in=config_settings.CONFIG_BUILT_IN_TYPES)

    async def get_by_type(self, db: AsyncSession, type: str) -> Sequence[Config]:
        """
        通过类型获取参数配置

        :param db: 数据库会话
        :param type: 参数配置类型
        :return:
        """
        return await self.select_models(db, type=type)

    async def get_by_key_and_type(self, db: AsyncSession, key: str, type: str) -> Config | None:
        """
        通过键名和类型获取参数配置

        :param db: 数据库会话
        :param key: 参数配置键名
        :param type: 参数配置类型
        :return:
        """
        return await self.select_model_by_column(db, key=key, type=type)

    async def get_by_key(self, db: AsyncSession, key: str) -> Config | None:
        """
        通过键名获取参数配置

        :param db: 数据库会话
        :param key: 参数配置键名
        :return:
        """
        return await self.select_model_by_column(db, key=key)

    async def get_list(self, name: str | None = None, type: str | None = None) -> Select:
        """
        获取参数配置列表

        :param name: 参数配置名称
        :param type: 参数配置类型
        :return:
        """
        filters = {'type__not_in': config_settings.CONFIG_BUILT_IN_TYPES}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if type is not None:
            filters.update(type__like=f'%{type}%')
        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateConfigParam) -> None:
        """
        创建参数配置

        :param db: 数据库会话
        :param obj: 创建参数配置参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateConfigParam) -> int:
        """
        更新参数配置

        :param db: 数据库会话
        :param pk: 参数配置 ID
        :param obj: 更新参数配置参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除参数配置

        :param db: 数据库会话
        :param pk: 参数配置 ID 列表
        :return:
        """
        return await self.delete_model_by_column(
            db, allow_multiple=True, id__in=pk, type__not_in=config_settings.CONFIG_BUILT_IN_TYPES
        )


config_dao: CRUDConfig = CRUDConfig(Config)
