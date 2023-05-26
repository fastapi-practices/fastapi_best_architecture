#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.crud.base import CRUDBase
from backend.app.models import Role
from backend.app.schemas.role import CreateRole, UpdateRole


class CRUDRole(CRUDBase[Role, CreateRole, UpdateRole]):
    async def get(self, db, role_id: int):
        return await self.get_(db, role_id)


RoleDao: CRUDRole = CRUDRole(Role)
