#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import Depends, Request, Query
from fastapi.security import OAuth2PasswordRequestForm
from starlette.background import BackgroundTasks

from backend.app.common.response.response_schema import response_base
from backend.app.schemas.token import GetLoginToken, GetSwaggerToken, GetNewToken
from backend.app.schemas.user import Auth
from backend.app.services.auth_service import AuthService


async def swagger_user_login(form_data: OAuth2PasswordRequestForm = Depends()) -> GetSwaggerToken:
    """swagger 表单登录"""
    token, user = await AuthService().swagger_login(form_data=form_data)
    return GetSwaggerToken(access_token=token, user=user)


async def user_login(request: Request, obj: Auth, background_tasks: BackgroundTasks):
    """用户登录"""
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


async def create_new_token(refresh_token: Annotated[str, Query(...)]):
    """创建新 token"""
    access_token, access_expire = await AuthService.new_token(refresh_token=refresh_token)
    data = GetNewToken(access_token=access_token, access_token_expire_time=access_expire)
    return await response_base.success(data=data)


async def user_logout(request: Request):
    """用户登出"""
    await AuthService.logout(request=request)
    return await response_base.success()
