#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.app.admin.model import DataScope
from backend.app.admin.schema.data_scope import CreateDataScopeParam, UpdateDataScopeParam, UpdateDataScopeRuleParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class DataScopeService:
    """Data range service category"""

    @staticmethod
    async def get(*, pk: int) -> DataScope:
        """
        Details on the extent of data acquisition

        :param pk: Range ID
        :return:
        """
        async with async_db_session() as db:
            data_scope = await data_scope_dao.get(db, pk)
            if not data_scope:
                raise errors.NotFoundError(msg='Data range does not exist')
            return data_scope

    @staticmethod
    async def get_rules(*, pk: int) -> DataScope:
        """
        Rules on access to data coverage

        :param pk: Range ID
        :return:
        """
        async with async_db_session() as db:
            data_scope = await data_scope_dao.get_with_relation(db, pk)
            if not data_scope:
                raise errors.NotFoundError(msg='Data range does not exist')
            return data_scope

    @staticmethod
    async def get_select(*, name: str | None, status: int | None) -> Select:
        """
        Access data range list query conditions

        :param name: range name
        :param status: range status
        :return:
        """
        return await data_scope_dao.get_list(name, status)

    @staticmethod
    async def create(*, obj: CreateDataScopeParam) -> None:
        """
        Create Data Range

        :param obj: data range parameters
        :return:
        """
        async with async_db_session.begin() as db:
            data_scope = await data_scope_dao.get_by_name(db, obj.name)
            if data_scope:
                raise errors.ForbiddenError(msg='Data range already exists')
            await data_scope_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDataScopeParam) -> int:
        """
        Update data ranges

        :param pk: Range ID
        :param obj: data range update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            data_scope = await data_scope_dao.get(db, pk)
            if not data_scope:
                raise errors.NotFoundError(msg='Data range does not exist')
            if data_scope.name != obj.name:
                if await data_scope_dao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='Data range already exists')
            count = await data_scope_dao.update(db, pk, obj)
            for role in await data_scope.awaitable_attrs.roles:
                for user in await role.awaitable_attrs.users:
                    await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_data_scope_rule(*, pk: int, rule_ids: UpdateDataScopeRuleParam) -> int:
        """
        Update data coverage rules

        :param pk: Range ID
        :param rule ID list
        :return:
        """
        async with async_db_session.begin() as db:
            count = await data_scope_dao.update_rules(db, pk, rule_ids)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        Delete Data Range

        :param pk: Range ID list
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
