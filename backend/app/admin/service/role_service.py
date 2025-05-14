#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.model import Role
from backend.app.admin.schema.role import (
    CreateRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.build_tree import get_tree_data


class RoleService:
    """Role service category"""

    @staticmethod
    async def get(*, pk: int) -> Role:
        """
        Get Role Details

        :param pk: Role ID
        :return:
        """
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Role does not exist')
            return role

    @staticmethod
    async def get_all() -> Sequence[Role]:
        """Get All Roles"""
        async with async_db_session() as db:
            roles = await role_dao.get_all(db)
            return roles

    @staticmethod
    async def get_users(*, pk: int) -> Sequence[Role]:
        """
        Retrieving user role lists

        :param pk: User ID
        :return:
        """
        async with async_db_session() as db:
            roles = await role_dao.get_users(db, user_id=pk)
            return roles

    @staticmethod
    async def get_select(*, name: str | None, status: int | None) -> Select:
        """
        Fetching Role List Query Conditions

        :param name: role name
        :param status: status
        :return:
        """
        return await role_dao.get_list(name=name, status=status)

    @staticmethod
    async def get_menu_tree(*, pk: int) -> list[dict[str, Any]]:
        """
        Menu Tree Structure for Fetching Roles

        :param pk: Role ID
        :return:
        """
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Role does not exist')
            menu_ids = [menu.id for menu in role.menus]
            menu_select = await menu_dao.get_role_menus(db, False, menu_ids)
            menu_tree = get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def get_scopes(*, pk: int) -> list[int]:
        """
        Get a list of role data ranges

        :param pk:
        :return:
        """
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Role does not exist')
            scope_ids = [scope.id for scope in role.scopes]
            return scope_ids

    @staticmethod
    async def create(*, obj: CreateRoleParam) -> None:
        """
        Create Role

        :param obj: role creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='Role Exists')
            await role_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateRoleParam) -> int:
        """
        Update Role

        :param pk: Role ID
        :param obj: role update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Role does not exist')
            if role.name != obj.name:
                role = await role_dao.get_by_name(db, obj.name)
                if role:
                    raise errors.ForbiddenError(msg='Role Exists')
            count = await role_dao.update(db, pk, obj)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete_prefix(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_role_menu(*, pk: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        Update Role Menu

        :param pk: Role ID
        :param menu_ids: menu ID list
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Role does not exist')
            for menu_id in menu_ids.menus:
                menu = await menu_dao.get(db, menu_id)
                if not menu:
                    raise errors.NotFoundError(msg='Menu does not exist')
            count = await role_dao.update_menus(db, pk, menu_ids)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete_prefix(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_role_scope(*, pk: int, scope_ids: UpdateRoleScopeParam) -> int:
        """
        Update role data range

        :param pk: Role ID
        :param caption ID list
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Role does not exist')
            for scope_id in scope_ids.scopes:
                scope = await data_scope_dao.get(db, scope_id)
                if not scope:
                    raise errors.NotFoundError(msg='Data range does not exist')
            count = await role_dao.update_scopes(db, pk, scope_ids)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        Remove Role

        :param pk: Role ID list
        :return:
        """
        async with async_db_session.begin() as db:
            count = await role_dao.delete(db, pk)
            for _pk in pk:
                role = await role_dao.get(db, _pk)
                if role:
                    for user in await role.awaitable_attrs.users:
                        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count


role_service: RoleService = RoleService()
