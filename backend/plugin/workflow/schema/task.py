from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ApproveWorkflowTaskParam(SchemaBase):
    comment: str | None = Field(None, description='审批意见')


class RejectWorkflowTaskParam(SchemaBase):
    comment: str | None = Field(None, description='拒绝意见')


class GetWorkflowTaskDetail(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    instance_id: int
    definition_id: int
    task_name: str
    assignee_id: int
    node_key: str | None = None
    status: str
    comment: str | None = None
    sort: int
    completed_time: str | None = None
    created_time: datetime
    updated_time: datetime | None = None
