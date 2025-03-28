#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.enums import UserSocialType
from backend.common.schema import SchemaBase


class UserSocialSchemaBase(SchemaBase):
    """用户社交基础模型"""

    source: UserSocialType = Field(description='社交平台')
    open_id: str | None = Field(None, description='开放平台 ID')
    uid: str | None = Field(None, description='用户 ID')
    union_id: str | None = Field(None, description='开放平台唯一 ID')
    scope: str | None = Field(None, description='授权范围')
    code: str | None = Field(None, description='授权码')


class CreateUserSocialParam(UserSocialSchemaBase):
    """创建用户社交参数"""

    user_id: int = Field(description='用户 ID')


class UpdateUserSocialParam(SchemaBase):
    """更新用户社交参数"""
