#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.casbin.crud.crud_casbin import casbin_dao
from backend.plugin.casbin.schema.casbin_rule import (
    CreatePolicyParam,
    CreateUserRoleParam,
    DeleteAllPoliciesParam,
    DeletePolicyParam,
    DeleteUserRoleParam,
    UpdatePoliciesParam,
    UpdatePolicyParam,
)
from backend.plugin.casbin.utils.rbac import casbin_enforcer


class CasbinService:
    @staticmethod
    async def get_casbin_list(*, ptype: str, sub: str) -> Select:
        return await casbin_dao.get_list(ptype, sub)

    @staticmethod
    async def get_policy_list(*, role: int | None = None) -> list:
        enforcer = await casbin_enforcer()
        if role is not None:
            data = enforcer.get_filtered_named_policy('p', 0, str(role))
        else:
            data = enforcer.get_policy()
        return data

    @staticmethod
    async def create_policy(*, p: CreatePolicyParam) -> bool:
        enforcer = await casbin_enforcer()
        data = await enforcer.add_policy(p.sub, p.path, p.method)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def create_policies(*, ps: list[CreatePolicyParam]) -> bool:
        enforcer = await casbin_enforcer()
        data = await enforcer.add_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def update_policy(*, obj: UpdatePolicyParam) -> bool:
        old_obj = obj.old
        new_obj = obj.new
        enforcer = await casbin_enforcer()
        _p = enforcer.has_policy(old_obj.sub, old_obj.path, old_obj.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.update_policy(
            [old_obj.sub, old_obj.path, old_obj.method], [new_obj.sub, new_obj.path, new_obj.method]
        )
        return data

    @staticmethod
    async def update_policies(*, obj: UpdatePoliciesParam) -> bool:
        enforcer = await casbin_enforcer()
        data = await enforcer.update_policies(
            [list(o.model_dump().values()) for o in obj.old], [list(n.model_dump().values()) for n in obj.new]
        )
        return data

    @staticmethod
    async def delete_policy(*, p: DeletePolicyParam) -> bool:
        enforcer = await casbin_enforcer()
        _p = enforcer.has_policy(p.sub, p.path, p.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_policy(p.sub, p.path, p.method)
        return data

    @staticmethod
    async def delete_policies(*, ps: list[DeletePolicyParam]) -> bool:
        enforcer = await casbin_enforcer()
        data = await enforcer.remove_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    @staticmethod
    async def delete_all_policies(*, sub: DeleteAllPoliciesParam) -> int:
        async with async_db_session.begin() as db:
            count = await casbin_dao.delete_policies_by_sub(db, sub)
        return count

    @staticmethod
    async def get_group_list() -> list:
        enforcer = await casbin_enforcer()
        data = enforcer.get_grouping_policy()
        return data

    @staticmethod
    async def create_group(*, g: CreateUserRoleParam) -> bool:
        enforcer = await casbin_enforcer()
        data = await enforcer.add_grouping_policy(g.uuid, g.role)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def create_groups(*, gs: list[CreateUserRoleParam]) -> bool:
        enforcer = await casbin_enforcer()
        data = await enforcer.add_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def delete_group(*, g: DeleteUserRoleParam) -> bool:
        enforcer = await casbin_enforcer()
        _g = enforcer.has_grouping_policy(g.uuid, g.role)
        if not _g:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_grouping_policy(g.uuid, g.role)
        return data

    @staticmethod
    async def delete_groups(*, gs: list[DeleteUserRoleParam]) -> bool:
        enforcer = await casbin_enforcer()
        data = await enforcer.remove_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    @staticmethod
    async def delete_all_groups(*, uuid: UUID) -> int:
        async with async_db_session.begin() as db:
            count = await casbin_dao.delete_groups_by_uuid(db, uuid)
        return count


casbin_service: CasbinService = CasbinService()
