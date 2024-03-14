#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fast_captcha import text_captcha
from fastapi import BackgroundTasks, Request

from backend.app.common import jwt
from backend.app.common.enums import LoginLogStatusType, UserSocialType
from backend.app.common.exception.errors import AuthorizationError
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_user import user_dao
from backend.app.crud.crud_user_social import user_social_dao
from backend.app.database.db_mysql import async_db_session
from backend.app.schemas.token import GetLoginToken
from backend.app.schemas.user import RegisterUserParam
from backend.app.schemas.user_social import CreateUserSocialParam
from backend.app.services.login_log_service import LoginLogService
from backend.app.utils.timezone import timezone


class GithubService:
    @staticmethod
    async def add_with_login(request: Request, background_tasks: BackgroundTasks, user: dict) -> GetLoginToken | None:
        async with async_db_session.begin() as db:
            email = user['email']
            if not email:
                raise AuthorizationError(msg='授权失败，GitHub 账户未绑定邮箱')
            username = user['login']
            nickname = user['name']
            sys_user = await user_dao.get_by_username(db, username)
            if sys_user:
                username = f'{username}{text_captcha(5)}'
            sys_user = await user_dao.get_by_nickname(db, nickname)
            if sys_user:
                nickname = f'{nickname}{text_captcha(5)}'
            sys_user = await user_dao.check_email(db, email)
            # 创建系统用户
            if not sys_user:
                new_sys_user = RegisterUserParam(username=username, password=None, nickname=nickname, email=email)
                await user_dao.create(db, new_sys_user)
            sys_user = await user_dao.get_by_username(db, username)
            # 绑定社交用户
            new_social_user = CreateUserSocialParam(source=UserSocialType.github, uid=user['id'], user_id=sys_user.id)
            await user_social_dao.create(db, new_social_user)
            # 创建 token
            access_token, access_token_expire_time = await jwt.create_access_token(
                str(sys_user.id), multi_login=sys_user.is_multi_login
            )
            refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                str(sys_user.id), access_token_expire_time, multi_login=sys_user.is_multi_login
            )
            await user_dao.update_login_time(db, sys_user.username)
            sys_user = await user_dao.get_by_username(db, sys_user.username)
            login_log = dict(
                db=db,
                request=request,
                user=user,
                login_time=timezone.now(),
                status=LoginLogStatusType.success.value,
                msg='登录成功（OAuth2）',
            )
            background_tasks.add_task(LoginLogService.create, **login_log)
            await redis_client.delete(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
            data = GetLoginToken(
                access_token=access_token,
                refresh_token=refresh_token,
                access_token_expire_time=access_token_expire_time,
                refresh_token_expire_time=refresh_token_expire_time,
                user=sys_user,  # type: ignore
            )
            return data


github_service: GithubService = GithubService()
