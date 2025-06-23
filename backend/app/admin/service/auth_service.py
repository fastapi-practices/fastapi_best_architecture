#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request, Response
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTask, BackgroundTasks

from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.model import User
from backend.app.admin.schema.token import GetLoginToken, GetNewToken
from backend.app.admin.schema.user import AuthLoginParam
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.enums import LoginLogStatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.common.response.response_code import CustomErrorCode
from backend.common.security.jwt import (
    create_access_token,
    create_new_token,
    create_refresh_token,
    get_token,
    jwt_decode,
    password_verify,
)
from backend.core.conf import settings
from backend.database.db import async_db_session, uuid4_str
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


class AuthService:
    """认证服务类"""

    @staticmethod
    async def user_verify(db: AsyncSession, username: str, password: str | None) -> User:
        """
        验证用户名和密码

        :param db: 数据库会话
        :param username: 用户名
        :param password: 密码
        :return:
        """
        user = await user_dao.get_by_username(db, username)
        if not user:
            raise errors.NotFoundError(msg='用户名或密码有误')

        if user.password is None:
            raise errors.AuthorizationError(msg='用户名或密码有误')
        else:
            if not password_verify(password, user.password):
                raise errors.AuthorizationError(msg='用户名或密码有误')

        if not user.status:
            raise errors.AuthorizationError(msg='用户已被锁定, 请联系统管理员')

        return user

    async def swagger_login(self, *, obj: HTTPBasicCredentials) -> tuple[str, User]:
        """
        Swagger 文档登录

        :param obj: 登录凭证
        :return:
        """
        async with async_db_session.begin() as db:
            user = await self.user_verify(db, obj.username, obj.password)
            await user_dao.update_login_time(db, obj.username)
            access_token = await create_access_token(
                user.id,
                user.is_multi_login,
                # extra info
                swagger=True,
            )
            return access_token.access_token, user

    async def login(
        self, *, request: Request, response: Response, obj: AuthLoginParam, background_tasks: BackgroundTasks
    ) -> GetLoginToken:
        """
        用户登录

        :param request: 请求对象
        :param response: 响应对象
        :param obj: 登录参数
        :param background_tasks: 后台任务
        :return:
        """
        async with async_db_session.begin() as db:
            user = None
            try:
                user = await self.user_verify(db, obj.username, obj.password)
                captcha_code = await redis_client.get(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                if not captcha_code:
                    raise errors.RequestError(msg='验证码失效，请重新获取')
                if captcha_code.lower() != obj.captcha.lower():
                    raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
                await redis_client.delete(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                await user_dao.update_login_time(db, obj.username)
                await db.refresh(user)
                access_token = await create_access_token(
                    user.id,
                    user.is_multi_login,
                    # extra info
                    username=user.username,
                    nickname=user.nickname,
                    last_login_time=timezone.to_str(user.last_login_time),
                    ip=request.state.ip,
                    os=request.state.os,
                    browser=request.state.browser,
                    device=request.state.device,
                )
                refresh_token = await create_refresh_token(access_token.session_uuid, user.id, user.is_multi_login)
                response.set_cookie(
                    key=settings.COOKIE_REFRESH_TOKEN_KEY,
                    value=refresh_token.refresh_token,
                    max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                    expires=timezone.to_utc(refresh_token.refresh_token_expire_time),
                    httponly=True,
                )
            except errors.NotFoundError as e:
                log.error('登陆错误: 用户名不存在')
                raise errors.NotFoundError(msg=e.msg)
            except (errors.RequestError, errors.CustomError) as e:
                if not user:
                    log.error('登陆错误: 用户密码有误')
                task = BackgroundTask(
                    login_log_service.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user.uuid if user else uuid4_str(),
                        username=obj.username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.fail.value,
                        msg=e.msg,
                    ),
                )
                raise errors.RequestError(msg=e.msg, background=task)
            except Exception as e:
                log.error(f'登陆错误: {e}')
                raise e
            else:
                background_tasks.add_task(
                    login_log_service.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user.uuid,
                        username=obj.username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.success.value,
                        msg='登录成功',
                    ),
                )
                data = GetLoginToken(
                    access_token=access_token.access_token,
                    access_token_expire_time=access_token.access_token_expire_time,
                    session_uuid=access_token.session_uuid,
                    user=user,  # type: ignore
                )
                return data

    @staticmethod
    async def get_codes(*, request: Request) -> list[str]:
        """
        获取用户权限码

        :param request: FastAPI 请求对象
        :return:
        """
        codes = set()
        if request.user.is_superuser:
            async with async_db_session.begin() as db:
                menus = await menu_dao.get_all(db, None, None)
                for menu in menus:
                    if menu.perms:
                        codes.add(*menu.perms.split(','))
        else:
            roles = request.user.roles
            if roles:
                for role in roles:
                    for menu in role.menus:
                        if menu.perms:
                            codes.add(*menu.perms.split(','))

        return list(codes)

    @staticmethod
    async def refresh_token(*, request: Request) -> GetNewToken:
        """
        刷新令牌

        :param request: FastAPI 请求对象
        :return:
        """
        refresh_token = request.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)
        if not refresh_token:
            raise errors.TokenError(msg='Refresh Token 已过期，请重新登录')
        token_payload = jwt_decode(refresh_token)
        async with async_db_session() as db:
            user = await user_dao.get(db, token_payload.id)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not user.status:
                raise errors.AuthorizationError(msg='用户已被锁定, 请联系统管理员')
            new_token = await create_new_token(
                refresh_token,
                token_payload.session_uuid,
                user.id,
                user.is_multi_login,
                # extra info
                username=user.username,
                nickname=user.nickname,
                last_login_time=timezone.to_str(user.last_login_time),
                ip=request.state.ip,
                os=request.state.os,
                browser=request.state.browser,
                device_type=request.state.device,
            )
            data = GetNewToken(
                access_token=new_token.new_access_token,
                access_token_expire_time=new_token.new_access_token_expire_time,
                session_uuid=new_token.session_uuid,
            )
            return data

    @staticmethod
    async def logout(*, request: Request, response: Response) -> None:
        """
        用户登出

        :param request: FastAPI 请求对象
        :param response: FastAPI 响应对象
        :return:
        """
        try:
            token = get_token(request)
            token_payload = jwt_decode(token)
            user_id = token_payload.id
            session_uuid = token_payload.session_uuid
            refresh_token = request.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)
        except errors.TokenError:
            return
        finally:
            response.delete_cookie(settings.COOKIE_REFRESH_TOKEN_KEY)

        await redis_client.delete(f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}')
        await redis_client.delete(f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{user_id}:{session_uuid}')
        if refresh_token:
            await redis_client.delete(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{refresh_token}')


auth_service: AuthService = AuthService()
