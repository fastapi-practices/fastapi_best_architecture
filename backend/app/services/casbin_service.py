#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from sqlalchemy import Select

from backend.app.schemas.casbin_rule import (
    CreatePolicy,
    CreateUserRole,
    DeleteAllPolicies,
    DeletePolicy,
    DeleteUserRole,
    UpdatePolicy,
)


class CasbinServiceABC(ABC):
    """
    Casbin服务基类
    """

    @abstractmethod
    async def get_casbin_list(self, *, ptype: str, sub: str) -> Select:
        """
        获取Casbin规则列表

        :param ptype:
        :param sub:
        :return:
        """
        pass

    @abstractmethod
    async def get_policy_list(self, *, role: str) -> list:
        """
        获取P规则列表

        :return:
        """
        pass

    @abstractmethod
    async def create_policy(self, *, p: CreatePolicy) -> bool:
        """
        创建P规则

        :param p:
        :return:
        """
        pass

    @abstractmethod
    async def create_policies(self, *, ps: list[CreatePolicy]) -> bool:
        """
        创建多组P规则

        :param ps:
        :return:
        """
        pass

    @abstractmethod
    async def update_policy(self, *, old: UpdatePolicy, new: UpdatePolicy) -> bool:
        """
        更新P规则

        :param old:
        :param new:
        :return:
        """
        pass

    @abstractmethod
    async def update_policies(self, *, old: list[UpdatePolicy], new: list[UpdatePolicy]) -> bool:
        """
        更新多组P规则

        :param old:
        :param new:
        :return:
        """
        pass

    @abstractmethod
    async def delete_policy(self, *, p: DeletePolicy) -> bool:
        """
        删除P规则

        :param p:
        :return:
        """
        pass

    @abstractmethod
    async def delete_policies(self, *, ps: list[DeletePolicy]) -> bool:
        """
        删除多组P规则

        :param ps:
        :return:
        """
        pass

    @abstractmethod
    async def delete_all_policies(self, *, sub: DeleteAllPolicies) -> int:
        """
        删除所有P规则

        :param sub:
        :return:
        """
        pass

    @abstractmethod
    async def get_group_list(self) -> list:
        """
        获取G规则列表

        :return:
        """
        pass

    @abstractmethod
    async def create_group(self, *, g: CreateUserRole) -> bool:
        """
        创建G规则

        :param g:
        :return:
        """
        pass

    @abstractmethod
    async def create_groups(self, *, gs: list[CreateUserRole]) -> bool:
        """
        创建多组G规则

        :param gs:
        :return:
        """
        pass

    @abstractmethod
    async def delete_group(self, *, g: DeleteUserRole) -> bool:
        """
        删除G规则

        :param g:
        :return:
        """
        pass

    @abstractmethod
    async def delete_groups(self, *, gs: list[DeleteUserRole]) -> bool:
        """
        删除多组G规则

        :param gs:
        :return:
        """
        pass

    @abstractmethod
    async def delete_all_groups(self, *, uuid: str) -> int:
        """
        删除所有G规则

        :param uuid:
        :return:
        """
        pass
