#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.crud.base import CRUDBase
from backend.app.models import Api
from backend.app.schemas.api import CreateApi, UpdateApi


class CRUDApi(CRUDBase[Api, CreateApi, UpdateApi]):
    # TODO: 添加 api 相关数据库操作
    pass


ApiDao: CRUDApi = CRUDApi(Api)
