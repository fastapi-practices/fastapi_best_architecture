#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from starlette.background import BackgroundTasks

from backend.app.common.jwt import get_token, jwt_decode, DependsJwtAuth
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.token import RefreshToken, LoginToken, SwaggerToken, RefreshTokenTime
from backend.app.schemas.user import Auth
from backend.app.services.user_service import UserService

router = APIRouter()


@router.post('/swagger_login', summary='swagger 表单登录', description='form 格式登录，仅用于 swagger 文档调试接口')
async def swagger_user_login(form_data: OAuth2PasswordRequestForm = Depends()) -> SwaggerToken:
    token, user = await UserService().swagger_login(form_data)
    return SwaggerToken(access_token=token, user=user)


@router.post(
    '/login',
    summary='用户登录',
    description='json 格式登录, 仅支持在第三方api工具调试接口, 例如: postman',
    dependencies=[Depends(RateLimiter(times=5, minutes=15))],
)
async def user_login(request: Request, obj: Auth, background_tasks: BackgroundTasks):
    access_token, refresh_token, access_expire, refresh_expire, user = await UserService().login(
        request=request, obj=obj, background_tasks=background_tasks
    )
    data = LoginToken(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expire_time=access_expire,
        refresh_token_expire_time=refresh_expire,
        user=user,
    )
    return response_base.success(data=data)


@router.post('/refresh_token', summary='刷新 token', dependencies=[DependsJwtAuth])
async def get_refresh_token(request: Request, custom_time: RefreshTokenTime):
    token = get_token(request)
    user_id, _ = jwt_decode(token)
    refresh_token, refresh_expire = await UserService.refresh_token(user_id=user_id, custom_time=custom_time)
    data = RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=refresh_expire)
    return response_base.success(data=data)


@router.post('/logout', summary='用户登出', dependencies=[DependsJwtAuth])
async def user_logout(request: Request):
    await UserService.logout(request.user.id)
    return response_base.success()
