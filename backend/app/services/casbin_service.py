#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.common.casbin_rbac import RbacEnforcer
from backend.app.common.exception import errors
from backend.app.crud.crud_casbin import CasbinDao
from backend.app.schemas.casbin_rule import CreatePolicy, UpdatePolicy, DeletePolicy, CreateUserRole, DeleteUserRole


class CasbinService:

    @staticmethod
    async def get_casbin_list(*, ptype: str, sub: str) -> Select:
        return await CasbinDao.get_all_policy(ptype, sub)

    @staticmethod
    async def get_policy_list():
        data = await RbacEnforcer.get_policy()
        return data

    @staticmethod
    async def create_policy(*, p: CreatePolicy):
        data = await RbacEnforcer.add_policy(p.sub, p.path, p.method)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def update_policy(*, old: UpdatePolicy, new: UpdatePolicy):
        _p = await RbacEnforcer.has_named_policy('p', old.sub, old.path, old.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await RbacEnforcer.update_policy([old.sub, old.path, old.method], [new.sub, new.path, new.method])
        return data

    @staticmethod
    async def delete_policy(*, p: DeletePolicy):
        _p = await RbacEnforcer.has_named_policy('p', p.sub, p.path, p.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await RbacEnforcer.remove_policy(p.sub, p.path, p.method)
        return data

    @staticmethod
    async def get_group_list():
        data = await RbacEnforcer.get_grouping_policy()
        return data

    @staticmethod
    async def create_group(*, g: CreateUserRole):
        data = await RbacEnforcer.add_grouping_policy(g.uuid, g.role)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def delete_group(*, g: DeleteUserRole):
        _g = await RbacEnforcer.has_named_grouping_policy('g', g.uuid, g.role)
        if not _g:
            raise errors.NotFoundError(msg='权限不存在')
        data = await RbacEnforcer.remove_grouping_policy(g.uuid, g.role)
        return data
