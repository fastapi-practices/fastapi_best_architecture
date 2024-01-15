#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
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


class RoleServiceImpl(RoleServiceABC):
    """
    角色服务实现类
    """

    async def get(self, *, pk: int) -> Role:
        async with async_db_session() as db:
            role = await RoleDao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            return role

    async def get_all(self) -> Sequence[Role]:
        async with async_db_session() as db:
            roles = await RoleDao.get_all(db)
            return roles

    async def get_user_roles(self, *, pk: int) -> Sequence[Role]:
        async with async_db_session() as db:
            roles = await RoleDao.get_user_all(db, user_id=pk)
            return roles

    async def get_select(self, *, name: str = None, data_scope: int = None, status: int = None) -> Select:
        return await RoleDao.get_list(name=name, data_scope=data_scope, status=status)

    async def create(self, *, obj: CreateRole) -> None:
        async with async_db_session.begin() as db:
            role = await RoleDao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='角色已存在')
            await RoleDao.create(db, obj)

    async def update(self, *, pk: int, obj: UpdateRole) -> int:
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

    async def update_role_menu(self, *, request: Request, pk: int, menu_ids: UpdateRoleMenu) -> int:
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

    async def delete(self, *, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await RoleDao.delete(db, pk)
            return count


RoleService: RoleServiceABC = RoleServiceImpl()
