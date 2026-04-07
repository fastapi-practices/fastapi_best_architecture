from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase
from backend.plugin.workflow.schema.message import GetWorkflowMessageDetail


class StartWorkflowInstanceParam(SchemaBase):
    definition_id: int = Field(description='流程定义ID')
    title: str = Field(description='标题')
    remark: str | None = Field(None, description='备注')
    form_data: dict[str, Any] = Field(default_factory=dict, description='表单数据')
    self_select_assignees: dict[str, int] = Field(default_factory=dict, description='自选审批人')


class GetWorkflowInstanceDetail(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    instance_no: str
    definition_id: int
    title: str
    initiator_id: int
    status: str
    current_task_id: int | None = None
    form_data: dict[str, Any] | str | None = None
    remark: str | None = None
    todo_count: int | None = None
    allow_withdraw: bool | None = None
    allow_urge: bool | None = None
    messages: list[GetWorkflowMessageDetail] = Field(default_factory=list, description='流程消息列表')
    created_time: datetime
    updated_time: datetime | None = None
