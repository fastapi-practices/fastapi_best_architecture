#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi_oauth20 import FastAPIOAuth20, GitHubOAuth20

from backend.app.admin.conf import admin_settings
from backend.app.admin.service.github_service import github_service
from backend.common.response.response_schema import ResponseModel, response_base

router = APIRouter()

github_client = GitHubOAuth20(admin_settings.OAUTH2_GITHUB_CLIENT_ID, admin_settings.OAUTH2_GITHUB_CLIENT_SECRET)
github_oauth2 = FastAPIOAuth20(github_client, admin_settings.OAUTH2_GITHUB_REDIRECT_URI)


@router.get('', summary='获取 Github 授权链接')
async def github_auth2() -> ResponseModel:
    auth_url = await github_client.get_authorization_url(redirect_uri=admin_settings.OAUTH2_GITHUB_REDIRECT_URI)
    return await response_base.success(data=auth_url)


@router.get(
    '/callback',
    summary='Github 授权重定向',
    description='Github 授权后，自动重定向到当前地址并获取用户信息，通过用户信息自动创建系统用户',
    response_model=None,
)
async def github_login(
    request: Request, background_tasks: BackgroundTasks, oauth: FastAPIOAuth20 = Depends(github_oauth2)
) -> ResponseModel:
    token, _state = oauth
    access_token = token['access_token']
    user = await github_client.get_userinfo(access_token)
    data = await github_service.create_with_login(request, background_tasks, user)
    return await response_base.success(data=data)
