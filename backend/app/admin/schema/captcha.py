#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.schema import SchemaBase


class GetCaptchaDetail(SchemaBase):
    """Authentication code details"""

    image_type: str = Field(description='Picture Type')
    image: str = Field(description='Picture content')
