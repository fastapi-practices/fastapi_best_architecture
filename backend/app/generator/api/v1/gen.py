#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Path

from backend.app.generator.service.gen_service import gen_service
from backend.common.response.response_schema import ResponseModel, response_base

router = APIRouter()


@router.get('/all', summary='获取代码生成业务表列表')
async def get_all_dbs():
    data = await gen_service.get_all()
    return await response_base.success(data=data)


@router.get('/{pk}', summary='获取代码生成业务model表详情')
async def get_db(pk: Annotated[int, Path(...)]):
    data = await gen_service.get(pk)
    return await response_base.success(data=data)


@router.post('/db', summary='创建代码生成业务表')
async def create_db(): ...


@router.put('/db', summary='更新代码生成业务表')
async def update_db(): ...


@router.delete('/db', summary='删除代码生成业务表')
async def delete_db(): ...


@router.post('/model', summary='创建代码生成model表')
async def create_model(): ...


@router.put('/model', summary='更新代码生成model表')
async def update_model(): ...


@router.delete('/model', summary='删除代码生成model表')
async def delete_model(): ...


@router.get('/preview', summary='生成代码预览')
async def preview_code() -> ResponseModel:
    data = await gen_service.get_preview()
    return await response_base.success(data=data)


@router.post('/generate', summary='生成代码')
async def generate_code():
    await gen_service.generate()
    return await response_base.success()


@router.post('/download', summary='下载代码')
async def download_code():
    await gen_service.download()
    ...
