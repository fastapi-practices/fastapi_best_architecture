#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.crud.base import CRUDBase
from backend.app.models import Menu
from backend.app.schemas.menu import CreateMenu, UpdateMenu


class CRUDMenu(CRUDBase[Menu, CreateMenu, UpdateMenu]):
    async def get(self, db, menu_id: int) -> Menu | None:
        return await self.get_(db, menu_id)


MenuDao: CRUDMenu = CRUDMenu(Menu)
