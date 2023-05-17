#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.crud.base import CRUDBase
from backend.app.models import Dept
from backend.app.schemas.dept import CreateDept, UpdateDept


class CRUDDept(CRUDBase[Dept, CreateDept, UpdateDept]):

    async def get_dept_by_id(self, db, dept_id):
        return await self.get(db, dept_id)


DeptDao: CRUDDept = CRUDDept(Dept)
