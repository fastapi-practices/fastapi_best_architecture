#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPBasicCredentials
from fastapi_limiter.depends import RateLimiter
from starlette.background import BackgroundTasks

from backend.app.admin.schema.token import GetSwaggerToken
from backend.app.admin.schema.user import AuthLoginParam
from backend.app.admin.service.auth_service import auth_service
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth

router = APIRouter()


@router.post('/login/swagger', summary='swagger 调试专用', description='用于快捷获取 token 进行 swagger 认证')
async def swagger_login(obj: Annotated[HTTPBasicCredentials, Depends()]) -> GetSwaggerToken:
    token, user = await auth_service.swagger_login(obj=obj)
    return GetSwaggerToken(access_token=token, user=user)  # type: ignore


@router.post(
    '/login',
    summary='用户登录',
    description='json 格式登录, 仅支持在第三方api工具调试, 例如: postman',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def user_login(request: Request, obj: AuthLoginParam, background_tasks: BackgroundTasks) -> ResponseModel:
    data = await auth_service.login(request=request, obj=obj, background_tasks=background_tasks)
    return await response_base.success(data=data)


@router.post('/token/new', summary='创建新 token', dependencies=[DependsJwtAuth])
async def create_new_token(request: Request, refresh_token: Annotated[str, Query(...)]) -> ResponseModel:
    data = await auth_service.new_token(request=request, refresh_token=refresh_token)
    return await response_base.success(data=data)


@router.post('/logout', summary='用户登出', dependencies=[DependsJwtAuth])
async def user_logout(request: Request) -> ResponseModel:
    await auth_service.logout(request=request)
    return await response_base.success()
