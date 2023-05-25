#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.datetime_parse import parse_datetime
from user_agents import parse

from backend.app.common import jwt
from backend.app.common.exception import errors
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_dept import DeptDao
from backend.app.crud.crud_role import RoleDao
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.login_log import CreateLoginLog
from backend.app.schemas.token import RefreshTokenTime
from backend.app.schemas.user import CreateUser, ResetPassword, UpdateUser, Avatar, Auth
from backend.app.services.login_log_service import LoginLogService
from backend.app.utils import re_verify, request_parse


class UserService:
    login_time = parse_datetime(datetime.utcnow())

    async def swagger_login(self, form_data: OAuth2PasswordRequestForm):
        async with async_db_session() as db:
            current_user = await UserDao.get_by_username(db, form_data.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not jwt.password_verify(form_data.password, current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
            # 更新登陆时间
            await UserDao.update_login_time(db, form_data.username, self.login_time)
            # 查询用户角色
            user_role_ids = await UserDao.get_role_ids(db, current_user.id)
            # 获取最新用户信息
            user = await UserDao.get(db, current_user.id)
            # 创建token
            access_token, _ = await jwt.create_access_token(str(user.id), role_ids=user_role_ids)
            return access_token, user

    async def login(self, request: Request, obj: Auth):
        async with async_db_session() as db:
            try:
                current_user = await UserDao.get_by_username(db, obj.username)
                if not current_user:
                    raise errors.NotFoundError(msg='用户不存在')
                elif not jwt.password_verify(obj.password, current_user.password):
                    raise errors.AuthorizationError(msg='密码错误')
                elif not current_user.is_active:
                    raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
                await UserDao.update_login_time(db, obj.username, self.login_time)
                user_role_ids = await UserDao.get_role_ids(db, current_user.id)
                user = await UserDao.get(db, current_user.id)
                access_token, access_token_expire_time = await jwt.create_access_token(
                    str(user.id), role_ids=user_role_ids
                )
                refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                    str(user.id), access_token_expire_time, role_ids=user_role_ids
                )
                ip = await request_parse.get_request_ip(request)
                user_agent = request.headers.get('User-Agent')
                user_agent_parse = str(parse(user_agent)).replace(' ', '').split('/')
                location = await request_parse.get_location(ip, user_agent) if settings.LOCATION_PARSE else '未知'
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except errors.AuthorizationError as e:
                await LoginLogService.create(
                    db=db,
                    obj_in=CreateLoginLog(
                        user_uuid=user.user_uuid,
                        username=user.username,
                        status=0,
                        ipaddr=ip,
                        location=location,
                        browser=user_agent_parse[2],
                        os=user_agent_parse[1],
                        msg=e.msg,
                        login_time=self.login_time,
                    ),
                )
                raise errors.AuthorizationError(msg=e.msg)
            except Exception as e:
                await LoginLogService.create(
                    db=db,
                    obj_in=CreateLoginLog(
                        user_uuid=user.user_uuid,
                        username=user.username,
                        status=0,
                        ipaddr=ip,
                        location=location,
                        browser=user_agent_parse[2],
                        os=user_agent_parse[1],
                        msg=str(e),
                        login_time=self.login_time,
                    ),
                )
                raise e
            else:
                await LoginLogService.create(
                    db=db,
                    obj_in=CreateLoginLog(
                        user_uuid=user.user_uuid,
                        username=user.username,
                        status=1,
                        ipaddr=ip,
                        location=location,
                        browser=user_agent_parse[2],
                        os=user_agent_parse[1],
                        msg='登陆成功',
                        login_time=self.login_time,
                    ),
                )
                return access_token, refresh_token, access_token_expire_time, refresh_token_expire_time, user

    @staticmethod
    async def refresh_token(user_id: int, custom_time: RefreshTokenTime):
        async with async_db_session() as db:
            current_user = await UserDao.get(db, user_id)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='用户已锁定, 获取失败')
            user_role_ids = await UserDao.get_role_ids(db, current_user.id)
            refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                str(current_user.id), custom_expire_time=custom_time, role_ids=user_role_ids
            )
            return refresh_token, refresh_token_expire_time

    @staticmethod
    async def logout(user_id: int):
        key = f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:'
        await redis_client.delete_prefix(key)
        return

    @staticmethod
    async def register(obj: CreateUser):
        async with async_db_session.begin() as db:
            username = await UserDao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已注册')
            email = await UserDao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            try:
                validate_email(obj.email, check_deliverability=False).email
            except EmailNotValidError:
                raise errors.ForbiddenError(msg='邮箱格式错误')
            dept = await DeptDao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await RoleDao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            await UserDao.create(db, obj)

    @staticmethod
    async def pwd_reset(obj: ResetPassword):
        async with async_db_session.begin() as db:
            pwd1 = obj.password1
            pwd2 = obj.password2
            if pwd1 != pwd2:
                raise errors.ForbiddenError(msg='两次密码输入不一致')
            await UserDao.reset_password(db, obj.id, obj.password2)

    @staticmethod
    async def get_userinfo(username: str):
        async with async_db_session() as db:
            user = await UserDao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    @staticmethod
    async def update(*, username: str, current_user: User, obj: UpdateUser):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            if input_user.username != obj.username:
                username = await UserDao.get_by_username(db, obj.username)
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
            if obj.phone is not None:
                if not re_verify.is_phone(obj.phone):
                    raise errors.ForbiddenError(msg='手机号码输入有误')
            dept = await DeptDao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await RoleDao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            count = await UserDao.update_userinfo(db, input_user, obj)
            return count

    @staticmethod
    async def update_avatar(*, username: str, current_user: User, avatar: Avatar):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.update_avatar(db, input_user, avatar)
            return count

    @staticmethod
    async def get_select():
        return UserDao.get_all()

    @staticmethod
    async def update_permission(pk: int):
        async with async_db_session.begin() as db:
            if await UserDao.get(db, pk):
                count = await UserDao.set_super(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def update_active(pk: int):
        async with async_db_session.begin() as db:
            if await UserDao.get(db, pk):
                count = await UserDao.set_active(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def delete(*, username: str, current_user: User):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.delete(db, input_user.id)
            return count
