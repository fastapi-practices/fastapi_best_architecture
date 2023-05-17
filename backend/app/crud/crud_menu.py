#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.crud.base import CRUDBase
from backend.app.models import Menu
from backend.app.schemas.menu import CreateMenu, UpdateMenu


class CRUDMenu(CRUDBase[Menu, CreateMenu, UpdateMenu]):
    # TODO: 添加 menu 相关数据库操作
    pass



MenuDao: CRUDMenu = CRUDMenu(Menu)
