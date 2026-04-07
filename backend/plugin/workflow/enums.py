from enum import Enum


class WorkflowDefinitionStatus(int, Enum):
    draft = 0
    published = 1
    disabled = 2


class WorkflowInstanceStatus(str, Enum):
    draft = 'DRAFT'
    running = 'RUNNING'
    approved = 'APPROVED'
    rejected = 'REJECTED'
    withdrawn = 'WITHDRAWN'
    cancelled = 'CANCELLED'


class WorkflowTaskStatus(str, Enum):
    pending = 'PENDING'
    approved = 'APPROVED'
    rejected = 'REJECTED'
    cancelled = 'CANCELLED'


class WorkflowMessageType(str, Enum):
    pending_approval = 'PENDING_APPROVAL'
    approved = 'APPROVED'
    rejected = 'REJECTED'
    withdrawn = 'WITHDRAWN'
