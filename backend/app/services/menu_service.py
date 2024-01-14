#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any

from fastapi import Request

from backend.app.models import Menu
from backend.app.schemas.menu import CreateMenu, UpdateMenu


class MenuServiceABC(ABC):
    """
    菜单服务基类
    """

    @abstractmethod
    async def get(self, *, pk: int) -> Menu:
        """
        获取菜单详情

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def get_menu_tree(self, *, title: str | None = None, status: int | None = None) -> list[dict[str, Any]]:
        """
        获取所有菜单展示树

        :param title:
        :param status:
        :return:
        """
        pass

    @abstractmethod
    async def get_role_menu_tree(self, *, pk: int) -> list[dict[str, Any]]:
        """
        获取角色所有菜单

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def get_user_menu_tree(self, *, request: Request) -> list[dict[str, Any]]:
        """
        获取用户菜单展示树

        :param request:
        :return:
        """
        pass

    @abstractmethod
    async def create(self, *, obj: CreateMenu) -> None:
        """
        创建菜单

        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update(self, *, pk: int, obj: UpdateMenu) -> int:
        """
        更新菜单

        :param pk:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: int) -> int:
        """
        删除菜单

        :param pk:
        :return:
        """
        pass
