#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from datetime import timedelta
from typing import Any
from uuid import uuid4

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pydantic_core import from_json
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import User
from backend.app.admin.schema.user import GetUserInfoWithRelationDetail
from backend.common.dataclasses import AccessToken, NewToken, RefreshToken, TokenPayload
from backend.common.exception.errors import AuthorizationError, TokenError
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.serializers import select_as_dict
from backend.utils.timezone import timezone

# JWT authorizes dependency injection
DependsJwtAuth = Depends(HTTPBearer())

password_hash = PasswordHash((BcryptHasher(),))


def get_hash_password(password: str, salt: bytes | None) -> str:
    """
    Encrypt password with Hashi algorithm

    :param password: password
    :param salt: salt value
    :return:
    """
    return password_hash.hash(password, salt=salt)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    Password authentication

    :param plain_password: password to be verified
    :param hashed_password: hash password
    :return:
    """
    return password_hash.verify(plain_password, hashed_password)


def jwt_encode(payload: dict[str, Any]) -> str:
    """
    Generate JWT token

    :param payload: load
    :return:
    """
    return jwt.encode(
        payload,
        settings.TOKEN_SECRET_KEY,
        settings.TOKEN_ALGORITHM,
    )


def jwt_decode(token: str) -> TokenPayload:
    """
    Parsing JWT token

    :param token: JWT token
    :return:
    """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        session_uuid = payload.get('session_uuid') or 'debug'
        user_id = payload.get('sub')
        expire_time = payload.get('exp')
        if not user_id:
            raise TokenError(msg='Token is invalid')
    except ExpiredSignatureError:
        raise TokenError(msg='Token Expired')
    except (JWTError, Exception):
        raise TokenError(msg='Token is invalid')
    return TokenPayload(id=int(user_id), session_uuid=session_uuid, expire_time=expire_time)


async def create_access_token(user_id: str, multi_login: bool, **kwargs) -> AccessToken:
    """
    Generate encryption token

    :param user_id: userID
    :param muldi_login: whether multiple login is allowed
    :param kwargs: token extra information
    :return:
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    session_uuid = str(uuid4())
    access_token = jwt_encode({
        'session_uuid': session_uuid,
        'exp': expire,
        'sub': user_id,
    })

    if not multi_login:
        await redis_client.delete_prefix(f'{settings.TOKEN_REDIS_PREFIX}:{user_id}')

    await redis_client.setex(
        f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}',
        settings.TOKEN_EXPIRE_SECONDS,
        access_token,
    )

    # Token Additional Information Store Alone
    if kwargs:
        await redis_client.setex(
            f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{session_uuid}',
            settings.TOKEN_EXPIRE_SECONDS,
            json.dumps(kwargs, ensure_ascii=False),
        )

    return AccessToken(access_token=access_token, access_token_expire_time=expire, session_uuid=session_uuid)


async def create_refresh_token(user_id: str, multi_login: bool) -> RefreshToken:
    """
    generate encrypted refreshing token only for creating new token

    :param user_id: userID
    :param muldi_login: whether multiple login is allowed
    :return:
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    refresh_token = jwt_encode({'exp': expire, 'sub': user_id})

    if not multi_login:
        key_prefix = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}'
        await redis_client.delete_prefix(key_prefix)

    await redis_client.setex(
        f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{refresh_token}',
        settings.TOKEN_REFRESH_EXPIRE_SECONDS,
        refresh_token,
    )
    return RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=expire)


async def create_new_token(user_id: str, refresh_token: str, multi_login: bool, **kwargs) -> NewToken:
    """
    Generate new token

    :param user_id: userID
    :param update token
    :param muldi_login: whether multiple login is allowed
    :param kwargs: token additional information
    :return:
    """
    redis_refresh_token = await redis_client.get(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{refresh_token}')
    if not redis_refresh_token or redis_refresh_token != refresh_token:
        raise TokenError(msg='Refresh Token expired, please re-entry')
    new_access_token = await create_access_token(user_id, multi_login, **kwargs)
    return NewToken(
        new_access_token=new_access_token.access_token,
        new_access_token_expire_time=new_access_token.access_token_expire_time,
        session_uuid=new_access_token.session_uuid,
    )


async def revoke_token(user_id: str, session_uuid: str) -> None:
    """
    Undo token

    :param user_id: userID
    :param session_uaid: Session ID
    :return:
    """
    token_key = f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}'
    await redis_client.delete(token_key)


def get_token(request: Request) -> str:
    """
    Access to the header token

    :param request: FastAPI
    :return:
    """
    authorization = request.headers.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg='Token is invalid')
    return token


async def get_current_user(db: AsyncSession, pk: int) -> User:
    """
    Get Current User

    :param db: database session
    :param pk: User ID
    :return:
    """
    from backend.app.admin.crud.crud_user import user_dao

    user = await user_dao.get_with_relation(db, user_id=pk)
    if not user:
        raise TokenError(msg='Token is invalid')
    if not user.status:
        raise AuthorizationError(msg='User is locked. Please contact the system administrator')
    if user.dept_id:
        if not user.dept.status:
            raise AuthorizationError(msg='The user\'s department has been locked in')
        if user.dept.del_flag:
            raise AuthorizationError(msg='The user\'s department has been deleted. Please contact the system administrator')
    if user.roles:
        role_status = [role.status for role in user.roles]
        if all(status == 0 for status in role_status):
            raise AuthorizationError(msg='The user\'s role is locked. Please contact the system administrator')
    return user


def superuser_verify(request: Request) -> bool:
    """
    Verify Current User Permissions

    :param request: FastAPI
    :return:
    """
    superuser = request.user.is_superuser
    if not superuser or not request.user.is_staff:
        raise AuthorizationError
    return superuser


async def jwt_authentication(token: str) -> GetUserInfoWithRelationDetail:
    """
    JWT AUTHENTICATION

    :param token: JWT token
    :return:
    """
    token_payload = jwt_decode(token)
    user_id = token_payload.id
    redis_token = await redis_client.get(f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{token_payload.session_uuid}')
    if not redis_token:
        raise TokenError(msg='Token Expired')

    if token != redis_token:
        raise TokenError(msg='Token disabled')

    cache_user = await redis_client.get(f'{settings.JWT_USER_REDIS_PREFIX}:{user_id}')
    if not cache_user:
        async with async_db_session() as db:
            current_user = await get_current_user(db, user_id)
            user = GetUserInfoWithRelationDetail(**select_as_dict(current_user))
            await redis_client.setex(
                f'{settings.JWT_USER_REDIS_PREFIX}:{user_id}',
                settings.JWT_USER_REDIS_EXPIRE_SECONDS,
                user.model_dump_json(),
            )
    else:
        # TODO: REPLACE WITH USE AT THE APPROPRIATE TIME model_validate_json
        # https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing
        user = GetUserInfoWithRelationDetail.model_validate(from_json(cache_user, allow_partial=True))
    return user
