#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.schema import SchemaBase


class GetCaptchaDetail(SchemaBase):
    """验证码详情"""

    image_type: str = Field(description='图片类型')
    image: str = Field(description='图片内容')
