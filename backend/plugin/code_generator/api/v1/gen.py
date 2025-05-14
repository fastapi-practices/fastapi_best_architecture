#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import StreamingResponse

from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.plugin.code_generator.conf import generator_settings
from backend.plugin.code_generator.schema.gen import ImportParam
from backend.plugin.code_generator.service.gen_service import gen_service

router = APIRouter()


@router.get('/tables', summary='Access to database tables')
async def get_all_tables(
    table_schema: Annotated[str, Query(description='Database Name')] = 'fba',
) -> ResponseSchemaModel[list[str]]:
    data = await gen_service.get_tables(table_schema=table_schema)
    return response_base.success(data=data)


@router.post(
    '/import',
    summary='Import code generation business and model bar',
    dependencies=[
        Depends(RequestPermission('gen:code:import')),
        DependsRBAC,
    ],
)
async def import_table(obj: ImportParam) -> ResponseModel:
    await gen_service.import_business_and_model(obj=obj)
    return response_base.success()


@router.get('/preview/{pk}', summary='Generate code preview', dependencies=[DependsJwtAuth])
async def preview_code(pk: Annotated[int, Path(description='OPERATIONS ID')]) -> ResponseSchemaModel[dict[str, bytes]]:
    data = await gen_service.preview(pk=pk)
    return response_base.success(data=data)


@router.get('/generate/{pk}/path', summary='Get code generation path', dependencies=[DependsJwtAuth])
async def generate_path(pk: Annotated[int, Path(description='OPERATIONS ID')]) -> ResponseSchemaModel[list[str]]:
    data = await gen_service.get_generate_path(pk=pk)
    return response_base.success(data=data)


@router.post(
    '/generate/{pk}',
    summary='Code Generation',
    description='File disk written. Please be careful',
    dependencies=[
        Depends(RequestPermission('gen:code:generate')),
        DependsRBAC,
    ],
)
async def generate_code(pk: Annotated[int, Path(description='OPERATIONS ID')]) -> ResponseModel:
    await gen_service.generate(pk=pk)
    return response_base.success()


@router.get('/download/{pk}', summary='Download Code', dependencies=[DependsJwtAuth])
async def download_code(pk: Annotated[int, Path(description='OPERATIONS ID')]):
    bio = await gen_service.download(pk=pk)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={generator_settings.DOWNLOAD_ZIP_FILENAME}.zip'},
    )
