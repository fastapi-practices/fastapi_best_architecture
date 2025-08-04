#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.schema import SchemaBase


class TaskRegisteredDetail(SchemaBase):
    name: str
    task: str
