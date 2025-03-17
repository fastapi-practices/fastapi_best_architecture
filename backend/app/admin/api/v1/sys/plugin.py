#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os.path
import zipfile

from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.params import Query
from starlette.responses import StreamingResponse

from backend.common.exception import errors
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.path_conf import PLUGIN_DIR
from backend.plugin.tools import install_requirements_async

router = APIRouter()


@router.post(
    '/install',
    summary='安装插件',
    description='需使用插件 zip 压缩包进行安装',
    dependencies=[
        Depends(RequestPermission('sys:plugin:install')),
        DependsRBAC,
    ],
)
async def install_plugin(file: Annotated[UploadFile, File()]) -> ResponseModel:
    contents = await file.read()
    file_bytes = io.BytesIO(contents)
    if not zipfile.is_zipfile(file_bytes):
        raise errors.ForbiddenError(msg='插件压缩包格式非法')
    with zipfile.ZipFile(file_bytes) as zf:
        # 校验压缩包
        plugin_dir_in_zip = f'{file.filename[:-4]}/backend/plugin/'
        members_in_plugin_dir = [name for name in zf.namelist() if name.startswith(plugin_dir_in_zip)]
        if not members_in_plugin_dir:
            raise errors.ForbiddenError(msg='插件压缩包内容非法')
        plugin_name = members_in_plugin_dir[1].replace(plugin_dir_in_zip, '').replace('/', '')
        if (
            len(members_in_plugin_dir) <= 3
            or f'{plugin_dir_in_zip}{plugin_name}/plugin.toml' not in members_in_plugin_dir
            or f'{plugin_dir_in_zip}{plugin_name}/README.md' not in members_in_plugin_dir
        ):
            raise errors.ForbiddenError(msg='插件压缩包内缺少必要文件')

        # 插件是否可安装
        full_plugin_path = os.path.join(PLUGIN_DIR, plugin_name)
        if os.path.exists(full_plugin_path):
            raise errors.ForbiddenError(msg='此插件已安装')
        os.makedirs(full_plugin_path)

        # 解压安装
        members = []
        for member in zf.infolist():
            if member.filename.startswith(plugin_dir_in_zip):
                member.filename = member.filename.replace(plugin_dir_in_zip, '')
                if not member.filename:
                    continue
                members.append(member)
        zf.extractall(PLUGIN_DIR, members)
        if os.path.exists(os.path.join(full_plugin_path, 'requirements.txt')):
            await install_requirements_async()

    return response_base.success()


@router.post(
    '/zip',
    summary='打包插件',
    dependencies=[
        Depends(RequestPermission('sys:plugin:zip')),
        DependsRBAC,
    ],
)
async def build_plugin_zip(plugin: Annotated[str, Query()]):
    plugin_dir = os.path.join(PLUGIN_DIR, plugin)
    if not os.path.exists(plugin_dir):
        raise errors.ForbiddenError(msg='插件不存在')
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, 'w') as zf:
        for root, dirs, files in os.walk(plugin_dir):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=plugin_dir)
                zf.write(file_path, arcname)
    bio.seek(0)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={plugin}.zip'},
    )
