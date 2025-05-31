#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.app.admin.model import DataScope
from backend.app.admin.schema.data_scope import CreateDataScopeParam, UpdateDataScopeParam, UpdateDataScopeRuleParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class DataScopeService:
    """数据范围服务类"""

    @staticmethod
    async def get(*, pk: int) -> DataScope:
        """
        获取数据范围详情

        :param pk: 范围 ID
        :return:
        """
        async with async_db_session() as db:
            data_scope = await data_scope_dao.get(db, pk)
            if not data_scope:
                raise errors.NotFoundError(msg='数据范围不存在')
            return data_scope

    @staticmethod
    async def get_all() -> Sequence[DataScope]:
        """获取所有数据范围"""
        async with async_db_session() as db:
            data_scopes = await data_scope_dao.get_all(db)
            return data_scopes

    @staticmethod
    async def get_rules(*, pk: int) -> DataScope:
        """
        获取数据范围规则

        :param pk: 范围 ID
        :return:
        """
        async with async_db_session() as db:
            data_scope = await data_scope_dao.get_with_relation(db, pk)
            if not data_scope:
                raise errors.NotFoundError(msg='数据范围不存在')
            return data_scope

    @staticmethod
    async def get_select(*, name: str | None, status: int | None) -> Select:
        """
        获取数据范围列表查询条件

        :param name: 范围名称
        :param status: 范围状态
        :return:
        """
        return await data_scope_dao.get_list(name, status)

    @staticmethod
    async def create(*, obj: CreateDataScopeParam) -> None:
        """
        创建数据范围

        :param obj: 数据范围参数
        :return:
        """
        async with async_db_session.begin() as db:
            data_scope = await data_scope_dao.get_by_name(db, obj.name)
            if data_scope:
                raise errors.ForbiddenError(msg='数据范围已存在')
            await data_scope_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDataScopeParam) -> int:
        """
        更新数据范围

        :param pk: 范围 ID
        :param obj: 数据范围更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            data_scope = await data_scope_dao.get(db, pk)
            if not data_scope:
                raise errors.NotFoundError(msg='数据范围不存在')
            if data_scope.name != obj.name:
                if await data_scope_dao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='数据范围已存在')
            count = await data_scope_dao.update(db, pk, obj)
            for role in await data_scope.awaitable_attrs.roles:
                for user in await role.awaitable_attrs.users:
                    await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_data_scope_rule(*, pk: int, rule_ids: UpdateDataScopeRuleParam) -> int:
        """
        更新数据范围规则

        :param pk: 范围 ID
        :param rule_ids: 规则 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await data_scope_dao.update_rules(db, pk, rule_ids)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        删除数据范围

        :param pk: 范围 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await data_scope_dao.delete(db, pk)
            for _pk in pk:
                data_rule = await data_scope_dao.get(db, _pk)
                if data_rule:
                    for role in await data_rule.awaitable_attrs.roles:
                        for user in await role.awaitable_attrs.users:
                            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count


data_scope_service: DataScopeService = DataScopeService()
