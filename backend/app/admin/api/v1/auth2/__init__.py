#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.auth2.github import router as github_router

router = APIRouter(prefix='/auth2')

router.include_router(github_router, prefix='/github', tags=['OAuth2'])
