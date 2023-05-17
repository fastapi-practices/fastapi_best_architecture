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


def create_access_token(data: int | Any, expires_delta: timedelta | None = None) -> str:
    """
    Generate encryption token

    :param data: Data transferred to the token
    :param expires_delta: Increased expiry time
    :return:
    """
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(settings.TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expires, 'sub': str(data[0]), 'role_ids': str(data[1])}
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    return encoded_jwt


async def get_current_user(db: CurrentSession, token: str = Depends(oauth2_schema)) -> User:
    """
    Get the current user through tokens

    :param db:
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = payload.get('sub')
        user_role = payload.get('role_ids')
        if not user_id or not user_role:
            raise TokenError
    except (jwt.JWTError, ValidationError):
        raise TokenError
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
# Permission dependency injection
DependsUser = Depends(get_current_user)
DependsSuperUser = Depends(get_current_is_superuser)
