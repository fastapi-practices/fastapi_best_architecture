#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from fastapi import Request
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_menu import MenuDao
from backend.app.crud.crud_role import RoleDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import Role
from backend.app.schemas.role import CreateRole, UpdateRole, UpdateRoleMenu


class RoleService:
    @staticmethod
    async def get(*, pk: int) -> Role:
        async with async_db_session() as db:
            role = await RoleDao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            return role

    @staticmethod
    async def get_all() -> Sequence[Role]:
        async with async_db_session() as db:
            roles = await RoleDao.get_all(db)
            return roles

    @staticmethod
    async def get_user_all(*, pk: int) -> Sequence[Role]:
        async with async_db_session() as db:
            roles = await RoleDao.get_user_all(db, user_id=pk)
            return roles

    @staticmethod
    async def get_select(*, name: str = None, data_scope: int = None, status: int = None) -> Select:
        return await RoleDao.get_list(name=name, data_scope=data_scope, status=status)

    @staticmethod
    async def create(*, obj: CreateRole) -> None:
        async with async_db_session.begin() as db:
            role = await RoleDao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='角色已存在')
            await RoleDao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateRole) -> int:
        async with async_db_session.begin() as db:
            role = await RoleDao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            if role.name != obj.name:
                role = await RoleDao.get_by_name(db, obj.name)
                if role:
                    raise errors.ForbiddenError(msg='角色已存在')
            count = await RoleDao.update(db, pk, obj)
            return count

    @staticmethod
    async def update_menus(*, request: Request, pk: int, menu_ids: UpdateRoleMenu) -> int:
        async with async_db_session.begin() as db:
            role = await RoleDao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            for menu_id in menu_ids.menus:
                menu = await MenuDao.get(db, menu_id)
                if not menu:
                    raise errors.NotFoundError(msg='菜单不存在')
            count = await RoleDao.update_menus(db, pk, menu_ids)
            await redis_client.delete_prefix(f'{settings.PERMISSION_REDIS_PREFIX}:{request.user.uuid}')
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await RoleDao.delete(db, pk)
            return count
