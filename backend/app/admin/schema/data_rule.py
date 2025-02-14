#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.schema import SchemaBase


class DataRuleSchemaBase(SchemaBase):
    name: str
    model: str
    column: str
    operator: RoleDataRuleOperatorType = Field(RoleDataRuleOperatorType.OR)
    expression: RoleDataRuleExpressionType = Field(RoleDataRuleExpressionType.eq)
    value: str


class CreateDataRuleParam(DataRuleSchemaBase):
    pass


class UpdateDataRuleParam(DataRuleSchemaBase):
    pass


class GetDataRuleDetail(DataRuleSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None

    def __hash__(self):
        return hash(self.name)
