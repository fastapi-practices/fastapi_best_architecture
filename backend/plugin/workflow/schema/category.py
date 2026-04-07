from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class WorkflowCategorySchemaBase(SchemaBase):
    name: str = Field(description='分类名称')
    code: str = Field(description='分类编码')
    icon: str | None = Field(None, description='图标')
    sort: int = Field(0, description='排序')
    status: int = Field(1, description='状态')
    remark: str | None = Field(None, description='备注')


class CreateWorkflowCategoryParam(WorkflowCategorySchemaBase):
    pass


class UpdateWorkflowCategoryParam(WorkflowCategorySchemaBase):
    pass


class GetWorkflowCategoryDetail(WorkflowCategorySchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
