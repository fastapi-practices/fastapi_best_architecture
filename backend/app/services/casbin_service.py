#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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


class CasbinService:
    @staticmethod
    async def get_casbin_list(*, ptype: str, sub: str) -> Select:
        return await CasbinDao.get_all_policy(ptype, sub)

    @staticmethod
    async def get_policy_list():
        enforcer = await RBAC.enforcer()
        data = enforcer.get_policy()
        return data

    @staticmethod
    async def get_policy_list_by_role(*, role: str):
        enforcer = await RBAC.enforcer()
        data = enforcer.get_filtered_named_policy('p', 0, role)
        return data

    @staticmethod
    async def create_policy(*, p: CreatePolicy):
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_policy(p.sub, p.path, p.method)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def create_policies(*, ps: list[CreatePolicy]):
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def update_policy(*, old: UpdatePolicy, new: UpdatePolicy):
        enforcer = await RBAC.enforcer()
        _p = enforcer.has_policy(old.sub, old.path, old.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.update_policy([old.sub, old.path, old.method], [new.sub, new.path, new.method])
        return data

    @staticmethod
    async def update_policies(*, old: list[UpdatePolicy], new: list[UpdatePolicy]):
        enforcer = await RBAC.enforcer()
        data = await enforcer.update_policies(
            [list(o.model_dump().values()) for o in old], [list(n.model_dump().values()) for n in new]
        )
        return data

    @staticmethod
    async def delete_policy(*, p: DeletePolicy):
        enforcer = await RBAC.enforcer()
        _p = enforcer.has_policy(p.sub, p.path, p.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_policy(p.sub, p.path, p.method)
        return data

    @staticmethod
    async def delete_policies(*, ps: list[DeletePolicy]):
        enforcer = await RBAC.enforcer()
        data = await enforcer.remove_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    @staticmethod
    async def delete_all_policies(*, sub: DeleteAllPolicies) -> int:
        async with async_db_session.begin() as db:
            count = await CasbinDao.delete_policies_by_sub(db, sub)
        return count

    @staticmethod
    async def get_group_list():
        enforcer = await RBAC.enforcer()
        data = enforcer.get_grouping_policy()
        return data

    @staticmethod
    async def create_group(*, g: CreateUserRole):
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_grouping_policy(g.uuid, g.role)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def create_groups(*, gs: list[CreateUserRole]):
        enforcer = await RBAC.enforcer()
        data = await enforcer.add_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def delete_group(*, g: DeleteUserRole):
        enforcer = await RBAC.enforcer()
        _g = enforcer.has_grouping_policy(g.uuid, g.role)
        if not _g:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_grouping_policy(g.uuid, g.role)
        return data

    @staticmethod
    async def delete_groups(*, gs: list[DeleteUserRole]):
        enforcer = await RBAC.enforcer()
        data = await enforcer.remove_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    @staticmethod
    async def delete_all_groups(*, uuid: str) -> int:
        async with async_db_session.begin() as db:
            count = await CasbinDao.delete_groups_by_uuid(db, uuid)
        return count
