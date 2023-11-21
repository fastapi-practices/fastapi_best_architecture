#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.log.login_log import router as login_log
from backend.app.api.v1.log.opera_log import router as opera_log

router = APIRouter()

router.include_router(login_log, prefix='/login')
router.include_router(opera_log, prefix='/opera')
