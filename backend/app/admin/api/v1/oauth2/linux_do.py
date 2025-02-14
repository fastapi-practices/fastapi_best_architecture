#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from fastapi_limiter.depends import RateLimiter
from fastapi_oauth20 import FastAPIOAuth20, LinuxDoOAuth20
from starlette.responses import RedirectResponse

from backend.app.admin.conf import admin_settings
from backend.app.admin.service.oauth2_service import oauth2_service
from backend.common.enums import UserSocialType
from backend.common.response.response_schema import ResponseSchemaModel, response_base

router = APIRouter()

_linux_do_client = LinuxDoOAuth20(
    admin_settings.OAUTH2_LINUX_DO_CLIENT_ID,
    admin_settings.OAUTH2_LINUX_DO_CLIENT_SECRET,
)
_linux_do_oauth2 = FastAPIOAuth20(_linux_do_client, admin_settings.OAUTH2_LINUX_DO_REDIRECT_URI)


@router.get('', summary='获取 Linux Do 授权链接')
async def linux_do_auth2() -> ResponseSchemaModel[str]:
    auth_url = await _linux_do_client.get_authorization_url(redirect_uri=admin_settings.OAUTH2_LINUX_DO_REDIRECT_URI)
    return response_base.success(data=auth_url)


@router.get(
    '/callback',
    summary='Linux Do 授权自动重定向',
    description='Linux Do 授权后，自动重定向到当前地址并获取用户信息，通过用户信息自动创建系统用户',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def linux_do_login(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    oauth2: FastAPIOAuth20 = Depends(_linux_do_oauth2),
):
    token, _state = oauth2
    access_token = token['access_token']
    user = await _linux_do_client.get_userinfo(access_token)
    data = await oauth2_service.create_with_login(
        request=request,
        response=response,
        background_tasks=background_tasks,
        user=user,
        social=UserSocialType.linuxdo,
    )
    return RedirectResponse(url=f'{admin_settings.OAUTH2_FRONTEND_REDIRECT_URI}?access_token={data.access_token}')
