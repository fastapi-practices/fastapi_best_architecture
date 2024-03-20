#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fast_captcha import text_captcha
from fastapi import BackgroundTasks, Request

from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.crud.crud_user_social import user_social_dao
from backend.app.admin.schema.token import GetLoginToken
from backend.app.admin.schema.user import RegisterUserParam
from backend.app.admin.schema.user_social import CreateUserSocialParam
from backend.app.admin.service.login_log_service import LoginLogService
from backend.common.enums import LoginLogStatusType, UserSocialType
from backend.common.exception.errors import AuthorizationError
from backend.common.security import jwt
from backend.database.db_mysql import async_db_session
from backend.database.db_redis import redis_client
from backend.utils.timezone import timezone


class GithubService:
    @staticmethod
    async def create_with_login(
        request: Request, background_tasks: BackgroundTasks, user: dict
    ) -> GetLoginToken | None:
        async with async_db_session.begin() as db:
            github_email = user['email']
            if not github_email:
                raise AuthorizationError(msg='授权失败，GitHub 账户未绑定邮箱')
            github_id = user['id']
            github_username = user['login']
            github_nickname = user['name']
            sys_user = await user_dao.check_email(db, github_email)
            if not sys_user:
                # 创建系统用户
                sys_user = await user_dao.get_by_username(db, github_username)
                if sys_user:
                    github_username = f'{github_username}{text_captcha(5)}'
                sys_user = await user_dao.get_by_nickname(db, github_nickname)
                if sys_user:
                    github_nickname = f'{github_nickname}{text_captcha(5)}'
                new_sys_user = RegisterUserParam(
                    username=github_username, password=None, nickname=github_nickname, email=github_email
                )
                await user_dao.create(db, new_sys_user, social=True)
                await db.flush()
                sys_user = await user_dao.check_email(db, github_email)
            # 绑定社交用户
            user_social = await user_social_dao.get(db, sys_user.id, UserSocialType.github)
            if not user_social:
                new_user_social = CreateUserSocialParam(
                    source=UserSocialType.github, uid=str(github_id), user_id=sys_user.id
                )
                await user_social_dao.create(db, new_user_social)
            # 创建 token
            access_token, access_token_expire_time = await jwt.create_access_token(
                str(sys_user.id), multi_login=sys_user.is_multi_login
            )
            refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                str(sys_user.id), access_token_expire_time, multi_login=sys_user.is_multi_login
            )
            await user_dao.update_login_time(db, sys_user.username)
            await db.refresh(sys_user)
            login_log = dict(
                db=db,
                request=request,
                user=sys_user,
                login_time=timezone.now(),
                status=LoginLogStatusType.success.value,
                msg='登录成功（OAuth2）',
            )
            background_tasks.add_task(LoginLogService.create, **login_log)
            await redis_client.delete(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
            data = GetLoginToken(
                access_token=access_token,
                refresh_token=refresh_token,
                access_token_expire_time=access_token_expire_time,
                refresh_token_expire_time=refresh_token_expire_time,
                user=sys_user,  # type: ignore
            )
            return data


github_service = GithubService()
