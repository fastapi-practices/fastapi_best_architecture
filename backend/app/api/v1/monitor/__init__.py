#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1.monitor.redis import router as redis_router
from backend.app.api.v1.monitor.server import router as server_router

router = APIRouter()

router.include_router(redis_router)
router.include_router(server_router)
