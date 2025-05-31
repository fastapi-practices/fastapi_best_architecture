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
    """角色服务类"""

    @staticmethod
    async def get(*, pk: int) -> Role:
        """
        获取角色详情

        :param pk: 角色 ID
        :return:
        """
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            return role

    @staticmethod
    async def get_all() -> Sequence[Role]:
        """获取所有角色"""
        async with async_db_session() as db:
            roles = await role_dao.get_all(db)
            return roles

    @staticmethod
    async def get_select(*, name: str | None, status: int | None) -> Select:
        """
        获取角色列表查询条件

        :param name: 角色名称
        :param status: 状态
        :return:
        """
        return await role_dao.get_list(name=name, status=status)

    @staticmethod
    async def get_menu_tree(*, pk: int) -> list[dict[str, Any] | None]:
        """
        获取角色的菜单树形结构

        :param pk: 角色 ID
        :return:
        """
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            menu_tree = get_tree_data(role.menus) if role.menus else []
            return menu_tree

    @staticmethod
    async def get_scopes(*, pk: int) -> list[int]:
        """
        获取角色数据范围列表

        :param pk:
        :return:
        """
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            scope_ids = [scope.id for scope in role.scopes]
            return scope_ids

    @staticmethod
    async def create(*, obj: CreateRoleParam) -> None:
        """
        创建角色

        :param obj: 角色创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='角色已存在')
            await role_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateRoleParam) -> int:
        """
        更新角色

        :param pk: 角色 ID
        :param obj: 角色更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            if role.name != obj.name:
                if await role_dao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='角色已存在')
            count = await role_dao.update(db, pk, obj)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete_prefix(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_role_menu(*, pk: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单

        :param pk: 角色 ID
        :param menu_ids: 菜单 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for menu_id in menu_ids.menus:
                menu = await menu_dao.get(db, menu_id)
                if not menu:
                    raise errors.NotFoundError(msg='菜单不存在')
            count = await role_dao.update_menus(db, pk, menu_ids)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete_prefix(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_role_scope(*, pk: int, scope_ids: UpdateRoleScopeParam) -> int:
        """
        更新角色数据范围

        :param pk: 角色 ID
        :param scope_ids: 权限规则 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for scope_id in scope_ids.scopes:
                scope = await data_scope_dao.get(db, scope_id)
                if not scope:
                    raise errors.NotFoundError(msg='数据范围不存在')
            count = await role_dao.update_scopes(db, pk, scope_ids)
            for user in await role.awaitable_attrs.users:
                await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        删除角色

        :param pk: 角色 ID 列表
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
