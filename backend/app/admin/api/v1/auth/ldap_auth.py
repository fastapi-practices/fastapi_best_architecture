#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import HTTPBasicCredentials

from starlette.background import BackgroundTasks

from backend.app.admin.schema.token import GetLoginToken, GetSwaggerToken
from backend.app.admin.schema.user import AuthLoginParam
from backend.app.admin.service.auth_service import auth_service
from backend.common.response.response_schema import ResponseSchemaModel, response_base


router = APIRouter()

@router.post('/login/ldap_swagger', summary='swagger 调试专用', description='用于快捷获取 token 进行 ldap_swagger 认证')
async def swagger_ldap_login(obj: Annotated[HTTPBasicCredentials, Depends()]) -> GetSwaggerToken:
    token, user = await auth_service.swagger_ldap_login(obj=obj)
    return GetSwaggerToken(access_token=token, user=user)

@router.post('/ldap_login', summary='LDAP登录', description='使用LDAP账号和密码登录系统')
async def ldap_login(
    request: Request, response: Response, obj: AuthLoginParam, background_tasks: BackgroundTasks
) -> ResponseSchemaModel[GetLoginToken]:
    data = await auth_service.ldap_login(request=request, response=response, obj=obj, background_tasks=background_tasks)
    return response_base.success(data=data)
