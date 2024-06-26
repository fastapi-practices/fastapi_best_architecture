#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field

from backend.common.enums import GenModelType
from backend.common.schema import SchemaBase


class GenModelSchemaBase(SchemaBase):
    name: str
    comment: str | None = None
    type: GenModelType = Field(GenModelType.String, description='模型 column 类型')
    default: str | None = None
    sort: int
    length: int
    is_pk: bool = Field(default=False)
    is_nullable: bool = Field(default=False)
    have_datetime_column: bool = Field(default=False)
    gen_business_id: int | None = Field(ge=1)


class CreateGenModelParam(GenModelSchemaBase):
    pass


class UpdateGenModelParam(GenModelSchemaBase):
    pass


class GetGenModelListDetails(GenModelSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
