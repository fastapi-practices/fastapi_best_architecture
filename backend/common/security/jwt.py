#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from asgiref.sync import sync_to_async
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import User
from backend.common.exception.errors import AuthorizationError, TokenError
from backend.core.conf import settings
from backend.database.db_redis import redis_client
from backend.utils.timezone import timezone

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# JWT authorizes dependency injection
DependsJwtAuth = Depends(HTTPBearer())


@sync_to_async
def get_hash_password(password: str) -> str:
    """
    Encrypt passwords using the hash algorithm

    :param password:
    :return:
    """
    return pwd_context.hash(password)


@sync_to_async
def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    Password verification

    :param plain_password: The password to verify
    :param hashed_password: The hash ciphers to compare
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(sub: str, expires_delta: timedelta | None = None, **kwargs) -> tuple[str, datetime]:
    """
    Generate encryption token

    :param sub: The subject/userid of the JWT
    :param expires_delta: Increased expiry time
    :return:
    """
    if expires_delta:
        expire = timezone.now() + expires_delta
        expire_seconds = int(expires_delta.total_seconds())
    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_EXPIRE_SECONDS
    multi_login = kwargs.pop('multi_login', None)
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    if multi_login is False:
        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:'
        await redis_client.delete_prefix(prefix)
    key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
    await redis_client.setex(key, expire_seconds, token)
    return token, expire


async def create_refresh_token(sub: str, expire_time: datetime | None = None, **kwargs) -> tuple[str, datetime]:
    """
    Generate encryption refresh token, only used to create a new token

    :param sub: The subject/userid of the JWT
    :param expire_time: expiry time
    :return:
    """
    if expire_time:
        expire = expire_time + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
        expire_datetime = timezone.f_datetime(expire_time)
        current_datetime = timezone.now()
        if expire_datetime < current_datetime:
            raise TokenError(msg='Refresh Token 过期时间无效')
        expire_seconds = int((expire_datetime - current_datetime).total_seconds())
    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_REFRESH_EXPIRE_SECONDS
    multi_login = kwargs.pop('multi_login', None)
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    refresh_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    if multi_login is False:
        prefix = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:'
        await redis_client.delete_prefix(prefix)
    key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}'
    await redis_client.setex(key, expire_seconds, refresh_token)
    return refresh_token, expire


async def create_new_token(sub: str, token: str, refresh_token: str, **kwargs) -> tuple[str, str, datetime, datetime]:
    """
    Generate new token

    :param sub:
    :param token
    :param refresh_token:
    :return:
    """
    redis_refresh_token = await redis_client.get(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}')
    if not redis_refresh_token or redis_refresh_token != refresh_token:
        raise TokenError(msg='Refresh Token 已过期')
    new_access_token, new_access_token_expire_time = await create_access_token(sub, **kwargs)
    new_refresh_token, new_refresh_token_expire_time = await create_refresh_token(sub, **kwargs)
    token_key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
    refresh_token_key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{refresh_token}'
    await redis_client.delete(token_key)
    await redis_client.delete(refresh_token_key)
    return new_access_token, new_refresh_token, new_access_token_expire_time, new_refresh_token_expire_time


@sync_to_async
def get_token(request: Request) -> str:
    """
    Get token for request header

    :return:
    """
    authorization = request.headers.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg='Token 无效')
    return token


@sync_to_async
def jwt_decode(token: str) -> int:
    """
    Decode token

    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = int(payload.get('sub'))
        if not user_id:
            raise TokenError(msg='Token 无效')
    except jwt.ExpiredSignatureError:
        raise TokenError(msg='Token 已过期')
    except (jwt.JWTError, Exception):
        raise TokenError(msg='Token 无效')
    return user_id


async def jwt_authentication(token: str) -> dict[str, int]:
    """
    JWT authentication

    :param token:
    :return:
    """
    user_id = await jwt_decode(token)
    key = f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{token}'
    token_verify = await redis_client.get(key)
    if not token_verify:
        raise TokenError(msg='Token 已过期')
    return {'sub': user_id}


async def get_current_user(db: AsyncSession, data: dict) -> User:
    """
    Get the current user through token

    :param db:
    :param data:
    :return:
    """
    user_id = data.get('sub')
    from backend.app.admin.crud.crud_user import user_dao

    user = await user_dao.get_with_relation(db, user_id=user_id)
    if not user:
        raise TokenError(msg='Token 无效')
    if not user.status:
        raise AuthorizationError(msg='用户已锁定')
    if user.dept_id:
        if not user.dept.status:
            raise AuthorizationError(msg='用户所属部门已锁定')
        if user.dept.del_flag:
            raise AuthorizationError(msg='用户所属部门已删除')
    if user.roles:
        role_status = [role.status for role in user.roles]
        if all(status == 0 for status in role_status):
            raise AuthorizationError(msg='用户所属角色已锁定')
    return user


@sync_to_async
def superuser_verify(request: Request) -> bool:
    """
    Verify the current user permissions through token

    :param request:
    :return:
    """
    is_superuser = request.user.is_superuser
    if not is_superuser:
        raise AuthorizationError(msg='仅管理员有权操作')
    if not request.user.is_staff:
        raise AuthorizationError(msg='此管理员已被禁止后台管理操作')
    return is_superuser
