#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_rule import GetDataRuleDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DataScopeBase(SchemaBase):
    """Data range base model"""

    name: str = Field(description='Name')
    status: StatusType = Field(StatusType.enable, description='Status')


class CreateDataScopeParam(DataScopeBase):
    """Create data range parameters"""


class UpdateDataScopeParam(DataScopeBase):
    """Update data range parameters"""


class UpdateDataScopeRuleParam(SchemaBase):
    """Update data range rule parameters"""

    rules: list[int] = Field(description='DATA RULE ID LIST')


class GetDataScopeDetail(DataScopeBase):
    """Data range details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='DATA RANGE ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')


class GetDataScopeWithRelationDetail(GetDataScopeDetail):
    """Details of data range linkages"""

    rules: list[GetDataRuleDetail] = Field([], description='Data Rule List')
