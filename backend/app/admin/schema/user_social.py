#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.enums import UserSocialType
from backend.common.schema import SchemaBase


class UserSocialSchemaBase(SchemaBase):
    source: UserSocialType
    open_id: str | None = None
    uid: str | None = None
    union_id: str | None = None
    scope: str | None = None
    code: str | None = None


class CreateUserSocialParam(UserSocialSchemaBase):
    user_id: int


class UpdateUserSocialParam(SchemaBase):
    pass
