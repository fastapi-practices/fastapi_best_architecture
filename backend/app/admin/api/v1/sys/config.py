#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends

from backend.app.admin.service.config_service import config_service
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/website', summary='获取网站配置信息', dependencies=[DependsJwtAuth])
async def get_website_config() -> ResponseModel:
    config = config_service.get_website()
    return response_base.success(data=config)


@router.post(
    '/website',
    summary='保存网站配置信息',
    dependencies=[
        Depends(RequestPermission('sys:config:add')),
        DependsRBAC,
    ],
)
async def save_website_config() -> ResponseModel:
    await config_service.save_website()
    return response_base.success()


@router.get('/protocol', summary='获取用户协议', dependencies=[DependsJwtAuth])
async def get_protocol_config() -> ResponseModel:
    config = config_service.get_protocol()
    return response_base.success(data=config)


@router.post(
    '/protocol',
    summary='保存用户协议',
    dependencies=[
        Depends(RequestPermission('sys:config:protocol:add')),
        DependsRBAC,
    ],
)
async def save_protocol_config() -> ResponseModel:
    await config_service.save_protocol()
    return response_base.success()


@router.get('/policy', summary='获取用户政策', dependencies=[DependsJwtAuth])
async def get_policy_config() -> ResponseModel:
    config = config_service.get_policy()
    return response_base.success(data=config)


@router.post(
    '/policy',
    summary='保存用户政策',
    dependencies=[
        Depends(RequestPermission('sys:config:policy:add')),
        DependsRBAC,
    ],
)
async def save_policy_config() -> ResponseModel:
    await config_service.save_policy()
    return response_base.success()
