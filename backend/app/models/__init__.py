#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 导入所有模型，并将 Base 放在最前面， 以便 Base 拥有它们
# imported by Alembic
"""
from backend.app.database.base_class import MappedBase  # noqa
from backend.app.models.user import User
