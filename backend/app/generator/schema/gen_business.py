#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field, model_validator
from typing_extensions import Self

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    app_name: str
    table_name_en: str
    table_name_zh: str
    table_simple_name_zh: str
    table_comment: str | None = None
    schema_name: str | None = None
    default_datetime_column: bool = Field(default=True)
    api_version: str = Field(default='v1')
    gen_path: str | None = None
    remark: str | None = None

    @model_validator(mode='after')
    def check_schema_name(self) -> Self:
        if self.schema_name is None:
            self.schema_name = self.table_name_en
        return self


class CreateGenBusinessParam(GenBusinessSchemaBase):
    pass


class UpdateGenBusinessParam(GenBusinessSchemaBase):
    pass


class GetGenBusinessDetail(GenBusinessSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
