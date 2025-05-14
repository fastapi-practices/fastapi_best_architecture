#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field, field_validator

from backend.common.schema import SchemaBase
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_sqlalchemy


class GenModelSchemaBase(SchemaBase):
    """Code Generation Model Foundation Model"""

    name: str = Field(description='Column Name')
    comment: str | None = Field(None, description='Column Description')
    type: str = Field(description='SQLA MODEL COLUMN TYPE')
    default: str | None = Field(None, description='Column Default')
    sort: int = Field(description='Column Sort')
    length: int = Field(description='Column Length')
    is_pk: bool = Field(False, description='Whether the primary key')
    is_nullable: bool = Field(False, description='Could it be empty')
    gen_business_id: int = Field(description='CODE GENERATION BUSINESS ID')

    @field_validator('type')
    @classmethod
    def type_update(cls, v: str) -> str:
        """Update column type"""
        return sql_type_to_sqlalchemy(v)


class CreateGenModelParam(GenModelSchemaBase):
    """Create code generation model parameters"""


class UpdateGenModelParam(GenModelSchemaBase):
    """Update code generation model parameters"""


class GetGenModelDetail(GenModelSchemaBase):
    """Get code generation model details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='PRIMARY ID')
    pd_type: str = Field(description='pydantic type for column type')
