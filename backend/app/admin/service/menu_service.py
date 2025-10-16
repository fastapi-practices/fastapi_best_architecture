from typing import Any

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.model import Menu
from backend.app.admin.schema.menu import CreateMenuParam, UpdateMenuParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.build_tree import get_tree_data, get_vben5_tree_data


class MenuService:
    """菜单服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Menu:
        """
        获取菜单详情

        :param db: 数据库会话
        :param pk: 菜单 ID
        :return:
        """

        menu = await menu_dao.get(db, menu_id=pk)
        if not menu:
            raise errors.NotFoundError(msg='菜单不存在')
        return menu

    @staticmethod
    async def get_tree(*, db: AsyncSession, title: str | None, status: int | None) -> list[dict[str, Any]]:
        """
        获取菜单树形结构

        :param db: 数据库会话
        :param title: 菜单标题
        :param status: 状态
        :return:
        """

        menu_data = await menu_dao.get_all(db, title=title, status=status)
        menu_tree = get_tree_data(menu_data)
        return menu_tree

    @staticmethod
    async def get_sidebar(*, db: AsyncSession, request: Request) -> list[dict[str, Any] | None]:
        """
        获取用户的菜单侧边栏

        :param db: 数据库会话
        :param request: FastAPI 请求对象
        :return:
        """

        if request.user.is_superuser:
            menu_data = await menu_dao.get_sidebar(db, None)
        else:
            roles = request.user.roles
            menu_ids = set()
            if roles:
                for role in roles:
                    menu_ids.update(menu.id for menu in role.menus)
                menu_data = await menu_dao.get_sidebar(db, list(menu_ids))
        menu_tree = get_vben5_tree_data(menu_data)
        return menu_tree

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateMenuParam) -> None:
        """
        创建菜单

        :param db: 数据库会话
        :param obj: 菜单创建参数
        :return:
        """

        title = await menu_dao.get_by_title(db, obj.title)
        if title:
            raise errors.ConflictError(msg='菜单标题已存在')
        if obj.parent_id:
            parent_menu = await menu_dao.get(db, obj.parent_id)
            if not parent_menu:
                raise errors.NotFoundError(msg='父级菜单不存在')
        await menu_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateMenuParam) -> int:
        """
        更新菜单

        :param db: 数据库会话
        :param pk: 菜单 ID
        :param obj: 菜单更新参数
        :return:
        """

        menu = await menu_dao.get(db, pk)
        if not menu:
            raise errors.NotFoundError(msg='菜单不存在')
        if menu.title != obj.title and await menu_dao.get_by_title(db, obj.title):
            raise errors.ConflictError(msg='菜单标题已存在')
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
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除菜单

        :param db: 数据库会话
        :param pk: 菜单 ID
        :return:
        """

        children = await menu_dao.get_children(db, pk)
        if children:
            raise errors.ConflictError(msg='菜单下存在子菜单，无法删除')
        menu = await menu_dao.get(db, pk)
        count = await menu_dao.delete(db, pk)
        if menu:
            for role in await menu.awaitable_attrs.roles:
                for user in await role.awaitable_attrs.users:
                    await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count


menu_service: MenuService = MenuService()
