#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    app_name: str
    table_name: str
    table_name_zh: str
    table_simple_name_zh: str
    table_comment: str | None = None
    relate_model_name: str | None = None
    relate_model_fk: int | None = None
    schema_name: str | None = None
    gen_type: int
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
