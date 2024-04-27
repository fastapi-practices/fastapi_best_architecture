#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID

from sqlalchemy import Select, and_, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import CasbinRule
from backend.app.admin.schema.casbin_rule import DeleteAllPoliciesParam


class CRUDCasbin(CRUDPlus[CasbinRule]):
    async def get_list(self, ptype: str, sub: str) -> Select:
        """
        获取策略列表

        :param ptype:
        :param sub:
        :return:
        """
        se = select(self.model).order_by(self.model.id.desc())
        where_list = []
        if ptype:
            where_list.append(self.model.ptype == ptype)
        if sub:
            where_list.append(self.model.v0.like(f'%{sub}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def delete_policies_by_sub(self, db: AsyncSession, sub: DeleteAllPoliciesParam) -> int:
        """
        删除角色所有P策略

        :param db:
        :param sub:
        :return:
        """
        where_list = []
        if sub.uuid:
            where_list.append(self.model.v0 == sub.uuid)
        where_list.append(self.model.v0 == sub.role)
        result = await db.execute(delete(self.model).where(or_(*where_list)))
        return result.rowcount

    async def delete_groups_by_uuid(self, db: AsyncSession, uuid: UUID) -> int:
        """
        删除用户所有G策略

        :param db:
        :param uuid:
        :return:
        """
        result = await db.execute(delete(self.model).where(self.model.v0 == str(uuid)))
        return result.rowcount


casbin_dao: CRUDCasbin = CRUDCasbin(CasbinRule)
