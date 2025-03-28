#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class NoticeSchemaBase(SchemaBase):
    """通知公告基础模型"""

    title: str = Field(description='标题')
    type: int = Field(description='类型（0：通知、1：公告）')
    author: str = Field(description='作者')
    source: str = Field(description='信息来源')
    status: StatusType = Field(StatusType.enable, description='状态（0：隐藏、1：显示）')
    content: str = Field(description='内容')


class CreateNoticeParam(NoticeSchemaBase):
    """创建通知公告参数"""


class UpdateNoticeParam(NoticeSchemaBase):
    """更新通知公告参数"""


class GetNoticeDetail(NoticeSchemaBase):
    """通知公告详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='通知公告 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
