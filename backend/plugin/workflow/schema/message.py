from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class GetWorkflowMessageDetail(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    receiver_id: int
    instance_id: int | None = None
    task_id: int | None = None
    message_type: str
    title: str
    content: str
    is_read: bool
    created_time: datetime
    updated_time: datetime | None = None
