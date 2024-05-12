#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Path, Query

from backend.app.generator.schema.gen_business import CreateGenBusinessParam, UpdateGenBusinessParam
from backend.app.generator.service.gen_business_service import gen_business_service
from backend.app.generator.service.gen_service import gen_service
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/all', summary='获取所有代码生成业务', dependencies=[DependsJwtAuth])
async def get_all_businesses() -> ResponseModel:
    data = await gen_business_service.get_all()
    return await response_base.success(data=data)


@router.get('/businesses/{pk}', summary='获取代码生成业务详情', dependencies=[DependsJwtAuth])
async def get_business(pk: Annotated[int, Path(...)]) -> ResponseModel:
    data = await gen_service.get_business_and_model(pk)
    return await response_base.success(data=data)


@router.post('/businesses', summary='创建代码生成业务', dependencies=[DependsRBAC])
async def create_business(obj: CreateGenBusinessParam) -> ResponseModel:
    await gen_business_service.create(obj=obj)
    return await response_base.success()


@router.put('/businesses/{pk}', summary='更新代码生成业务', dependencies=[DependsRBAC])
async def update_business(pk: Annotated[int, Path(...)], obj: UpdateGenBusinessParam) -> ResponseModel:
    count = await gen_business_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('/businesses', summary='删除代码生成业务', dependencies=[DependsRBAC])
async def delete_business(pk: Annotated[int, Query(...)]) -> ResponseModel:
    count = await gen_business_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.post('/models', summary='创建代码生成模型', dependencies=[DependsRBAC])
async def create_model() -> ResponseModel: ...


@router.put('/models', summary='更新代码生成模型', dependencies=[DependsRBAC])
async def update_model() -> ResponseModel: ...


@router.delete('/models', summary='删除代码生成模型', dependencies=[DependsRBAC])
async def delete_model() -> ResponseModel: ...


@router.get('/preview', summary='生成代码预览', dependencies=[DependsJwtAuth])
async def preview_code() -> ResponseModel:
    data = await gen_service.preview()
    return await response_base.success(data=data)


@router.post('/generate', summary='生成代码', dependencies=[DependsRBAC])
async def generate_code() -> ResponseModel:
    await gen_service.generate()
    return await response_base.success()


@router.post('/download', summary='下载代码', dependencies=[DependsRBAC])
async def download_code() -> ResponseModel:
    await gen_service.download()
    ...
