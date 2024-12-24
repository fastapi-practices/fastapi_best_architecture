#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from fastapi import Request
from sqlalchemy import Select

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.model import Role
from backend.app.admin.schema.role import (
    CreateRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleRuleParam,
)
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class RoleService:
    @staticmethod
    async def get(*, pk: int) -> Role:
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            return role

    @staticmethod
    async def get_all() -> Sequence[Role]:
        async with async_db_session() as db:
            roles = await role_dao.get_all(db)
            return roles

    @staticmethod
    async def get_by_user(*, pk: int) -> Sequence[Role]:
        async with async_db_session() as db:
            roles = await role_dao.get_by_user(db, user_id=pk)
            return roles

    @staticmethod
    async def get_select(*, name: str = None, status: int = None) -> Select:
        return await role_dao.get_list(name=name, status=status)

    @staticmethod
    async def create(*, obj: CreateRoleParam) -> None:
        async with async_db_session.begin() as db:
            role = await role_dao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='角色已存在')
            await role_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateRoleParam) -> int:
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            if role.name != obj.name:
                role = await role_dao.get_by_name(db, obj.name)
                if role:
                    raise errors.ForbiddenError(msg='角色已存在')
            count = await role_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def update_role_menu(*, request: Request, pk: int, menu_ids: UpdateRoleMenuParam) -> int:
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for menu_id in menu_ids.menus:
                menu = await menu_dao.get(db, menu_id)
                if not menu:
                    raise errors.NotFoundError(msg='菜单不存在')
            count = await role_dao.update_menus(db, pk, menu_ids)
            if pk in [role.id for role in request.user.roles]:
                await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{request.user.id}')
            return count

    @staticmethod
    async def update_role_rule(*, request: Request, pk: int, rule_ids: UpdateRoleRuleParam) -> int:
        async with async_db_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for rule_id in rule_ids.rules:
                rule = await data_rule_dao.get(db, rule_id)
                if not rule:
                    raise errors.NotFoundError(msg='数据权限不存在')
            count = await role_dao.update_rules(db, pk, rule_ids)
            if pk in [role.id for role in request.user.roles]:
                await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{request.user.id}')
            return count

    @staticmethod
    async def delete(*, request: Request, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await role_dao.delete(db, pk)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{request.user.id}')
            return count


role_service: RoleService = RoleService()
