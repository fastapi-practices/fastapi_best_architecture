#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.common.jwt import DependsUser
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.token import Token
from backend.app.schemas.user import Auth
from backend.app.services.user_service import UserService

router = APIRouter()


@router.post('/swagger_login', summary='swagger 表单登录', description='form 格式登录，仅用于 swagger 文档调试接口')
async def swagger_user_login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    token, user = await UserService.swagger_login(form_data)
    return Token(access_token=token, user=user)


@router.post('/login', summary='用户登录', description='json 格式登录, 仅支持在第三方api工具调试接口, 例如: postman')
async def user_login(obj: Auth):
    token, user = await UserService.login(obj)
    # TODO: token 存储
    data = Token(access_token=token, user=user)
    return response_base.success(data=data)


@router.post('/logout', summary='用户登出', dependencies=[DependsUser])
async def user_logout():
    # TODO: 加入 token 黑名单
    return response_base.success()
