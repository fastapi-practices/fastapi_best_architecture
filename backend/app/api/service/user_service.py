#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email_validator import validate_email, EmailNotValidError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination.ext.sqlalchemy import paginate

from backend.app.api import jwt
from backend.app.common.exception import errors
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_session, async_session_transaction, AsyncSessionNotInput
from backend.app.models import User
from backend.app.schemas.user import CreateUser, ResetPassword, UpdateUser, Avatar
from backend.app.utils import re_verify


class UserService:

    @staticmethod
    @async_session
    async def login(db: AsyncSessionNotInput, *, form_data: OAuth2PasswordRequestForm):
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
    # @async_session
    # async def login(db: AsyncSessionNotInput, *, obj: Auth):
    #     current_user = await UserDao.get_user_by_username(db, obj.username)
    #     if not current_user:
    #         raise errors.NotFoundError(msg='用户名不存在')
    #     elif not jwt.password_verify(obj.password, current_user.password):
    #         raise errors.AuthorizationError(msg='密码错误')
    #     elif not current_user.is_active:
    #         raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
    #     # 更新登陆时间
    #     await UserDao.update_user_login_time(db, obj.username)
    #     # 创建token
    #     access_token = jwt.create_access_token(current_user.id)
    #     return access_token, current_user.is_superuser

    @staticmethod
    @async_session_transaction
    async def register(db: AsyncSessionNotInput, *, obj: CreateUser):
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
    @async_session_transaction
    async def pwd_reset(db: AsyncSessionNotInput, *, obj: ResetPassword):
        pwd1 = obj.password1
        pwd2 = obj.password2
        if pwd1 != pwd2:
            raise errors.ForbiddenError(msg='两次密码输入不一致')
        await UserDao.reset_password(db, obj.id, obj.password2)

    @staticmethod
    @async_session
    async def get_userinfo(db: AsyncSessionNotInput, *, username: str):
        user = await UserDao.get_user_by_username(db, username)
        if not user:
            raise errors.NotFoundError(msg='用户不存在')
        return user

    @staticmethod
    @async_session_transaction
    async def update(db: AsyncSessionNotInput, *, username: str, current_user: User, obj: UpdateUser):
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
        count = await UserDao.update_userinfo(db, input_user, obj)
        return count

    @staticmethod
    @async_session_transaction
    async def update_avatar(db: AsyncSessionNotInput, *, username: str, current_user: User, avatar: Avatar):
        if not current_user.is_superuser:
            if not username == current_user.username:
                raise errors.AuthorizationError
        input_user = await UserDao.get_user_by_username(db, username)
        if not input_user:
            raise errors.NotFoundError(msg='用户不存在')
        count = await UserDao.update_avatar(db, input_user, avatar)
        return count

    @staticmethod
    @async_session
    async def get_user_list(db: AsyncSessionNotInput):
        user_select = UserDao.get_users()
        return await paginate(db, user_select)

    @staticmethod
    @async_session_transaction
    async def update_permission(db: AsyncSessionNotInput, *, pk: int):
        if await UserDao.get_user_by_id(db, pk):
            count = await UserDao.super_set(db, pk)
            return count
        else:
            raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    @async_session_transaction
    async def update_active(db: AsyncSessionNotInput, *, pk: int):
        if await UserDao.get_user_by_id(db, pk):
            count = await UserDao.active_set(db, pk)
            return count
        else:
            raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    @async_session_transaction
    async def delete(db: AsyncSessionNotInput, *, username: str, current_user: User):
        if not current_user.is_superuser:
            if not username == current_user.username:
                raise errors.AuthorizationError
        input_user = await UserDao.get_user_by_username(db, username)
        if not input_user:
            raise errors.NotFoundError(msg='用户不存在')
        count = await UserDao.delete_user(db, input_user.id)
        return count
