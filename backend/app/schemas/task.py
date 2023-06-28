#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.schemas.base import SchemaBase


class GetTask(SchemaBase):
    id: str
    func_name: str
    trigger: str
    executor: str
    name: str
    misfire_grace_time: str
    coalesce: str
    max_instances: str
    next_run_time: str
