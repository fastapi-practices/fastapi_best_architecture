#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from backend.common.dataclasses import UploadUrl
from backend.common.enums import FileType
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.utils.file_ops import file_verify, upload_file

router = APIRouter()


@router.post('/image', summary='上传图片', dependencies=[DependsJwtAuth])
async def upload_image(file: Annotated[UploadFile, File()]) -> ResponseSchemaModel[UploadUrl]:
    file_verify(file, FileType.image)
    filename = await upload_file(file)
    return response_base.success(data={'url': f'/static/upload/{filename}'})


@router.post('/video', summary='上传视频', dependencies=[DependsJwtAuth])
async def upload_video(file: Annotated[UploadFile, File()]) -> ResponseSchemaModel[UploadUrl]:
    file_verify(file, FileType.video)
    filename = await upload_file(file)
    return response_base.success(data={'url': f'/static/upload/{filename}'})
