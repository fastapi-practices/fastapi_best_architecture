from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


WorkflowConfigValue = dict[str, Any] | list[Any] | str | None


class WorkflowDefinitionSchemaBase(SchemaBase):
    category_id: int | None = Field(None, description='分类ID')
    name: str = Field(description='流程名称')
    code: str = Field(description='流程编码')
    description: str | None = Field(None, description='描述')
    form_config: WorkflowConfigValue = Field(None, description='表单配置')
    flow_config: WorkflowConfigValue = Field(None, description='流程配置')
    status: int = Field(0, description='状态')
    allow_withdraw: bool = Field(True, description='允许撤回')
    allow_urge: bool = Field(True, description='允许催办')


class CreateWorkflowDefinitionParam(WorkflowDefinitionSchemaBase):
    pass


class UpdateWorkflowDefinitionParam(WorkflowDefinitionSchemaBase):
    pass


class GetWorkflowDefinitionDetail(WorkflowDefinitionSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None


class PreviewWorkflowFlowItem(SchemaBase):
    node_id: str = Field(description='节点ID')
    node_type: str = Field(description='节点类型')
    label: str = Field(description='节点名称')
    assignee_id: int | None = Field(None, description='审批人ID')
    assignee_name: str | None = Field(None, description='审批人显示名')
    self_select_options: list[int] = Field(default_factory=list, description='自选审批范围')
    self_select_option_labels: dict[int, str] = Field(default_factory=dict, description='自选审批人名称映射')


class PreviewWorkflowFlowResponse(SchemaBase):
    items: list[PreviewWorkflowFlowItem] = Field(default_factory=list, description='审批链预览')
