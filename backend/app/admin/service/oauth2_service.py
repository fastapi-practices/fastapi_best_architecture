#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fast_captcha import text_captcha
from fastapi import BackgroundTasks, Request, Response

from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.crud.crud_user_social import user_social_dao
from backend.app.admin.schema.token import GetLoginToken
from backend.app.admin.schema.user import RegisterUserParam
from backend.app.admin.schema.user_social import CreateUserSocialParam
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.enums import LoginLogStatusType, UserSocialType
from backend.common.exception.errors import AuthorizationError
from backend.common.security import jwt
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


class OAuth2Service:
    @staticmethod
    async def create_with_login(
        *,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
        user: dict,
        social: UserSocialType,
    ) -> GetLoginToken | None:
        async with async_db_session.begin() as db:
            # 获取 OAuth2 平台用户信息
            social_id = user.get('id')
            social_username = user.get('username')
            if social == UserSocialType.github:
                social_username = user.get('login')
            social_nickname = user.get('name')
            social_email = user.get('email')
            if social == UserSocialType.linuxdo:  # 不提供明文邮箱的平台
                social_email = f'{social_username}@linux.do'
            if not social_email:
                raise AuthorizationError(msg=f'授权失败，{social.value} 账户未绑定邮箱')
            # 创建系统用户
            sys_user = await user_dao.check_email(db, social_email)
            if not sys_user:
                sys_user = await user_dao.get_by_username(db, social_username)
                if sys_user:
                    social_username = f'{social_username}#{text_captcha(5)}'
                sys_user = await user_dao.get_by_nickname(db, social_nickname)
                if sys_user:
                    social_username = f'{social_nickname}#{text_captcha(5)}'
                new_sys_user = RegisterUserParam(
                    username=social_username, password=None, nickname=social_username, email=social_email
                )
                await user_dao.create(db, new_sys_user, social=True)
                await db.flush()
                sys_user = await user_dao.check_email(db, social_email)
            # 绑定社交用户
            sys_user_id = sys_user.id
            user_social = await user_social_dao.get(db, sys_user_id, social.value)
            if not user_social:
                new_user_social = CreateUserSocialParam(source=social.value, uid=str(social_id), user_id=sys_user_id)
                await user_social_dao.create(db, new_user_social)
            # 创建 token
            access_token = await jwt.create_access_token(
                str(sys_user_id),
                sys_user.is_multi_login,
                # extra info
                username=sys_user.username,
                nickname=sys_user.nickname,
                last_login_time=timezone.t_str(timezone.now()),
                ip=request.state.ip,
                os=request.state.os,
                browser=request.state.browser,
                device=request.state.device,
            )
            refresh_token = await jwt.create_refresh_token(str(sys_user_id), multi_login=sys_user.is_multi_login)
            await user_dao.update_login_time(db, sys_user.username)
            await db.refresh(sys_user)
            login_log = dict(
                db=db,
                request=request,
                user_uuid=sys_user.uuid,
                username=sys_user.username,
                login_time=timezone.now(),
                status=LoginLogStatusType.success.value,
                msg='登录成功（OAuth2）',
            )
            background_tasks.add_task(login_log_service.create, **login_log)
            await redis_client.delete(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
            response.set_cookie(
                key=settings.COOKIE_REFRESH_TOKEN_KEY,
                value=refresh_token.refresh_token,
                max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                expires=timezone.f_utc(refresh_token.refresh_token_expire_time),
                httponly=True,
            )
            data = GetLoginToken(
                access_token=access_token.access_token,
                access_token_expire_time=access_token.access_token_expire_time,
                user=sys_user,  # type: ignore
                session_uuid=access_token.session_uuid,
            )
            return data


oauth2_service: OAuth2Service = OAuth2Service()
