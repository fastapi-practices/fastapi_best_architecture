#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import Request

from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.model import Menu
from backend.app.admin.schema.menu import CreateMenuParam, UpdateMenuParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.build_tree import get_tree_data, get_vben5_tree_data


class MenuService:
    """Menu service class"""

    @staticmethod
    async def get(*, pk: int) -> Menu:
        """
        Get Menu Details

        :param pk: menu ID
        :return:
        """
        async with async_db_session() as db:
            menu = await menu_dao.get(db, menu_id=pk)
            if not menu:
                raise errors.NotFoundError(msg='Menu does not exist')
            return menu

    @staticmethod
    async def get_menu_tree(*, title: str | None, status: int | None) -> list[dict[str, Any]]:
        """
        Get Menu Tree Structure

        :param type: menu title
        :param status: status
        :return:
        """
        async with async_db_session() as db:
            menu_select = await menu_dao.get_all(db, title=title, status=status)
            menu_tree = get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def get_user_menu_tree(*, request: Request) -> list[dict[str, Any]]:
        """
        Get user's menu tree structure

        :param request: FastAPI
        :return:
        """
        async with async_db_session() as db:
            roles = request.user.roles
            menu_ids = []
            menu_tree = []
            if roles:
                for role in roles:
                    menu_ids.extend([menu.id for menu in role.menus])
                menu_select = await menu_dao.get_role_menus(db, request.user.is_superuser, menu_ids)
                menu_tree = get_vben5_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def create(*, obj: CreateMenuParam) -> None:
        """
        Create Menu

        :param obj: menu creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            title = await menu_dao.get_by_title(db, obj.title)
            if title:
                raise errors.ForbiddenError(msg='Menu Title Exists')
            if obj.parent_id:
                parent_menu = await menu_dao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='Parent menu does not exist')
            await menu_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateMenuParam) -> int:
        """
        Update Menu

        :param pk: menu ID
        :param obj: menu update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            menu = await menu_dao.get(db, pk)
            if not menu:
                raise errors.NotFoundError(msg='Menu does not exist')
            if menu.title != obj.title:
                if await menu_dao.get_by_title(db, obj.title):
                    raise errors.ForbiddenError(msg='Menu Title Exists')
            if obj.parent_id:
                parent_menu = await menu_dao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='Parent menu does not exist')
            if obj.parent_id == menu.id:
                raise errors.ForbiddenError(msg='Prohibit association with parent')
            count = await menu_dao.update(db, pk, obj)
            for role in await menu.awaitable_attrs.roles:
                for user in await role.awaitable_attrs.users:
                    await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        Remove Menu

        :param pk: menu ID
        :return:
        """
        async with async_db_session.begin() as db:
            children = await menu_dao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(msg='Exists submenu under menu, cannot be deleted')
            menu = await menu_dao.get(db, pk)
            count = await menu_dao.delete(db, pk)
            if menu:
                for role in await menu.awaitable_attrs.roles:
                    for user in await role.awaitable_attrs.users:
                        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count


menu_service: MenuService = MenuService()
