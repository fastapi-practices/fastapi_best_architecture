#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi_oauth20 import FastAPIOAuth20, GoogleOAuth20

from backend.app.core.conf import settings

router = APIRouter()

google_client = GoogleOAuth20(settings.OAUTH2_GOOGLE_CLIENT_ID, settings.OAUTH2_GOOGLE_CLIENT_SECRET)
google_oauth2 = FastAPIOAuth20(google_client, settings.OAUTH2_GOOGLE_REDIRECT_URI)


@router.get('/google', summary='获取 Google 授权地址')
async def auth_google() -> str:
    return await google_client.get_authorization_url(redirect_uri=settings.OAUTH2_REDIRECT_URI)


@router.post(
    '/login/google',
    summary='谷歌授权重定向地址',
    description='Google 授权后，重定向到当前地址获取 Google 用户信息，通过用户信息自动创建系统用户',
)
async def login_google(oauth: google_oauth2 = Depends()):
    token, state = oauth
    access_token = token['access_token']
    await google_client.get_userinfo(access_token)
    # TODO: 创建系统用户，token，系统 access token
