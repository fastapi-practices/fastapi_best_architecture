from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class LoginRequest(SchemaBase):
    """AD 域认证登录请求"""

    username: str = Field(description='AD 用户名或邮箱')
    password: str = Field(description='AD 密码')


class UserInfo(SchemaBase):
    """用户基本信息"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='用户 ID')
    uuid: str = Field(description='用户 UUID')
    username: str = Field(description='用户名')
    nickname: str = Field(description='昵称')
    email: str | None = Field(None, description='邮箱')
    auth_provider: str = Field('local', description='认证提供方')


class LoginResponse(SchemaBase):
    """AD 域认证登录响应"""

    access_token: str = Field(description='访问令牌')
    access_token_expire_time: datetime = Field(description='令牌过期时间')
    session_uuid: str = Field(description='会话 UUID')
    token_type: str = Field('bearer', description='令牌类型')
    user: UserInfo = Field(description='用户信息')
