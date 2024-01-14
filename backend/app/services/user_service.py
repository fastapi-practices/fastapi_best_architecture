#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from fastapi import Request
from sqlalchemy import Select

from backend.app.models import User
from backend.app.schemas.user import AddUser, Avatar, RegisterUser, ResetPassword, UpdateUser, UpdateUserRole


class UserServiceABC(ABC):
    """
    用户服务基类
    """

    @abstractmethod
    async def register(self, *, obj: RegisterUser) -> None:
        """
        注册用户

        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def add(self, *, request: Request, obj: AddUser) -> None:
        """
        添加用户

        :param request:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def pwd_reset(self, *, request: Request, obj: ResetPassword) -> int:
        """
        密码重置

        :param request:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def get_userinfo(self, *, username: str) -> User:
        """
        获取用户信息

        :param username:
        :return:
        """
        pass

    @abstractmethod
    async def update(self, *, request: Request, username: str, obj: UpdateUser) -> int:
        """
        更新用户信息

        :param request:
        :param username:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update_roles(self, *, request: Request, username: str, obj: UpdateUserRole) -> None:
        """
        更新用户角色

        :param request:
        :param username:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update_avatar(self, *, request: Request, username: str, avatar: Avatar) -> int:
        """
        更新用户头像

        :param request:
        :param username:
        :param avatar:
        :return:
        """
        pass

    @abstractmethod
    async def get_select(self, *, dept: int, username: str = None, phone: str = None, status: int = None) -> Select:
        """
        获取用户分页查询

        :param dept:
        :param username:
        :param phone:
        :param status:
        :return:
        """
        pass

    @abstractmethod
    async def update_permission(self, *, request: Request, pk: int) -> int:
        """
        更新用户超级权限

        :param request:
        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def update_staff(self, *, request: Request, pk: int) -> int:
        """
        更新用户后台权限

        :param request:
        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def update_status(self, *, request: Request, pk: int) -> int:
        """
        更新用户状态

        :param request:
        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def update_multi_login(self, *, request: Request, pk: int) -> int:
        """
        更新用户多点登录

        :param request:
        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, username: str) -> int:
        """
        删除用户

        :param username:
        :return:
        """
        pass
