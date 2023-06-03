#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.crud.crud_menu import MenuDao
from backend.app.crud.crud_role import RoleDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import Role
from backend.app.schemas.role import CreateRole, UpdateRole


class RoleService:
    @staticmethod
    async def get(pk: int) -> Role:
        async with async_db_session() as db:
            role = await RoleDao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            return role

    @staticmethod
    async def get_select(*, name: str = None, data_scope: int = None) -> Select:
        return await RoleDao.get_all(name=name, data_scope=data_scope)

    @staticmethod
    async def create(*, obj: CreateRole, user_id: int) -> None:
        async with async_db_session.begin() as db:
            role = await RoleDao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='角色已存在')
            for menu_id in obj.menus:
                menu = await MenuDao.get(db, menu_id)
                if not menu:
                    raise errors.ForbiddenError(msg='菜单不存在')
            await RoleDao.create(db, obj, user_id)

    @staticmethod
    async def update(*, pk: int, obj: UpdateRole, user_id: int) -> int:
        async with async_db_session.begin() as db:
            role = await RoleDao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            if role.name != obj.name:
                role = await RoleDao.get_by_name(db, obj.name)
                if role:
                    raise errors.ForbiddenError(msg='角色已存在')
            for menu_id in obj.menus:
                menu = await MenuDao.get(db, menu_id)
                if not menu:
                    raise errors.ForbiddenError(msg='菜单不存在')
            count = await RoleDao.update(db, pk, obj, user_id)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await RoleDao.delete(db, pk)
            return count
