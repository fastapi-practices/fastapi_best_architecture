from pydantic import Field

from backend.common.schema import SchemaBase


class CodeGenTableQueryParam(SchemaBase):
    """代码生成表查询参数"""

    table_schema: str = Field('fba', description='数据库名')


class ImportParam(SchemaBase):
    """导入参数"""

    app: str = Field(description='应用名称，用于代码生成到指定 app')
    table_schema: str = Field(description='数据库名')
    table_name: str = Field(description='数据库表名')
