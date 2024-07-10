#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field, field_validator

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
    gen_business_id: int | None = Field(ge=1)

    @field_validator('type')
    @classmethod
    def sql_type_to_python(cls, v: GenModelType):
        type_mapping = {
            GenModelType.CHAR: 'str',
            GenModelType.VARCHAR: 'str',
            GenModelType.String: 'str',
            GenModelType.TEXT: 'str',
            GenModelType.Text: 'str',
            GenModelType.LONGTEXT: 'str',
            GenModelType.UnicodeText: 'str',
            GenModelType.INT: 'int',
            GenModelType.INTEGER: 'int',
            GenModelType.Integer: 'int',
            GenModelType.BigInteger: 'int',
            GenModelType.SmallInteger: 'int',
            GenModelType.BIGINT: 'int',
            GenModelType.SMALLINT: 'int',
            GenModelType.FLOAT: 'float',
            GenModelType.Float: 'float',
            GenModelType.Boolean: 'bool',
            GenModelType.DECIMAL: 'decimal',
            GenModelType.UUID: 'UUID',
            GenModelType.Uuid: 'UUID',
        }
        return type_mapping.get(v) or v


class CreateGenModelParam(GenModelSchemaBase):
    pass


class UpdateGenModelParam(GenModelSchemaBase):
    pass


class GetGenModelListDetails(GenModelSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
