#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.common.rbac import RBAC
from backend.app.crud.crud_casbin import CasbinDao
from backend.app.database.db_mysql import async_db_session
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
    async def get_policy_list(self, *, role: int) -> list:
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


class CasbinServiceImpl(CasbinServiceABC):
    """
    Casbin服务实现类
    """

    async def get_casbin_list(self, *, ptype: str, sub: str) -> Select:
        return await CasbinDao.get_all_policy(ptype, sub)

    async def get_policy_list(self, *, role: int | None = None) -> list:
        enforcer = await RBAC.enforcer()
        if role is not None:
            data = enforcer.get_filtered_named_policy('p', 0, str(role))
        else:
            data = enforcer.get_policy()
        return data

    async def create_policy(self, *, p: CreatePolicy) -> bool:
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_policy(p.sub, p.path, p.method)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    async def create_policies(self, *, ps: list[CreatePolicy]) -> bool:
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    async def update_policy(self, *, old: UpdatePolicy, new: UpdatePolicy) -> bool:
        enforcer = await RBAC.enforcer()
        _p = enforcer.has_policy(old.sub, old.path, old.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.update_policy([old.sub, old.path, old.method], [new.sub, new.path, new.method])
        return data

    async def update_policies(self, *, old: list[UpdatePolicy], new: list[UpdatePolicy]) -> bool:
        enforcer = await RBAC.enforcer()
        data = await enforcer.update_policies(
            [list(o.model_dump().values()) for o in old], [list(n.model_dump().values()) for n in new]
        )
        return data

    async def delete_policy(self, *, p: DeletePolicy) -> bool:
        enforcer = await RBAC.enforcer()
        _p = enforcer.has_policy(p.sub, p.path, p.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_policy(p.sub, p.path, p.method)
        return data

    async def delete_policies(self, *, ps: list[DeletePolicy]) -> bool:
        enforcer = await RBAC.enforcer()
        data = await enforcer.remove_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    async def delete_all_policies(self, *, sub: DeleteAllPolicies) -> int:
        async with async_db_session.begin() as db:
            count = await CasbinDao.delete_policies_by_sub(db, sub)
        return count

    async def get_group_list(self) -> list:
        enforcer = await RBAC.enforcer()
        data = enforcer.get_grouping_policy()
        return data

    async def create_group(self, *, g: CreateUserRole) -> bool:
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_grouping_policy(g.uuid, g.role)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    async def create_groups(self, *, gs: list[CreateUserRole]) -> bool:
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    async def delete_group(self, *, g: DeleteUserRole) -> bool:
        enforcer = await RBAC.enforcer()
        _g = enforcer.has_grouping_policy(g.uuid, g.role)
        if not _g:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_grouping_policy(g.uuid, g.role)
        return data

    async def delete_groups(self, *, gs: list[DeleteUserRole]) -> bool:
        enforcer = await RBAC.enforcer()
        data = await enforcer.remove_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    async def delete_all_groups(self, *, uuid: str) -> int:
        async with async_db_session.begin() as db:
            count = await CasbinDao.delete_groups_by_uuid(db, uuid)
        return count


CasbinService: CasbinServiceABC = CasbinServiceImpl()
