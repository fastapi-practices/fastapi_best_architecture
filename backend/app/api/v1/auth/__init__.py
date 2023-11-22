#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.auth.auth import router as auth_router
from backend.app.api.v1.auth.captcha import router as captcha_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(captcha_router)
