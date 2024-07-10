#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field, model_validator
from pydantic.alias_generators import to_pascal

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    app_name: str
    table_name_en: str
    table_name_zh: str
    table_simple_name_zh: str
    table_comment: str | None = None
    schema_name: str | None = None
    have_datetime_column: bool = Field(default=False)
    api_version: str = Field(default='v1')
    gen_path: str | None = None
    remark: str | None = None

    @model_validator(mode='after')
    def check_schema_name(self):
        if self.schema_name is None:
            self.schema_name = to_pascal(self.table_name_en)
        return self


class CreateGenBusinessParam(GenBusinessSchemaBase):
    pass


class UpdateGenBusinessParam(GenBusinessSchemaBase):
    pass


class GetGenBusinessListDetails(GenBusinessSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
