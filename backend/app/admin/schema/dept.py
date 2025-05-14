#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import CustomEmailStr, CustomPhoneNumber, SchemaBase


class DeptSchemaBase(SchemaBase):
    """Sector Foundation Model"""

    name: str = Field(description='Department name')
    parent_id: int | None = Field(None, description='DEPARTMENT PARENT ID')
    sort: int = Field(0, ge=0, description='Sort')
    leader: str | None = Field(None, description='Head')
    phone: CustomPhoneNumber | None = Field(None, description='Call')
    email: CustomEmailStr | None = Field(None, description='Mailbox')
    status: StatusType = Field(StatusType.enable, description='Status')


class CreateDeptParam(DeptSchemaBase):
    """Create sector parameters"""


class UpdateDeptParam(DeptSchemaBase):
    """Update departmental parameters"""


class GetDeptDetail(DeptSchemaBase):
    """Sector details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='SECTOR ID')
    del_flag: bool = Field(description='Delete')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')
