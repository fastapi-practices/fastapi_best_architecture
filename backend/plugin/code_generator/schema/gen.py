#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.schema import SchemaBase


class ImportParam(SchemaBase):
    """Import parameters"""

    app: str = Field(description='apply name for code generation to specify app')
    table_schema: str = Field(description='Database Name')
    table_name: str = Field(description='Database Table Name')
