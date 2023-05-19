#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
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


async def create_access_token(sub: int | Any, data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate encryption token

    :param sub: The subject/userid of the JWT
    :param data: Data transferred to the token
    :param expires_delta: Increased expiry time
    :return:
    """
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
        expire_seconds = expires_delta.total_seconds()
    else:
        expires = datetime.utcnow() + timedelta(seconds=settings.TOKEN_EXPIRE_MINUTES)
        expire_seconds = settings.TOKEN_EXPIRE_SECONDS
    to_encode = {'exp': expires, 'sub': str(sub), **data}
    token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    if sub not in settings.TOKEN_WHITE_LIST:
        await redis_client.delete(f'token:{sub}:*')
    key = f'token:{sub}:{token}'
    await redis_client.setex(key, expire_seconds, token)
    return token


async def jwt_authentication(token: str = Depends(oauth2_schema)):
    """
    JWT authentication

    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = payload.get('sub')
        user_role = payload.get('role_ids')
        if not user_id or not user_role:
            raise TokenError
        # 验证token是否有效
        key = f'token:{user_id}:{token}'
        valid_token = await redis_client.get(key)
        if not valid_token:
            raise TokenError
        return {'payload': payload, 'token': token}
    except (jwt.JWTError, ValidationError):
        raise TokenError


async def get_current_user(db: CurrentSession, data: dict = Depends(jwt_authentication)) -> User:
    """
    Get the current user through tokens

    :param db:
    :param data:
    :return:
    """
    user_id = data.get('payload').get('sub')
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
JwtAuthentication = Annotated[dict, Depends(jwt_authentication)]
# Permission dependency injection
DependsUser = Depends(get_current_user)
DependsSuperUser = Depends(get_current_is_superuser)
