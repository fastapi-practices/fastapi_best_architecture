#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.casbin.crud.crud_casbin import casbin_dao
from backend.plugin.casbin.schema.casbin_rule import (
    CreateGroupParam,
    CreatePolicyParam,
    DeleteAllPoliciesParam,
    DeleteGroupParam,
    DeletePolicyParam,
    UpdatePoliciesParam,
    UpdatePolicyParam,
)
from backend.plugin.casbin.utils.rbac import casbin_enforcer


class CasbinService:
    """Casbin 权限服务类"""

    @staticmethod
    async def get_casbin_list(*, ptype: str, sub: str) -> Select:
        """
        获取 Casbin 规则列表

        :param ptype: 策略类型
        :param sub: 用户 UUID / 角色 ID
        :return:
        """
        return await casbin_dao.get_list(ptype, sub)

    @staticmethod
    async def get_policy_list(*, role: int | None = None) -> list:
        """
        获取 P 策略列表

        :param role: 角色ID
        :return:
        """
        enforcer = await casbin_enforcer()
        if role is not None:
            data = enforcer.get_filtered_named_policy('p', 0, str(role))
        else:
            data = enforcer.get_policy()
        return data

    @staticmethod
    async def create_policy(*, p: CreatePolicyParam) -> bool:
        """
        创建 P 策略

        :param p: 策略参数
        :return:
        """
        enforcer = await casbin_enforcer()
        data = await enforcer.add_policy(p.sub, p.path, p.method)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def create_policies(*, ps: list[CreatePolicyParam]) -> bool:
        """
        批量创建 P 策略

        :param ps: 策略参数列表
        :return:
        """
        enforcer = await casbin_enforcer()
        data = await enforcer.add_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def update_policy(*, obj: UpdatePolicyParam) -> bool:
        """
        更新 P 策略

        :param obj: 更新 P 策略参数
        :return:
        """
        old_obj = obj.old
        new_obj = obj.new
        enforcer = await casbin_enforcer()
        _p = enforcer.has_policy(old_obj.sub, old_obj.path, old_obj.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.update_policy(
            [old_obj.sub, old_obj.path, old_obj.method],
            [new_obj.sub, new_obj.path, new_obj.method],
        )
        return data

    @staticmethod
    async def update_policies(*, obj: UpdatePoliciesParam) -> bool:
        """
        批量更新 P 策略

        :param obj: 更新 P 策略参数
        :return:
        """
        enforcer = await casbin_enforcer()
        data = await enforcer.update_policies(
            [list(o.model_dump().values()) for o in obj.old],
            [list(n.model_dump().values()) for n in obj.new],
        )
        return data

    @staticmethod
    async def delete_policy(*, p: DeletePolicyParam) -> bool:
        """
        删除 P 策略

        :param p: 删除参数
        :return:
        """
        enforcer = await casbin_enforcer()
        _p = enforcer.has_policy(p.sub, p.path, p.method)
        if not _p:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_policy(p.sub, p.path, p.method)
        return data

    @staticmethod
    async def delete_policies(*, ps: list[DeletePolicyParam]) -> bool:
        """
        批量删除 P 策略

        :param ps: 删除参数列表
        :return:
        """
        enforcer = await casbin_enforcer()
        data = await enforcer.remove_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    @staticmethod
    async def delete_all_policies(*, sub: DeleteAllPoliciesParam) -> int:
        """
        删除所有 P 策略

        :param sub: 删除参数
        :return:
        """
        async with async_db_session.begin() as db:
            count = await casbin_dao.delete_policies_by_sub(db, sub)
        return count

    @staticmethod
    async def get_group_list() -> list:
        """获取 G 策略列表"""
        enforcer = await casbin_enforcer()
        data = enforcer.get_grouping_policy()
        return data

    @staticmethod
    async def create_group(*, g: CreateGroupParam) -> bool:
        """
        创建 G 策略

        :param g: 创建 G 策略参数
        :return:
        """
        enforcer = await casbin_enforcer()
        data = await enforcer.add_grouping_policy(g.uuid, g.role)
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def create_groups(*, gs: list[CreateGroupParam]) -> bool:
        """
        批量创建 G 策略

        :param gs: 创建参数列表
        :return:
        """
        enforcer = await casbin_enforcer()
        data = await enforcer.add_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.ForbiddenError(msg='权限已存在')
        return data

    @staticmethod
    async def delete_group(*, g: DeleteGroupParam) -> bool:
        """
        删除 G 策略

        :param g: 删除参数
        :return:
        """
        enforcer = await casbin_enforcer()
        _g = enforcer.has_grouping_policy(g.uuid, g.role)
        if not _g:
            raise errors.NotFoundError(msg='权限不存在')
        data = await enforcer.remove_grouping_policy(g.uuid, g.role)
        return data

    @staticmethod
    async def delete_groups(*, gs: list[DeleteGroupParam]) -> bool:
        """
        批量删除 G 策略

        :param gs: 删除参数列表
        :return: 是否成功
        """
        enforcer = await casbin_enforcer()
        data = await enforcer.remove_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.NotFoundError(msg='权限不存在')
        return data

    @staticmethod
    async def delete_all_groups(*, uuid: UUID) -> int:
        """
        删除所有 G 策略

        :param uuid: 用户uuid
        :return: 删除数量
        """
        async with async_db_session.begin() as db:
            count = await casbin_dao.delete_groups_by_uuid(db, uuid)
        return count


casbin_service: CasbinService = CasbinService()
