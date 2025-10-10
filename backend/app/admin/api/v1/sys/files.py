from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from backend.common.dataclasses import UploadUrl
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.utils.file_ops import upload_file, upload_file_verify

router = APIRouter()


@router.post(
    '/upload',
    summary='文件上传',
    dependencies=[
        Depends(RequestPermission('sys:file:upload')),
        DependsRBAC,
    ],
)
async def upload_files(file: Annotated[UploadFile, File()]) -> ResponseSchemaModel[UploadUrl]:
    upload_file_verify(file)
    filename = await upload_file(file)
    return response_base.success(data={'url': f'/static/upload/{filename}'})
