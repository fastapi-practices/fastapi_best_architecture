#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, and_, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.base import CRUDBase
from backend.app.models import CasbinRule
from backend.app.schemas.casbin_rule import CreatePolicy, DeleteAllPolicies, UpdatePolicy


class CRUDCasbin(CRUDBase[CasbinRule, CreatePolicy, UpdatePolicy]):
    async def get_all_policy(self, ptype: str, sub: str) -> Select:
        se = select(self.model).order_by(self.model.id)
        where_list = []
        if ptype:
            where_list.append(self.model.ptype == ptype)
        if sub:
            where_list.append(self.model.v0.like(f'%{sub}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def delete_policies_by_sub(self, db: AsyncSession, sub: DeleteAllPolicies) -> int:
        where_list = []
        if sub.uuid:
            where_list.append(self.model.v0 == sub.uuid)
        where_list.append(self.model.v0 == sub.role)
        result = await db.execute(delete(self.model).where(or_(*where_list)))
        return result.rowcount

    async def delete_groups_by_uuid(self, db: AsyncSession, uuid: str) -> int:
        result = await db.execute(delete(self.model).where(self.model.v0 == uuid))
        return result.rowcount


CasbinDao: CRUDCasbin = CRUDCasbin(CasbinRule)
