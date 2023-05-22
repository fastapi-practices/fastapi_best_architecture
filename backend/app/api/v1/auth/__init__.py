#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter
from backend.app.api.v1.auth.auth import router as auth_router

router = APIRouter(prefix='/auth', tags=['认证'])

router.include_router(auth_router)
