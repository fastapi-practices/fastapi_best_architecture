from backend.common.schema import SchemaBase


class TaskRegisteredDetail(SchemaBase):
    name: str
    task: str
