#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class NoticeSchemaBase(SchemaBase):
    """Notification bulletin base model"""

    title: str = Field(description='Title')
    type: int = Field(description='Type (0: circular, 1: bulletin)')
    author: str = Field(description='Author')
    source: str = Field(description='Sources of information')
    status: StatusType = Field(StatusType.enable, description='Status (0: hidden, 1: displayed)')
    content: str = Field(description='Contents')


class CreateNoticeParam(NoticeSchemaBase):
    """Create notification bulletin parameters"""


class UpdateNoticeParam(NoticeSchemaBase):
    """Update notification bulletin parameters"""


class GetNoticeDetail(NoticeSchemaBase):
    """Notification of details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='ANNOUNCEMENTS ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')
