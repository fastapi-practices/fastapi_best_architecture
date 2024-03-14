#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi_oauth20 import FastAPIOAuth20, GitHubOAuth20

from app.services.github_service import github_service
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.core.conf import settings

router = APIRouter()

github_client = GitHubOAuth20(settings.OAUTH2_GITHUB_CLIENT_ID, settings.OAUTH2_GITHUB_CLIENT_SECRET)
github_oauth2 = FastAPIOAuth20(github_client, settings.OAUTH2_GITHUB_REDIRECT_URI)


@router.get('/github', summary='获取 Github 授权链接')
async def auth_github() -> ResponseModel:
    auth_url = await github_client.get_authorization_url(redirect_uri=settings.OAUTH2_GITHUB_REDIRECT_URI)
    return await response_base.success(data=auth_url)


@router.get(
    '/github/callback',
    summary='Github 授权重定向',
    description='Github 授权后，自动重定向到当前地址并获取用户信息，通过用户信息自动创建系统用户',
)
async def login_github(
    request: Request, background_tasks: BackgroundTasks, oauth: FastAPIOAuth20 = Depends(github_oauth2)
) -> ResponseModel:
    token, state = oauth
    access_token = token['access_token']
    user = await github_client.get_userinfo(access_token)
    data = await github_service.add_with_login(request, background_tasks, user)
    return await response_base.success(data=data)
