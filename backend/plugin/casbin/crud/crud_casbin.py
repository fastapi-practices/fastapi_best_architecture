#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.casbin.model import CasbinRule
from backend.plugin.casbin.schema.casbin_rule import DeleteAllPoliciesParam


class CRUDCasbin(CRUDPlus[CasbinRule]):
    async def get_list(self, ptype: str, sub: str) -> Select:
        """
        获取策略列表

        :param ptype:
        :param sub:
        :return:
        """
        return await self.select_order('id', 'desc', ptype=ptype, v0__like=f'%{sub}%')

    async def delete_policies_by_sub(self, db: AsyncSession, sub: DeleteAllPoliciesParam) -> int:
        """
        删除角色所有P策略

        :param db:
        :param sub:
        :return:
        """
        where_list = [sub.role]
        if sub.uuid:
            where_list.append(sub.uuid)
        return await self.delete_model_by_column(db, allow_multiple=True, v0__mor={'eq': where_list})

    async def delete_groups_by_uuid(self, db: AsyncSession, uuid: UUID) -> int:
        """
        删除用户所有G策略

        :param db:
        :param uuid:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, v0=str(uuid))


casbin_dao: CRUDCasbin = CRUDCasbin(CasbinRule)
