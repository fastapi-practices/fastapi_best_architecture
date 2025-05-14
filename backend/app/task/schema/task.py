#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from pydantic import Field

from backend.common.schema import SchemaBase


class RunParam(SchemaBase):
    """Task running parameters"""

    name: str = Field(description='Task Name')
    args: list[Any] | None = Field(None, description='Task Function Location Parameters')
    kwargs: dict[str, Any] | None = Field(None, description='Task function keyword parameters')


class TaskResult(SchemaBase):
    """Results of mandate implementation"""

    result: str = Field(description='Results of mandate implementation')
    traceback: str = Field(description='Error stacking information')
    status: str = Field(description='Task Status')
    name: str = Field(description='Task Name')
    args: list[Any] | None = Field(None, description='Task Function Location Parameters')
    kwargs: dict[str, Any] | None = Field(None, description='Task function keyword parameters')
    worker: str = Field(description='worker of the mission')
    retries: int | None = Field(None, description='Number of retries')
    queue: str | None = Field(None, description='Task Queue')
