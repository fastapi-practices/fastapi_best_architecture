#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from typing_extensions import Annotated

from backend.app.common.exception.errors import AuthorizationError, TokenError
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import CurrentSession
from backend.app.models import User
from backend.app.schemas.token import RefreshTokenTime

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL_SWAGGER)


def get_hash_password(password: str) -> str:
    """
    Encrypt passwords using the hash algorithm

    :param password:
    :return:
    """
    return pwd_context.hash(password)


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
        expire = datetime.utcnow() + expires_delta
        expire_seconds = int(expires_delta.total_seconds())
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_EXPIRE_SECONDS
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    if sub not in settings.TOKEN_WHITE_LIST:
        await redis_client.delete_prefix(f'{settings.TOKEN_REDIS_PREFIX}:{sub}:')
    key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
    await redis_client.setex(key, expire_seconds, token)
    return token, expire


async def create_refresh_token(
    sub: str, expire_time: datetime | None = None, custom_expire_time: RefreshTokenTime | None = None, **kwargs
) -> tuple[str, datetime]:
    """
    Generate encryption refresh token

    :param sub: The subject/userid of the JWT
    :param expire_time: expiry time
    :param custom_expire_time: custom expiry time
    :return:
    """
    if expire_time:
        expire = expire_time + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = int((expire - datetime.utcnow()).total_seconds())
    elif custom_expire_time:
        expire = custom_expire_time.expire_time
        expire_seconds = int((expire - datetime.utcnow()).total_seconds())
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_EXPIRE_SECONDS
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    # 刷新 token 时，保持旧 token 有效，不执行删除操作
    key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
    await redis_client.setex(key, expire_seconds, token)
    return token, expire


def get_token(request: Request) -> str:
    """
    Get token for request header

    :return:
    """
    authorization = request.headers.get('Authorization')
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError
    return param


def jwt_decode(token: str) -> tuple[int, list[int]]:
    """
    Decode token

    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = int(payload.get('sub'))
        user_roles = list(payload.get('role_ids'))
        if not user_id or not user_roles:
            raise TokenError
    except (jwt.JWTError, ValidationError, Exception):
        raise TokenError
    return user_id, user_roles


async def jwt_authentication(token: str = Depends(oauth2_schema)) -> dict[str, int]:
    """
    JWT authentication

    :param token:
    :return:
    """
    user_id, _ = jwt_decode(token)
    key = f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{token}'
    token_verify = await redis_client.get(key)
    if not token_verify:
        raise TokenError
    return {'sub': user_id}


async def get_current_user(db: CurrentSession, data: dict = Depends(jwt_authentication)) -> User:
    """
    Get the current user through tokens

    :param db:
    :param data:
    :return:
    """
    user_id = data.get('sub')
    user = await UserDao.get_user_with_relation(db, user_id=user_id)
    if not user:
        raise TokenError
    return user


async def get_current_is_superuser(user: User = Depends(get_current_user)):
    """
    Verify the current user permissions through token

    :param user:
    :return:
    """
    is_superuser = user.is_superuser
    if not is_superuser:
        raise AuthorizationError
    return is_superuser


# User Annotated
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentSuperUser = Annotated[bool, Depends(get_current_is_superuser)]
# Token dependency injection
CurrentJwtAuth = Annotated[dict, Depends(jwt_authentication)]
# Permission dependency injection
DependsUser = Depends(get_current_user)
DependsSuperUser = Depends(get_current_is_superuser)
