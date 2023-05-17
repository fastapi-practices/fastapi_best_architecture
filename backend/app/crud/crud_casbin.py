#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.crud.base import CRUDBase
from backend.app.models import CasbinRule
from backend.app.schemas.casbin_rule import CreatePolicy, UpdatePolicy


class CRUDCasbin(CRUDBase[CasbinRule, CreatePolicy, UpdatePolicy]):
    # TODO: 添加 casbin 相关数据库操作
    pass


CasbinDao: CRUDCasbin = CRUDCasbin(CasbinRule)
