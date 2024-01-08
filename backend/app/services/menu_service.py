#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import Request

from backend.app.common.exception import errors
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_menu import MenuDao
from backend.app.crud.crud_role import RoleDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import Menu
from backend.app.schemas.menu import CreateMenu, UpdateMenu
from backend.app.utils.build_tree import get_tree_data


class MenuService:
    @staticmethod
    async def get(*, pk: int) -> Menu:
        async with async_db_session() as db:
            menu = await MenuDao.get(db, menu_id=pk)
            if not menu:
                raise errors.NotFoundError(msg='菜单不存在')
            return menu

    @staticmethod
    async def get_menu_tree(*, title: str | None = None, status: int | None = None) -> list[dict[str, Any]]:
        async with async_db_session() as db:
            menu_select = await MenuDao.get_all(db, title=title, status=status)
            menu_tree = await get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def get_role_menu_tree(*, pk: int) -> list[dict[str, Any]]:
        async with async_db_session() as db:
            role = await RoleDao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            menu_ids = [menu.id for menu in role.menus]
            menu_select = await MenuDao.get_role_menus(db, False, menu_ids)
            menu_tree = await get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def get_user_menu_tree(*, request: Request) -> list[dict[str, Any]]:
        async with async_db_session() as db:
            roles = request.user.roles
            menu_ids = []
            menu_tree = []
            if roles:
                for role in roles:
                    menu_ids.extend([menu.id for menu in role.menus])
                menu_select = await MenuDao.get_role_menus(db, request.user.is_superuser, menu_ids)
                menu_tree = await get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def create(*, obj: CreateMenu) -> None:
        async with async_db_session.begin() as db:
            title = await MenuDao.get_by_title(db, obj.title)
            if title:
                raise errors.ForbiddenError(msg='菜单标题已存在')
            if obj.parent_id:
                parent_menu = await MenuDao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='父级菜单不存在')
            await MenuDao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateMenu) -> int:
        async with async_db_session.begin() as db:
            menu = await MenuDao.get(db, pk)
            if not menu:
                raise errors.NotFoundError(msg='菜单不存在')
            if menu.title != obj.title:
                if await MenuDao.get_by_title(db, obj.title):
                    raise errors.ForbiddenError(msg='菜单标题已存在')
            if obj.parent_id:
                parent_menu = await MenuDao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='父级菜单不存在')
            count = await MenuDao.update(db, pk, obj)
            await redis_client.delete_prefix(settings.PERMISSION_REDIS_PREFIX)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        async with async_db_session.begin() as db:
            children = await MenuDao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(msg='菜单下存在子菜单，无法删除')
            count = await MenuDao.delete(db, pk)
            return count
