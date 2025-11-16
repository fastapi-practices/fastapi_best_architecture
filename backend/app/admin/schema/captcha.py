from pydantic import Field

from backend.common.schema import SchemaBase


class GetCaptchaDetail(SchemaBase):
    """验证码详情"""

    is_enabled: bool = Field(description='是否启用')
    expire_seconds: int = Field(description='过期秒数')
    uuid: str = Field(description='图片唯一标识')
    image: str = Field(description='图片内容')
