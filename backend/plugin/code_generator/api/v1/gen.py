#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import StreamingResponse

from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.plugin.code_generator.schema.gen import ImportParam
from backend.plugin.code_generator.service.gen_service import gen_service

router = APIRouter()


@router.get('', summary='获取数据库表')
async def get_all_tables(
    table_schema: Annotated[str, Query(description='数据库名')] = 'fba',
) -> ResponseSchemaModel[list[str]]:
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
async def import_table(obj: ImportParam) -> ResponseModel:
    await gen_service.import_business_and_model(obj=obj)
    return response_base.success()


@router.get('/{pk}/preview', summary='生成代码预览', dependencies=[DependsJwtAuth])
async def preview_code(pk: Annotated[int, Path(description='业务 ID')]) -> ResponseSchemaModel[dict[str, bytes]]:
    data = await gen_service.preview(pk=pk)
    return response_base.success(data=data)


@router.get('/{pk}/code/path', summary='获取代码生成路径', dependencies=[DependsJwtAuth])
async def generate_path(pk: Annotated[int, Path(description='业务 ID')]) -> ResponseSchemaModel[list[str]]:
    data = await gen_service.get_generate_path(pk=pk)
    return response_base.success(data=data)


@router.post(
    '/{pk}/code',
    summary='代码生成',
    description='文件磁盘写入，请谨慎操作',
    dependencies=[
        Depends(RequestPermission('gen:code:write')),
        DependsRBAC,
    ],
)
async def generate_code(pk: Annotated[int, Path(description='业务 ID')]) -> ResponseModel:
    await gen_service.generate(pk=pk)
    return response_base.success()


@router.get('/{pk}', summary='下载代码', dependencies=[DependsJwtAuth])
async def download_code(pk: Annotated[int, Path(description='业务 ID')]):
    bio = await gen_service.download(pk=pk)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={settings.CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME}.zip'},
    )
