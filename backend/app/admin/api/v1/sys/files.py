from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from fastapi import File, Depends, APIRouter

from backend.utils.file_ops import upload_file, upload_file_verify
from backend.common.security.rbac import DependsRBAC
from backend.common.security.permission import RequestPermission
from backend.common.response.response_schema import response_base

if TYPE_CHECKING:
    from fastapi import UploadFile

    from backend.common.dataclasses import UploadUrl
    from backend.common.response.response_schema import ResponseSchemaModel

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
