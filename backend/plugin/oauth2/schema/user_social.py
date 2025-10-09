from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from backend.common.schema import SchemaBase

if TYPE_CHECKING:
    from backend.common.enums import UserSocialType


class UserSocialSchemaBase(SchemaBase):
    """用户社交基础模型"""

    sid: str = Field(description='第三方用户 ID')
    source: UserSocialType = Field(description='社交平台')


class CreateUserSocialParam(UserSocialSchemaBase):
    """创建用户社交参数"""

    user_id: int = Field(description='用户 ID')


class UpdateUserSocialParam(SchemaBase):
    """更新用户社交参数"""
