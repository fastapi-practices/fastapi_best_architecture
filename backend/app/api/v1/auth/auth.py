#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from starlette.background import BackgroundTasks

from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.token import GetLoginToken, GetSwaggerToken, GetNewToken
from backend.app.schemas.user import AuthLogin
from backend.app.services.auth_service import AuthService

router = APIRouter()


@router.post('/swagger_login', summary='swagger 表单登录', description='form 格式登录，仅用于 swagger 文档调试接口')
async def swagger_user_login(form_data: OAuth2PasswordRequestForm = Depends()) -> GetSwaggerToken:
    token, user = await AuthService().swagger_login(form_data=form_data)
    return GetSwaggerToken(access_token=token, user=user)


@router.post(
    '/login',
    summary='用户登录',
    description='json 格式登录, 仅支持在第三方api工具调试接口, 例如: postman',
    dependencies=[Depends(RateLimiter(times=5, minutes=15))],
)
async def user_login(request: Request, obj: AuthLogin, background_tasks: BackgroundTasks):
    access_token, refresh_token, access_expire, refresh_expire, user = await AuthService().login(
        request=request, obj=obj, background_tasks=background_tasks
    )
    data = GetLoginToken(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expire_time=access_expire,
        refresh_token_expire_time=refresh_expire,
        user=user,
    )
    return await response_base.success(data=data)


@router.post('/new_token', summary='创建新 token', dependencies=[DependsJwtAuth])
async def create_new_token(refresh_token: Annotated[str, Query(...)]):
    access_token, access_expire = await AuthService.new_token(refresh_token=refresh_token)
    data = GetNewToken(access_token=access_token, access_token_expire_time=access_expire)
    return await response_base.success(data=data)


@router.post('/logout', summary='用户登出', dependencies=[DependsJwtAuth])
async def user_logout(request: Request):
    await AuthService.logout(request=request)
    return await response_base.success()
