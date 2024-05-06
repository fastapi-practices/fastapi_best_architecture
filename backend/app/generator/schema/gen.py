#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    app_name: str
    model_name: str
    model_name_zh: str
    model_simple_name_zh: str
    model_comment: str | None = None
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


class GenModelSchemaBase(SchemaBase):
    name: str
    comment: str | None = None
    type: str
    default: str | None = None
    length: int
    is_pk: bool
    is_nullable: bool


class CreateGenModel(GenModelSchemaBase):
    pass


class UpdateGenModel(GenModelSchemaBase):
    pass


class GetGenModelListDetails(GenModelSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    gen_business_id: int
