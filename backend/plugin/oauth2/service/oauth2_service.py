#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fast_captcha import text_captcha
from fastapi import BackgroundTasks, Request, Response

from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.schema.token import GetLoginToken
from backend.app.admin.schema.user import AddOAuth2UserParam
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.enums import LoginLogStatusType, UserSocialType
from backend.common.security import jwt
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.plugin.oauth2.crud.crud_user_social import user_social_dao
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam
from backend.utils.timezone import timezone


class OAuth2Service:
    """OAuth2 认证服务类"""

    @staticmethod
    async def create_with_login(
        *,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
        user: dict[str, Any],
        social: UserSocialType,
    ) -> GetLoginToken | None:
        """
        创建 OAuth2 用户并登录

        :param request: FastAPI 请求对象
        :param response: FastAPI 响应对象
        :param background_tasks: FastAPI 后台任务
        :param user: OAuth2 用户信息
        :param social: 社交平台类型
        :return:
        """
        async with async_db_session.begin() as db:
            sid = user.get('uuid')
            username = user.get('username')
            nickname = user.get('nickname')
            email = user.get('email')
            avatar = user.get('avatar_url')

            if social == UserSocialType.github:
                sid = user.get('id')
                username = user.get('login')
                nickname = user.get('name')

            if social == UserSocialType.linux_do:
                sid = user.get('id')
                nickname = user.get('name')

            sys_user = None
            user_social = await user_social_dao.get_by_sid(db, str(sid), str(social.value))
            if not user_social:
                if email:
                    sys_user = await user_dao.check_email(db, email)

                    # 创建系统用户
                    if not sys_user:
                        while await user_dao.get_by_username(db, username):
                            username = f'{username}_{text_captcha(5)}'
                        new_sys_user = AddOAuth2UserParam(
                            username=username,
                            password='123456',  # 默认密码，可修改系统用户表进行默认密码检测并配合前端进行修改密码提示
                            nickname=nickname,
                            email=email,
                            avatar=avatar,
                        )
                        await user_dao.add_by_oauth2(db, new_sys_user)
                        await db.flush()
                        sys_user = await user_dao.get_by_username(db, username)

                    # 绑定社交用户
                    new_user_social = CreateUserSocialParam(sid=str(sid), source=social.value, user_id=sys_user.id)
                    await user_social_dao.create(db, new_user_social)

            if not sys_user:
                sys_user = await user_dao.get(db, user_social.user_id)
                if avatar:
                    await user_dao.update_avatar(db, sys_user.id, avatar)

            # 创建 token
            access_token = await jwt.create_access_token(
                str(sys_user.id),
                sys_user.is_multi_login,
                # extra info
                username=sys_user.username,
                nickname=sys_user.nickname or f'#{text_captcha(5)}',
                last_login_time=timezone.t_str(timezone.now()),
                ip=request.state.ip,
                os=request.state.os,
                browser=request.state.browser,
                device=request.state.device,
            )
            refresh_token = await jwt.create_refresh_token(str(sys_user.id), multi_login=sys_user.is_multi_login)
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
            await redis_client.delete(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
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
                session_uuid=access_token.session_uuid,
                user=sys_user,  # type: ignore
            )
            return data


oauth2_service: OAuth2Service = OAuth2Service()
