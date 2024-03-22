#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request
from fastapi.security import HTTPBasicCredentials
from starlette.background import BackgroundTask, BackgroundTasks

from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.model import User
from backend.app.admin.schema.token import GetLoginToken, GetNewToken
from backend.app.admin.schema.user import AuthLoginParam
from backend.app.admin.service.login_log_service import LoginLogService
from backend.common.enums import LoginLogStatusType
from backend.common.exception import errors
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
from backend.database.db_mysql import async_db_session
from backend.database.db_redis import redis_client
from backend.utils.timezone import timezone


class AuthService:
    @staticmethod
    async def swagger_login(obj: HTTPBasicCredentials) -> tuple[str, User]:
        async with async_db_session.begin() as db:
            current_user = await user_dao.get_by_username(db, obj.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not await password_verify(f'{obj.password}{current_user.salt}', current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.status:
                raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
            access_token, _ = await create_access_token(str(current_user.id), multi_login=current_user.is_multi_login)
            await user_dao.update_login_time(db, obj.username)
            return access_token, current_user

    @staticmethod
    async def login(*, request: Request, obj: AuthLoginParam, background_tasks: BackgroundTasks) -> GetLoginToken:
        async with async_db_session.begin() as db:
            try:
                current_user = await user_dao.get_by_username(db, obj.username)
                if not current_user:
                    raise errors.NotFoundError(msg='用户不存在')
                elif not await password_verify(obj.password + current_user.salt, current_user.password):
                    raise errors.AuthorizationError(msg='密码错误')
                elif not current_user.status:
                    raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
                captcha_code = await redis_client.get(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                if not captcha_code:
                    raise errors.AuthorizationError(msg='验证码失效，请重新获取')
                if captcha_code.lower() != obj.captcha.lower():
                    raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
                access_token, access_token_expire_time = await create_access_token(
                    str(current_user.id), multi_login=current_user.is_multi_login
                )
                refresh_token, refresh_token_expire_time = await create_refresh_token(
                    str(current_user.id), access_token_expire_time, multi_login=current_user.is_multi_login
                )
                await user_dao.update_login_time(db, obj.username)
                await db.refresh(current_user)
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                err_log_info = dict(
                    db=db,
                    request=request,
                    user=current_user,
                    login_time=timezone.now(),
                    status=LoginLogStatusType.fail.value,
                    msg=e.msg,
                )
                task = BackgroundTask(LoginLogService.create, **err_log_info)
                raise errors.AuthorizationError(msg=e.msg, background=task)
            except Exception as e:
                raise e
            else:
                login_log = dict(
                    db=db,
                    request=request,
                    user=current_user,
                    login_time=timezone.now(),
                    status=LoginLogStatusType.success.value,
                    msg='登录成功',
                )
                background_tasks.add_task(LoginLogService.create, **login_log)
                await redis_client.delete(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                data = GetLoginToken(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    access_token_expire_time=access_token_expire_time,
                    refresh_token_expire_time=refresh_token_expire_time,
                    user=current_user,  # type: ignore
                )
                return data

    @staticmethod
    async def new_token(*, request: Request, refresh_token: str) -> GetNewToken:
        user_id = await jwt_decode(refresh_token)
        if request.user.id != user_id:
            raise errors.TokenError(msg='刷新 token 无效')
        async with async_db_session() as db:
            current_user = await user_dao.get(db, user_id)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not current_user.status:
                raise errors.AuthorizationError(msg='用户已锁定，操作失败')
            current_token = await get_token(request)
            (
                new_access_token,
                new_refresh_token,
                new_access_token_expire_time,
                new_refresh_token_expire_time,
            ) = await create_new_token(
                str(current_user.id), current_token, refresh_token, multi_login=current_user.is_multi_login
            )
            data = GetNewToken(
                access_token=new_access_token,
                access_token_expire_time=new_access_token_expire_time,
                refresh_token=new_refresh_token,
                refresh_token_expire_time=new_refresh_token_expire_time,
            )
            return data

    @staticmethod
    async def logout(*, request: Request) -> None:
        token = await get_token(request)
        if request.user.is_multi_login:
            key = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:{token}'
            await redis_client.delete(key)
        else:
            prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:'
            await redis_client.delete_prefix(prefix)


auth_service = AuthService()
