#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.common.jwt import DependsUser
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.token import Token
from backend.app.services.user_service import UserService

router = APIRouter()


@router.post('/login', summary='表单登录', description='form 格式登录，支持直接在 api 文档调试接口')
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    token, user = await UserService.login(form_data)
    data = Token(access_token=token, user=user)
    return response_base.response_200(data=data)


# @router.post('/login', summary='用户登录', description='json 格式登录, 仅支持在第三方api工具调试接口, 例如: postman')
# async def user_login(obj: Auth):
#     token, user = await UserService.login(obj)
#     data = Token(access_token=token, user=user)
#     return response_base.response_200(data=data)


@router.post('/logout', summary='用户登出', dependencies=[DependsUser])
async def user_logout():
    return response_base.response_200()
