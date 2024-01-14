#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Sequence

from fastapi import Request
from sqlalchemy import Select

from backend.app.models import Role
from backend.app.schemas.role import CreateRole, UpdateRole, UpdateRoleMenu


class RoleServiceABC(ABC):
    """
    角色服务基类
    """

    @abstractmethod
    async def get(self, *, pk: int) -> Role:
        """
        获取角色详情

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[Role]:
        """
        获取所有角色

        :return:
        """
        pass

    @abstractmethod
    async def get_user_roles(self, *, pk: int) -> Sequence[Role]:
        """
        获取用户所有角色

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def get_select(self, *, name: str = None, data_scope: int = None, status: int = None) -> Select:
        """
        获取角色分页查询

        :param name:
        :param data_scope:
        :param status:
        :return:
        """
        pass

    @abstractmethod
    async def create(self, *, obj: CreateRole) -> None:
        """
        创建角色

        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update(self, *, pk: int, obj: UpdateRole) -> int:
        """
        更新角色

        :param pk:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update_role_menu(self, *, request: Request, pk: int, menu_ids: UpdateRoleMenu) -> int:
        """
        更新角色菜单

        :param request:
        :param pk:
        :param menu_ids:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: list[int]) -> int:
        """
        删除角色

        :param pk:
        :return:
        """
        pass
