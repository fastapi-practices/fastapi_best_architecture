#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.conf import admin_settings
from backend.app.admin.model import Config
from backend.app.admin.schema.config import CreateConfigParam, UpdateConfigParam


class CRUDConfig(CRUDPlus[Config]):
    async def get(self, db: AsyncSession, pk: int) -> Config | None:
        """
        获取系统参数配置

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model_by_column(db, id=pk, type__not_in=admin_settings.CONFIG_BUILT_IN_TYPES)

    async def get_by_type(self, db: AsyncSession, type: str) -> Sequence[Config]:
        """
        通过 type 获取内置系统配置

        :param db:
        :param type:
        :return:
        """
        return await self.select_models(db, type=type)

    async def get_by_key_and_type(self, db: AsyncSession, key: str, type: str) -> Config | None:
        """
        通过 name 和 type 获取内置系统配置

        :param db:
        :param key:
        :param type:
        :return:
        """
        return await self.select_model_by_column(db, key=key, type=type)

    async def get_by_key(self, db: AsyncSession, key: str) -> Config | None:
        """
        通过 key 获取系统配置参数

        :param db:
        :param key:
        :param built_in:
        :return:
        """
        return await self.select_model_by_column(db, key=key)

    async def get_list(self, name: str = None, type: str = None) -> Select:
        """
        获取系统参数配置列表

        :param name:
        :param type:
        :return:
        """
        filters = {'type__not_in': admin_settings.CONFIG_BUILT_IN_TYPES}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if type is not None:
            filters.update(type__like=f'%{type}%')
        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj_in: CreateConfigParam) -> None:
        """
        创建 Config

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateConfigParam) -> int:
        """
        更新 Config

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 Config

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(
            db, allow_multiple=True, id__in=pk, type__not_in=admin_settings.CONFIG_BUILT_IN_TYPES
        )


config_dao: CRUDConfig = CRUDConfig(Config)
