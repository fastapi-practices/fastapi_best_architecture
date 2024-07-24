#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ConfigSchemaBase(SchemaBase):
    login_title: str = Field(default='登陆 FBA')
    login_sub_title: str = Field(default='fastapi_best_architecture')
    footer: str = Field(default='FBA')
    logo: str = Field(default='Arco')
    system_title: str = Field(default='Arco')
    system_comment: str = Field(
        default='基于 FastAPI 构建的前后端分离 RBAC 权限控制系统，采用独特的伪三层架构模型设计，'
        '内置 fastapi-admin 基本实现，并作为模板库免费开源'
    )


class CreateConfigParam(ConfigSchemaBase):
    pass


class UpdateConfigParam(ConfigSchemaBase):
    pass


class GetConfigListDetails(ConfigSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
