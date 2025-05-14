#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    """Code Generation Business Base Model"""

    app_name: str = Field(description='Application name (English)')
    table_name: str = Field(description='Table name (English)')
    doc_comment: str = Field(description='Document Comment (for function/parameter documents)')
    table_comment: str | None = Field(None, description='Table Description')
    class_name: str | None = Field(None, description='Basic class name (default is the English Table name)')
    schema_name: str | None = Field(None, description='Schema Name (Default is Table Name)')
    filename: str | None = Field(None, description='Base File Name (default is the English Table Name)')
    default_datetime_column: bool = Field(True, description='Existence of default timebar')
    api_version: str = Field('v1', description='code generation api version')
    gen_path: str | None = Field(None, description='code generation path (default app root path)')
    remark: str | None = Field(None, description='Remarks')


class CreateGenBusinessParam(GenBusinessSchemaBase):
    """Create code generation business parameters"""


class UpdateGenBusinessParam(GenBusinessSchemaBase):
    """Update code generation business parameters"""


class GetGenBusinessDetail(GenBusinessSchemaBase):
    """Get code generation details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='PRIMARY ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')
