#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class NoticeSchemaBase(SchemaBase):
    title: str
    type: int
    author: str
    source: str
    status: StatusType = Field(default=StatusType.enable)
    content: str


class CreateNoticeParam(NoticeSchemaBase):
    pass


class UpdateNoticeParam(NoticeSchemaBase):
    pass


class GetNoticeDetail(NoticeSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
