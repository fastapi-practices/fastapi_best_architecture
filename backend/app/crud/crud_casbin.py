#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, select, and_

from backend.app.crud.base import CRUDBase
from backend.app.models import CasbinRule
from backend.app.schemas.casbin_rule import CreatePolicy, UpdatePolicy


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


CasbinDao: CRUDCasbin = CRUDCasbin(CasbinRule)
