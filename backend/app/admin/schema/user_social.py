#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.enums import UserSocialType
from backend.common.schema import SchemaBase


class UserSocialSchemaBase(SchemaBase):
    """User social infrastructure model"""

    source: UserSocialType = Field(description='Social platform')
    open_id: str | None = Field(None, description='OPEN PLATFORM ID')
    uid: str | None = Field(None, description='USER ID')
    union_id: str | None = Field(None, description='OPEN PLATFORM ONLY ID')
    scope: str | None = Field(None, description='Scope of authorization')
    code: str | None = Field(None, description='Authorization Code')


class CreateUserSocialParam(UserSocialSchemaBase):
    """Create user social parameters"""

    user_id: int = Field(description='USER ID')


class UpdateUserSocialParam(SchemaBase):
    """Update user social parameters"""
