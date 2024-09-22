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
from backend.app.admin.service.login_log_service import LoginLogService
from backend.common.enums import LoginLogStatusType, UserSocialType
from backend.common.exception.errors import AuthorizationError
from backend.common.security import jwt
from backend.core.conf import settings
from backend.database.db_mysql import async_db_session
from backend.database.db_redis import redis_client
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
            _id = user.get('id')
            _username = user.get('username')
            if social == UserSocialType.github:
                _username = user.get('login')
            _nickname = user.get('name')
            _email = user.get('email')
            if social == UserSocialType.linuxdo:
                _email = f'{_username}@linux.do'
            if not _email:
                raise AuthorizationError(msg=f'授权失败，{social.value} 账户未绑定邮箱')
            # 创建系统用户
            sys_user = await user_dao.check_email(db, _email)
            if not sys_user:
                sys_user = await user_dao.get_by_username(db, _username)
                if sys_user:
                    _username = f'{_username}#{text_captcha(5)}'
                sys_user = await user_dao.get_by_nickname(db, _nickname)
                if sys_user:
                    _nickname = f'{_nickname}#{text_captcha(5)}'
                new_sys_user = RegisterUserParam(username=_username, password=None, nickname=_nickname, email=_email)
                await user_dao.create(db, new_sys_user, social=True)
                await db.flush()
                sys_user = await user_dao.check_email(db, _email)
            # 绑定社交用户
            sys_user_id = sys_user.id
            user_social = await user_social_dao.get(db, sys_user_id, social.value)
            if not user_social:
                new_user_social = CreateUserSocialParam(source=social.value, uid=str(_id), user_id=sys_user_id)
                await user_social_dao.create(db, new_user_social)
            # 创建 token
            access_token = await jwt.create_access_token(str(sys_user_id), sys_user.is_multi_login)
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
            background_tasks.add_task(LoginLogService.create, **login_log)
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
            )
            return data


oauth2_service = OAuth2Service()
