from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from fastapi_oauth20 import FastAPIOAuth20, GitHubOAuth20
from pyrate_limiter import Duration, Rate
from starlette.responses import RedirectResponse

from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.core.conf import settings
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.oauth2.enums import UserSocialType
from backend.plugin.oauth2.service.oauth2_service import oauth2_service
from backend.utils.limiter import RateLimiter

router = APIRouter()

github_client = GitHubOAuth20(settings.OAUTH2_GITHUB_CLIENT_ID, settings.OAUTH2_GITHUB_CLIENT_SECRET)


@router.get('', summary='获取 Github 授权链接')
async def get_github_oauth2_url(db: CurrentSession, request: Request) -> ResponseSchemaModel[str]:
    auth_url = await oauth2_service.get_login_auth_url(db=db, request=request, source=UserSocialType.github)
    return response_base.success(data=auth_url)


@router.get(
    '/callback',
    summary='Github 授权自动重定向',
    description='Github 授权后，自动重定向到当前地址并获取用户信息，通过用户信息自动创建系统用户',
    dependencies=[Depends(RateLimiter(Rate(5, Duration.MINUTE)))],
)
async def github_oauth2_callback(  # noqa: ANN201
    db: CurrentSessionTransaction,
    response: Response,
    background_tasks: BackgroundTasks,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(github_client, redirect_uri=settings.OAUTH2_GITHUB_REDIRECT_URI)),
    ],
):
    token_data, state = oauth2
    access_token = token_data['access_token']
    user = await github_client.get_userinfo(access_token)
    data = await oauth2_service.login_or_binding(
        db=db,
        response=response,
        background_tasks=background_tasks,
        user=user,
        social=UserSocialType.github,
        state=state,
    )

    # 绑定流程
    if data is None:
        return RedirectResponse(url=settings.OAUTH2_FRONTEND_BINDING_REDIRECT_URI)

    # 登录流程
    return RedirectResponse(
        url=f'{settings.OAUTH2_FRONTEND_LOGIN_REDIRECT_URI}?access_token={data.access_token}&session_uuid={data.session_uuid}',
    )
