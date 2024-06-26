#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import GenType
from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    app_name: str
    table_name_en: str
    table_name_zh: str
    table_simple_name_zh: str
    table_comment: str | None = None
    # relate_model_name: str | None = None
    # relate_model_fk: int | None = None
    schema_name: str | None = None
    have_datetime_column: bool = Field(default=False)
    gen_type: GenType = Field(default=GenType.gz, description='代码生成类型（0：自定义路径 1：内部写入 2：压缩包）')
    gen_path: str | None = None
    remark: str | None = None


class CreateGenBusinessParam(GenBusinessSchemaBase):
    pass


class UpdateGenBusinessParam(GenBusinessSchemaBase):
    pass


class GetGenBusinessListDetails(GenBusinessSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
