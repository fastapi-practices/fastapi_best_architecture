from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_rule import GetDataRuleDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DataScopeBase(SchemaBase):
    """数据范围基础模型"""

    name: str = Field(description='名称')
    status: StatusType = Field(description='状态')


class CreateDataScopeParam(DataScopeBase):
    """创建数据范围参数"""


class UpdateDataScopeParam(DataScopeBase):
    """更新数据范围参数"""


class UpdateDataScopeRuleParam(SchemaBase):
    """更新数据范围规则参数"""

    rules: list[int] = Field(description='数据规则 ID 列表')


class DeleteDataScopeParam(SchemaBase):
    """删除数据范围参数"""

    pks: list[int] = Field(description='数据范围 ID 列表')


class GetDataScopeDetail(DataScopeBase):
    """数据范围详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='数据范围 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')


class GetDataScopeWithRelationDetail(GetDataScopeDetail):
    """数据范围关联详情"""

    rules: list[GetDataRuleDetail] = Field([], description='数据规则列表')
