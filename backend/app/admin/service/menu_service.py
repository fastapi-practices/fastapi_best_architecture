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
    """菜单服务类"""

    @staticmethod
    async def get(*, pk: int) -> Menu:
        """
        获取菜单详情

        :param pk: 菜单 ID
        :return:
        """
        async with async_db_session() as db:
            menu = await menu_dao.get(db, menu_id=pk)
            if not menu:
                raise errors.NotFoundError(msg='菜单不存在')
            return menu

    @staticmethod
    async def get_menu_tree(*, title: str | None, status: int | None) -> list[dict[str, Any]]:
        """
        获取菜单树形结构

        :param title: 菜单标题
        :param status: 状态
        :return:
        """
        async with async_db_session() as db:
            menu_data = await menu_dao.get_all(db, title=title, status=status)
            menu_tree = get_tree_data(menu_data)
            return menu_tree

    @staticmethod
    async def get_sidebar(*, request: Request) -> list[dict[str, Any] | None]:
        """
        获取用户的菜单侧边栏

        :param request: FastAPI 请求对象
        :return:
        """
        async with async_db_session() as db:
            roles = request.user.roles
            menu_tree = []
            if roles:
                unique_menus = {}
                for role in roles:
                    for menu in role.menus:
                        unique_menus[menu.id] = menu
                all_ids = set(unique_menus.keys())
                valid_menu_ids = [
                    menu_id
                    for menu_id, menu in unique_menus.items()
                    if menu.parent_id is None or menu.parent_id in all_ids
                ]
                menu_data = await menu_dao.get_sidebar(db, request.user.is_superuser, valid_menu_ids)
                menu_tree = get_vben5_tree_data(menu_data)
            return menu_tree

    @staticmethod
    async def create(*, obj: CreateMenuParam) -> None:
        """
        创建菜单

        :param obj: 菜单创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            title = await menu_dao.get_by_title(db, obj.title)
            if title:
                raise errors.ForbiddenError(msg='菜单标题已存在')
            if obj.parent_id:
                parent_menu = await menu_dao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='父级菜单不存在')
            await menu_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateMenuParam) -> int:
        """
        更新菜单

        :param pk: 菜单 ID
        :param obj: 菜单更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            menu = await menu_dao.get(db, pk)
            if not menu:
                raise errors.NotFoundError(msg='菜单不存在')
            if menu.title != obj.title:
                if await menu_dao.get_by_title(db, obj.title):
                    raise errors.ForbiddenError(msg='菜单标题已存在')
            if obj.parent_id:
                parent_menu = await menu_dao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg='父级菜单不存在')
            if obj.parent_id == menu.id:
                raise errors.ForbiddenError(msg='禁止关联自身为父级')
            count = await menu_dao.update(db, pk, obj)
            for role in await menu.awaitable_attrs.roles:
                for user in await role.awaitable_attrs.users:
                    await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        删除菜单

        :param pk: 菜单 ID
        :return:
        """
        async with async_db_session.begin() as db:
            children = await menu_dao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(msg='菜单下存在子菜单，无法删除')
            menu = await menu_dao.get(db, pk)
            count = await menu_dao.delete(db, pk)
            if menu:
                for role in await menu.awaitable_attrs.roles:
                    for user in await role.awaitable_attrs.users:
                        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count


menu_service: MenuService = MenuService()
