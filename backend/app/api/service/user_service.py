#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from hashlib import sha256

from email_validator import validate_email, EmailNotValidError
from fast_captcha import text_captcha
from fastapi import Request, HTTPException, Response, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination.ext.async_sqlalchemy import paginate

from backend.app.api import jwt
from backend.app.common.exception import errors
from backend.app.common.log import log
from backend.app.common.redis import redis_client
from backend.app.common.response.response_code import CodeEnum
from backend.app.core.conf import settings
from backend.app.core.path_conf import AvatarPath
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.user import CreateUser, ResetPassword, UpdateUser, ELCode, Auth2
from backend.app.utils import re_verify
from backend.app.utils.format_string import cut_path
from backend.app.utils.generate_string import get_current_timestamp, get_uuid
from backend.app.utils.send_email import send_verification_code_email, SEND_EMAIL_LOGIN_TEXT


class UserService:

    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm):
        async with async_db_session() as db:
            current_user = await UserDao.get_user_by_username(db, form_data.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户名不存在')
            elif not jwt.password_verify(form_data.password, current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
            # 更新登陆时间
            await UserDao.update_user_login_time(db, form_data.username)
            # 创建token
            access_token = jwt.create_access_token(current_user.id)
            return access_token, current_user.is_superuser

    # @staticmethod
    # async def login(obj: Auth):
    #     async with async_db_session() as db:
    #         current_user = await UserDao.get_user_by_username(db, obj.username)
    #         if not current_user:
    #             raise errors.NotFoundError(msg='用户名不存在')
    #         elif not jwt.password_verify(obj.password, current_user.password):
    #             raise errors.AuthorizationError(msg='密码错误')
    #         elif not current_user.is_active:
    #             raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
    #         # 更新登陆时间
    #         await UserDao.update_user_login_time(db, obj.username)
    #         # 创建token
    #         access_token = jwt.create_access_token(current_user.id)
    #         return access_token, current_user.is_superuser

    @staticmethod
    async def login_email(*, request: Request, obj: Auth2):
        async with async_db_session() as db:
            current_email = await UserDao.check_email(db, obj.email)
            if not current_email:
                raise errors.NotFoundError(msg='邮箱不存在')
            username = await UserDao.get_username_by_email(db, obj.email)
            current_user = await UserDao.get_user_by_username(db, username)
            if not current_user.is_active:
                raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
            try:
                uid = request.app.state.email_login_code
            except Exception:
                raise errors.ForbiddenError(msg='请先获取邮箱验证码再登陆')
            r_code = await redis_client.get(f'{uid}')
            if not r_code:
                raise errors.NotFoundError(msg='验证码失效，请重新获取')
            if r_code != obj.code:
                raise errors.CodeError(error=CodeEnum.CAPTCHA_ERROR)
            await UserDao.update_user_login_time(db, username)
            access_token = jwt.create_access_token(current_user.id)
            return access_token, current_user.is_superuser

    @staticmethod
    async def send_login_email_captcha(request: Request, obj: ELCode):
        async with async_db_session() as db:
            if not await UserDao.check_email(db, obj.email):
                raise errors.NotFoundError(msg='邮箱不存在')
            username = await UserDao.get_username_by_email(db, obj.email)
            current_user = await UserDao.get_user_by_username(db, username)
            if not current_user.is_active:
                raise errors.ForbiddenError(msg='该用户已被锁定，无法登录，发送验证码失败')
            try:
                code = text_captcha()
                await send_verification_code_email(obj.email, code, SEND_EMAIL_LOGIN_TEXT)
            except Exception as e:
                log.error('验证码发送失败 {}', e)
                raise errors.ServerError(msg=f'验证码发送失败: {e}')
            else:
                uid = get_uuid()
                await redis_client.set(uid, code, settings.EMAIL_LOGIN_CODE_MAX_AGE)
                request.app.state.email_login_code = uid

    @staticmethod
    async def register(obj: CreateUser):
        async with async_db_session.begin() as db:
            username = await UserDao.get_user_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已注册')
            email = await UserDao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            try:
                validate_email(obj.email, check_deliverability=False).email
            except EmailNotValidError:
                raise errors.ForbiddenError(msg='邮箱格式错误')
            await UserDao.create_user(db, obj)

    @staticmethod
    async def get_pwd_rest_captcha(*, username_or_email: str, response: Response):
        async with async_db_session() as db:
            code = text_captcha()
            if await UserDao.get_user_by_username(db, username_or_email):
                try:
                    response.delete_cookie(key='fastapi_reset_pwd_code')
                    response.delete_cookie(key='fastapi_reset_pwd_username')
                    response.set_cookie(
                        key='fastapi_reset_pwd_code',
                        value=sha256(code.encode('utf-8')).hexdigest(),
                        max_age=settings.COOKIES_MAX_AGE
                    )
                    response.set_cookie(
                        key='fastapi_reset_pwd_username',
                        value=username_or_email,
                        max_age=settings.COOKIES_MAX_AGE
                    )
                except Exception as e:
                    log.exception('无法发送验证码 {}', e)
                    raise e
                current_user_email = await UserDao.get_email_by_username(db, username_or_email)
                await send_verification_code_email(current_user_email, code)
            else:
                try:
                    validate_email(username_or_email, check_deliverability=False)
                except EmailNotValidError:
                    raise HTTPException(status_code=404, detail='用户名不存在')
                email_result = await UserDao.check_email(db, username_or_email)
                if not email_result:
                    raise HTTPException(status_code=404, detail='邮箱不存在')
                try:
                    response.delete_cookie(key='fastapi_reset_pwd_code')
                    response.delete_cookie(key='fastapi_reset_pwd_username')
                    response.set_cookie(
                        key='fastapi_reset_pwd_code',
                        value=sha256(code.encode('utf-8')).hexdigest(),
                        max_age=settings.COOKIES_MAX_AGE
                    )
                    username = await UserDao.get_username_by_email(db, username_or_email)
                    response.set_cookie(
                        key='fastapi_reset_pwd_username',
                        value=username,
                        max_age=settings.COOKIES_MAX_AGE
                    )
                except Exception as e:
                    log.exception('无法发送验证码 {}', e)
                    raise e
                await send_verification_code_email(username_or_email, code)

    @staticmethod
    async def pwd_reset(*, obj: ResetPassword, request: Request, response: Response):
        async with async_db_session.begin() as db:
            pwd1 = obj.password1
            pwd2 = obj.password2
            cookie_reset_pwd_code = request.cookies.get('fastapi_reset_pwd_code')
            cookie_reset_pwd_username = request.cookies.get('fastapi_reset_pwd_username')
            if pwd1 != pwd2:
                raise errors.ForbiddenError(msg='两次密码输入不一致')
            if cookie_reset_pwd_username is None or cookie_reset_pwd_code is None:
                raise errors.NotFoundError(msg='验证码已失效，请重新获取验证码')
            if cookie_reset_pwd_code != sha256(obj.code.encode('utf-8')).hexdigest():
                raise errors.ForbiddenError(msg='验证码错误')
            await UserDao.reset_password(db, cookie_reset_pwd_username, obj.password2)
            response.delete_cookie(key='fastapi_reset_pwd_code')
            response.delete_cookie(key='fastapi_reset_pwd_username')

    @staticmethod
    async def get_user_info(username: str):
        async with async_db_session() as db:
            user = await UserDao.get_user_by_username(db, username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
        if user.avatar is not None:
            user.avatar = cut_path(AvatarPath + user.avatar)[1]
        return user

    @staticmethod
    async def update(*, username: str, current_user: User, obj: UpdateUser):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            if input_user.username != obj.username:
                username = await UserDao.get_user_by_username(db, obj.username)
                if username:
                    raise errors.ForbiddenError(msg='该用户名已存在')
            if input_user.email != obj.email:
                _email = await UserDao.check_email(db, obj.email)
                if _email:
                    raise errors.ForbiddenError(msg='该邮箱已注册')
                try:
                    validate_email(obj.email, check_deliverability=False).email
                except EmailNotValidError:
                    raise errors.ForbiddenError(msg='邮箱格式错误')
            if obj.mobile_number is not None:
                if not re_verify.is_mobile(obj.mobile_number):
                    raise errors.ForbiddenError(msg='手机号码输入有误')
            if obj.wechat is not None:
                if not re_verify.is_wechat(obj.wechat):
                    raise errors.ForbiddenError(msg='微信号码输入有误')
            if obj.qq is not None:
                if not re_verify.is_qq(obj.qq):
                    raise errors.ForbiddenError(msg='QQ号码输入有误')
            count = await UserDao.update_userinfo(db, input_user, obj)
            return count

    @staticmethod
    async def update_avatar(*, username: str, current_user: User, avatar: UploadFile):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            input_user_avatar = input_user.avatar
            if avatar is not None:
                if input_user_avatar is not None:
                    try:
                        os.remove(AvatarPath + input_user_avatar)
                    except Exception as e:
                        log.error('用户 {} 更新头像时，原头像文件 {} 删除失败\n{}', current_user.username,
                                  input_user_avatar,
                                  e)
                new_file = await avatar.read()
                if 'image' not in avatar.content_type:
                    raise errors.ForbiddenError(msg='图片格式错误，请重新选择图片')
                file_name = str(get_current_timestamp()) + '_' + avatar.filename
                if not os.path.exists(AvatarPath):
                    os.makedirs(AvatarPath)
                with open(AvatarPath + f'{file_name}', 'wb') as f:
                    f.write(new_file)
            else:
                file_name = input_user_avatar
            count = await UserDao.update_avatar(db, input_user, file_name)
            return count

    @staticmethod
    async def delete_avatar(*, username: str, current_user: User):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            input_user_avatar = input_user.avatar
            if input_user_avatar is not None:
                try:
                    os.remove(AvatarPath + input_user_avatar)
                except Exception as e:
                    log.error('用户 {} 删除头像文件 {} 失败\n{}', input_user.username, input_user_avatar, e)
            else:
                raise errors.NotFoundError(msg='用户没有头像文件，请上传头像文件后再执行此操作')
            count = await UserDao.delete_avatar(db, input_user.id)
            return count

    @staticmethod
    async def get_user_list():
        async with async_db_session() as db:
            user_select = UserDao.get_users()
            return await paginate(db, user_select)

    @staticmethod
    async def update_permission(pk: int):
        async with async_db_session.begin() as db:
            if await UserDao.get_user_by_id(db, pk):
                count = await UserDao.super_set(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def update_active(pk: int):
        async with async_db_session.begin() as db:
            if await UserDao.get_user_by_id(db, pk):
                count = await UserDao.active_set(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def delete(*, username: str, current_user: User):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            input_user_avatar = input_user.avatar
            try:
                if input_user_avatar is not None:
                    os.remove(AvatarPath + input_user_avatar)
            except Exception as e:
                log.error(f'删除用户 {input_user.username} 头像文件:{input_user_avatar} 失败\n{e}')
            finally:
                count = await UserDao.delete_user(db, input_user.id)
                return count
