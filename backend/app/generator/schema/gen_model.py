#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field, field_validator

from backend.common.schema import SchemaBase
from backend.utils.type_conversion import sql_type_to_sqlalchemy


class GenModelSchemaBase(SchemaBase):
    name: str
    comment: str | None = None
    type: str
    default: str | None = None
    sort: int
    length: int
    is_pk: bool = Field(default=False)
    is_nullable: bool = Field(default=False)
    gen_business_id: int | None = Field(ge=1)

    @field_validator('type')
    @classmethod
    def type_update(cls, v):
        return sql_type_to_sqlalchemy(v)


class CreateGenModelParam(GenModelSchemaBase):
    pass


class UpdateGenModelParam(GenModelSchemaBase):
    pass


class GetGenModelDetail(GenModelSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pd_type: str
