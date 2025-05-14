#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from fastapi import Request
from sqlalchemy import Select

from backend.app.admin.crud.crud_dept import dept_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.model import User
from backend.app.admin.schema.user import (
    AddUserParam,
    AvatarParam,
    RegisterUserParam,
    ResetPasswordParam,
    UpdateUserParam,
    UpdateUserRoleParam,
)
from backend.common.exception import errors
from backend.common.security.jwt import get_hash_password, get_token, jwt_decode, password_verify, superuser_verify
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class UserService:
    """User service category"""

    @staticmethod
    async def register(*, obj: RegisterUserParam) -> None:
        """
        Register new users

        :param obj: user registration parameters
        :return:
        """
        async with async_db_session.begin() as db:
            if not obj.password:
                raise errors.ForbiddenError(msg='Password is empty')
            username = await user_dao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='User registered')
            obj.nickname = obj.nickname if obj.nickname else f'#{random.randrange(10000, 88888)}'
            nickname = await user_dao.get_by_nickname(db, obj.nickname)
            if nickname:
                raise errors.ForbiddenError(msg='Nickname registered')
            email = await user_dao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='Mailbox registered')
            await user_dao.create(db, obj)

    @staticmethod
    async def add(*, request: Request, obj: AddUserParam) -> None:
        """
        Add new user

        :param request: FastAPI
        :param obj: user add parameters
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            username = await user_dao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='User registered')
            obj.nickname = obj.nickname if obj.nickname else f'#{random.randrange(88888, 99999)}'
            nickname = await user_dao.get_by_nickname(db, obj.nickname)
            if nickname:
                raise errors.ForbiddenError(msg='Nickname registered')
            if not obj.password:
                raise errors.ForbiddenError(msg='Password is empty')
            email = await user_dao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='Mailbox registered')
            dept = await dept_dao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='Department does not exist')
            for role_id in obj.roles:
                role = await role_dao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='Role does not exist')
            await user_dao.add(db, obj)

    @staticmethod
    async def pwd_reset(*, request: Request, obj: ResetPasswordParam) -> int:
        """
        Reset user password

        :param request: FastAPI
        :param obj: password reset parameters
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get(db, request.user.id)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if not password_verify(obj.old_password, user.password):
                raise errors.ForbiddenError(msg='Original password error')
            if obj.new_password != obj.confirm_password:
                raise errors.ForbiddenError(msg='Password input is inconsistent')
            new_pwd = get_hash_password(obj.new_password, user.salt)
            count = await user_dao.reset_password(db, request.user.id, new_pwd)
            key_prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{request.user.id}',
                f'{settings.JWT_USER_REDIS_PREFIX}:{request.user.id}',
            ]
            for prefix in key_prefix:
                await redis_client.delete_prefix(prefix)
            return count

    @staticmethod
    async def get_userinfo(*, username: str) -> User:
        """
        Get User Information

        :param username:
        :return:
        """
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            return user

    @staticmethod
    async def update(*, request: Request, username: str, obj: UpdateUserParam) -> int:
        """
        Update user information

        :param request: FastAPI
        :param username:
        :param obj: user update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            if request.user.username != username:
                raise errors.ForbiddenError(msg='You can only modify your own information')
            user = await user_dao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if user.username != obj.username:
                _username = await user_dao.get_by_username(db, obj.username)
                if _username:
                    raise errors.ForbiddenError(msg='Username registered')
            if user.nickname != obj.nickname:
                nickname = await user_dao.get_by_nickname(db, obj.nickname)
                if nickname:
                    raise errors.ForbiddenError(msg='Nickname registered')
            if user.email != obj.email:
                email = await user_dao.check_email(db, obj.email)
                if email:
                    raise errors.ForbiddenError(msg='Mailbox registered')
            count = await user_dao.update_userinfo(db, user.id, obj)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_roles(*, request: Request, username: str, obj: UpdateUserRoleParam) -> None:
        """
        Update user roles

        :param request: FastAPI
        :param username:
        :param obj: role update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            if not request.user.is_superuser and request.user.username != username:
                raise errors.ForbiddenError(msg='You can only modify your own information')
            input_user = await user_dao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='User does not exist')
            for role_id in obj.roles:
                role = await role_dao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='Role does not exist')
            await user_dao.update_role(db, input_user, obj)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{input_user.id}')

    @staticmethod
    async def update_avatar(*, request: Request, username: str, avatar: AvatarParam) -> int:
        """
        Update user header

        :param request: FastAPI
        :param username:
        :param avarar: headline parameters
        :return:
        """
        async with async_db_session.begin() as db:
            if request.user.username != username:
                raise errors.AuthorizationError(msg='你只能修改自己的信息')
            user = await user_dao.get_by_username(db, username)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            count = await user_dao.update_avatar(db, user.id, avatar)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def get_select(*, dept: int, username: str, phone: str, status: int) -> Select:
        """
        Fetch user list query conditions

        :param dept: Department ID
        :param username:
        :param phone number
        :param status: status
        :return:
        """
        return await user_dao.get_list(dept=dept, username=username, phone=phone, status=status)

    @staticmethod
    async def update_permission(*, request: Request, pk: int) -> int:
        """
        Update user privileges

        :param request: FastAPI
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='Illegal operation')
            super_status = await user_dao.get_super(db, pk)
            count = await user_dao.set_super(db, pk, not super_status)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_staff(*, request: Request, pk: int) -> int:
        """
        Update user staff status

        :param request: FastAPI
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='Illegal operation')
            staff_status = await user_dao.get_staff(db, pk)
            count = await user_dao.set_staff(db, pk, not staff_status)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_status(*, request: Request, pk: int) -> int:
        """
        Update user status

        :param request: FastAPI
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='Illegal operation')
            status = await user_dao.get_status(db, pk)
            count = await user_dao.set_status(db, pk, 0 if status == 1 else 1)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_multi_login(*, request: Request, pk: int) -> int:
        """
        Update user multiple login status

        :param request: FastAPI
        :param pk: User ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            multi_login = await user_dao.get_multi_login(db, pk) if pk != user.id else request.user.is_multi_login
            new_multi_login = not multi_login
            count = await user_dao.set_multi_login(db, pk, new_multi_login)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            token = get_token(request)
            token_payload = jwt_decode(token)
            if pk == user.id:
                # system administrator disables token other than the current token when modifying yourself
                if not new_multi_login:
                    key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                    await redis_client.delete_prefix(key_prefix, exclude=f'{key_prefix}:{token_payload.session_uuid}')
            else:
                # all tokens expire when system administrator changes another person
                if not new_multi_login:
                    key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                    await redis_client.delete_prefix(key_prefix)
            return count

    @staticmethod
    async def delete(*, username: str) -> int:
        """
        Remove User

        :param username:
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get_by_username(db, username)
            if not user:
                raise errors.NotFoundError(msg='User does not exist')
            count = await user_dao.delete(db, user.id)
            key_prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
            ]
            for key in key_prefix:
                await redis_client.delete_prefix(key)
            return count


user_service: UserService = UserService()
