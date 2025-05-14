#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.schema import SchemaBase


class DataRuleSchemaBase(SchemaBase):
    """Data rule base model"""

    name: str = Field(description='Rule name')
    model: str = Field(description='Model Name')
    column: str = Field(description='Field Name')
    operator: RoleDataRuleOperatorType = Field(RoleDataRuleOperatorType.AND, description='OPERATOR (AND/OR)')
    expression: RoleDataRuleExpressionType = Field(RoleDataRuleExpressionType.eq, description='Expression Type')
    value: str = Field(description='Rule value')


class CreateDataRuleParam(DataRuleSchemaBase):
    """Create data rule parameters"""


class UpdateDataRuleParam(DataRuleSchemaBase):
    """Update data rule parameters"""


class GetDataRuleDetail(DataRuleSchemaBase):
    """Data rule details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='RULE ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')


class GetDataRuleColumnDetail(SchemaBase):
    """Data rules for model field details"""

    key: str = Field(description='Field name')
    comment: str = Field(description='Field comments')
