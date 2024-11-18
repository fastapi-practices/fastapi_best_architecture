#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import timedelta

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pydantic_core import from_json
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import User
from backend.app.admin.schema.user import CurrentUserIns
from backend.common.dataclasses import AccessToken, NewToken, RefreshToken
from backend.common.exception.errors import AuthorizationError, TokenError
from backend.core.conf import settings
from backend.database.db_mysql import async_db_session
from backend.database.db_redis import redis_client
from backend.utils.serializers import select_as_dict
from backend.utils.timezone import timezone

# JWT authorizes dependency injection
DependsJwtAuth = Depends(HTTPBearer())

password_hash = PasswordHash((BcryptHasher(),))


def get_hash_password(password: str, salt: bytes | None) -> str:
    """
    Encrypt passwords using the hash algorithm

    :param password:
    :param salt:
    :return:
    """
    return password_hash.hash(password, salt=salt)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    Password verification

    :param plain_password: The password to verify
    :param hashed_password: The hash ciphers to compare
    :return:
    """
    return password_hash.verify(plain_password, hashed_password)


async def create_access_token(sub: str, multi_login: bool) -> AccessToken:
    """
    Generate encryption token

    :param sub: The subject/userid of the JWT
    :param multi_login: multipoint login for user
    :return:
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    expire_seconds = settings.TOKEN_EXPIRE_SECONDS

    to_encode = {'exp': expire, 'sub': sub}
    access_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)

    if multi_login is False:
        key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{sub}'
        await redis_client.delete_prefix(key_prefix)

    key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{access_token}'
    await redis_client.setex(key, expire_seconds, access_token)
    return AccessToken(access_token=access_token, access_token_expire_time=expire)


async def create_refresh_token(sub: str, multi_login: bool) -> RefreshToken:
    """
    Generate encryption refresh token, only used to create a new token

    :param sub: The subject/userid of the JWT
    :param multi_login: multipoint login for user
    :return:
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    expire_seconds = settings.TOKEN_REFRESH_EXPIRE_SECONDS

    to_encode = {'exp': expire, 'sub': sub}
    refresh_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)

    if multi_login is False:
        key_prefix = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}'
        await redis_client.delete_prefix(key_prefix)

    key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}'
    await redis_client.setex(key, expire_seconds, refresh_token)
    return RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=expire)


async def create_new_token(sub: str, token: str, refresh_token: str, multi_login: bool) -> NewToken:
    """
    Generate new token

    :param sub:
    :param token
    :param refresh_token:
    :param multi_login:
    :return:
    """
    redis_refresh_token = await redis_client.get(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}')
    if not redis_refresh_token or redis_refresh_token != refresh_token:
        raise TokenError(msg='Refresh Token 已过期')

    new_access_token = await create_access_token(sub, multi_login)
    new_refresh_token = await create_refresh_token(sub, multi_login)

    token_key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
    refresh_token_key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}'
    await redis_client.delete(token_key)
    await redis_client.delete(refresh_token_key)
    return NewToken(
        new_access_token=new_access_token.access_token,
        new_access_token_expire_time=new_access_token.access_token_expire_time,
        new_refresh_token=new_refresh_token.refresh_token,
        new_refresh_token_expire_time=new_refresh_token.refresh_token_expire_time,
    )


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
    except ExpiredSignatureError:
        raise TokenError(msg='Token 已过期')
    except (JWTError, Exception):
        raise TokenError(msg='Token 无效')
    return user_id


async def get_current_user(db: AsyncSession, pk: int) -> User:
    """
    Get the current user through token

    :param db:
    :param pk:
    :return:
    """
    from backend.app.admin.crud.crud_user import user_dao

    user = await user_dao.get_with_relation(db, user_id=pk)
    if not user:
        raise TokenError(msg='Token 无效')
    if not user.status:
        raise AuthorizationError(msg='用户已被锁定，请联系系统管理员')
    if user.dept_id:
        if not user.dept.status:
            raise AuthorizationError(msg='用户所属部门已被锁定，请联系系统管理员')
        if user.dept.del_flag:
            raise AuthorizationError(msg='用户所属部门已被删除，请联系系统管理员')
    if user.roles:
        role_status = [role.status for role in user.roles]
        if all(status == 0 for status in role_status):
            raise AuthorizationError(msg='用户所属角色已被锁定，请联系系统管理员')
    return user


def superuser_verify(request: Request) -> bool:
    """
    Verify the current user permissions through token

    :param request:
    :return:
    """
    superuser = request.user.is_superuser
    if not superuser or not request.user.is_staff:
        raise AuthorizationError
    return superuser


async def jwt_authentication(token: str) -> CurrentUserIns:
    """
    JWT authentication

    :param token:
    :return:
    """
    user_id = jwt_decode(token)
    key = f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{token}'
    token_verify = await redis_client.get(key)
    if not token_verify:
        raise TokenError(msg='Token 已过期')
    cache_user = await redis_client.get(f'{settings.JWT_USER_REDIS_PREFIX}:{user_id}')
    if not cache_user:
        async with async_db_session() as db:
            current_user = await get_current_user(db, user_id)
            user = CurrentUserIns(**select_as_dict(current_user))
            await redis_client.setex(
                f'{settings.JWT_USER_REDIS_PREFIX}:{user_id}',
                settings.JWT_USER_REDIS_EXPIRE_SECONDS,
                user.model_dump_json(),
            )
    else:
        # TODO: 在恰当的时机，应替换为使用 model_validate_json
        # https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing
        user = CurrentUserIns.model_validate(from_json(cache_user, allow_partial=True))
    return user
