#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.crud.base import CRUDBase
from backend.app.models import Dept
from backend.app.schemas.dept import CreateDept, UpdateDept


class CRUDDept(CRUDBase[Dept, CreateDept, UpdateDept]):
    async def get(self, db, dept_id: int):
        return await self.get_(db, dept_id)


DeptDao: CRUDDept = CRUDDept(Dept)
