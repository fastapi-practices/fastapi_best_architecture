#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import StreamingResponse

from backend.app.generator.conf import generator_settings
from backend.app.generator.schema.gen_business import (
    CreateGenBusinessParam,
    GetGenBusinessListDetails,
    UpdateGenBusinessParam,
)
from backend.app.generator.schema.gen_model import CreateGenModelParam, GetGenModelListDetails, UpdateGenModelParam
from backend.app.generator.service.gen_business_service import gen_business_service
from backend.app.generator.service.gen_model_service import gen_model_service
from backend.app.generator.service.gen_service import gen_service
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.utils.serializers import select_as_dict, select_list_serialize

router = APIRouter()


@router.get('/businesses/all', summary='获取所有代码生成业务', dependencies=[DependsJwtAuth])
async def get_all_businesses() -> ResponseModel:
    businesses = await gen_business_service.get_all()
    data = select_list_serialize(businesses)
    return response_base.success(data=data)


@router.get('/businesses/{pk}', summary='获取代码生成业务详情', dependencies=[DependsJwtAuth])
async def get_business(pk: Annotated[int, Path(...)]) -> ResponseModel:
    business = await gen_business_service.get(pk=pk)
    data = GetGenBusinessListDetails(**select_as_dict(business))
    return response_base.success(data=data)


@router.get('/businesses/{pk}/models', summary='获取代码生成业务所有模型', dependencies=[DependsJwtAuth])
async def get_business_models(pk: Annotated[int, Path(...)]) -> ResponseModel:
    models = await gen_model_service.get_by_business(business_id=pk)
    data = select_list_serialize(models)
    return response_base.success(data=data)


@router.post(
    '/businesses',
    summary='创建代码生成业务',
    deprecated=True,
    dependencies=[
        Depends(RequestPermission('gen:code:business:add')),
        DependsRBAC,
    ],
)
async def create_business(obj: CreateGenBusinessParam) -> ResponseModel:
    await gen_business_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/businesses/{pk}',
    summary='更新代码生成业务',
    dependencies=[
        Depends(RequestPermission('gen:code:business:edit')),
        DependsRBAC,
    ],
)
async def update_business(pk: Annotated[int, Path(...)], obj: UpdateGenBusinessParam) -> ResponseModel:
    count = await gen_business_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/businesses/{pk}',
    summary='删除代码生成业务',
    dependencies=[
        Depends(RequestPermission('gen:code:business:del')),
        DependsRBAC,
    ],
)
async def delete_business(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await gen_business_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/models/types', summary='获取代码生成模型列类型', dependencies=[DependsJwtAuth])
async def get_model_types() -> ResponseModel:
    model_types = await gen_model_service.get_types()
    return response_base.success(data=model_types)


@router.get('/models/{pk}', summary='获取代码生成模型详情', dependencies=[DependsJwtAuth])
async def get_model(pk: Annotated[int, Path(...)]) -> ResponseModel:
    model = await gen_model_service.get(pk=pk)
    data = GetGenModelListDetails(**select_as_dict(model))
    return response_base.success(data=data)


@router.post(
    '/models',
    summary='创建代码生成模型',
    dependencies=[
        Depends(RequestPermission('gen:code:model:add')),
        DependsRBAC,
    ],
)
async def create_model(obj: CreateGenModelParam) -> ResponseModel:
    await gen_model_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/models/{pk}',
    summary='更新代码生成模型',
    dependencies=[
        Depends(RequestPermission('gen:code:model:edit')),
        DependsRBAC,
    ],
)
async def update_model(pk: Annotated[int, Path(...)], obj: UpdateGenModelParam) -> ResponseModel:
    count = await gen_model_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/models/{pk}',
    summary='删除代码生成模型',
    dependencies=[
        Depends(RequestPermission('gen:code:model:del')),
        DependsRBAC,
    ],
)
async def delete_model(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await gen_model_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/tables', summary='获取数据库表', dependencies=[DependsRBAC])
async def get_all_tables(table_schema: Annotated[str, Query(..., description='数据库名')] = 'fba') -> ResponseModel:
    data = await gen_service.get_tables(table_schema=table_schema)
    return response_base.success(data=data)


@router.post(
    '/import',
    summary='导入代码生成业务和模型列',
    dependencies=[
        Depends(RequestPermission('gen:code:import')),
        DependsRBAC,
    ],
)
async def import_table(
    app: Annotated[str, Body(..., description='应用名称，用于代码生成到指定 app')],
    table_name: Annotated[str, Body(..., description='数据库表名')],
    table_schema: Annotated[str, Body(..., description='数据库名')] = 'fba',
) -> ResponseModel:
    await gen_service.import_business_and_model(app=app, table_schema=table_schema, table_name=table_name)
    return response_base.success()


@router.get('/preview/{pk}', summary='生成代码预览', dependencies=[DependsJwtAuth])
async def preview_code(pk: Annotated[int, Path(..., description='业务ID')]) -> ResponseModel:
    data = await gen_service.preview(pk=pk)
    return response_base.success(data=data)


@router.get('/generate/{pk}/path', summary='获取代码生成路径', dependencies=[DependsJwtAuth])
async def generate_path(pk: Annotated[int, Path(..., description='业务ID')]):
    data = await gen_service.get_generate_path(pk=pk)
    return response_base.success(data=data)


@router.post(
    '/generate/{pk}',
    summary='代码生成',
    description='文件磁盘写入，请谨慎操作',
    dependencies=[
        Depends(RequestPermission('gen:code:generate')),
        DependsRBAC,
    ],
)
async def generate_code(pk: Annotated[int, Path(..., description='业务ID')]) -> ResponseModel:
    await gen_service.generate(pk=pk)
    return response_base.success()


@router.get('/download/{pk}', summary='下载代码', dependencies=[DependsJwtAuth])
async def download_code(pk: Annotated[int, Path(..., description='业务ID')]):
    bio = await gen_service.download(pk=pk)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={generator_settings.DOWNLOAD_ZIP_FILENAME}.zip'},
    )
