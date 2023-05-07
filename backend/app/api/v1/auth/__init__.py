#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter
from backend.app.api.v1.auth.user import router as user_router

router = APIRouter(prefix='/auth', tags=['用户管理'])

router.include_router(user_router, prefix='/users')
