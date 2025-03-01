#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os.path
import zipfile

from typing import Annotated

from fastapi import APIRouter, File, UploadFile
from fastapi.params import Query

from backend.common.exception import errors
from backend.common.response.response_schema import ResponseModel, response_base
from backend.core.path_conf import PLUGIN_DIR
from backend.plugin.tools import install_requirements_async

router = APIRouter()


@router.post('/install', summary='安装插件', description='需使用插件 zip 压缩包进行安装')
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
            await install_requirements_async(False)

    return response_base.success()


@router.post('/zip', summary='打包插件')
async def build_plugin_zip(plugin: Annotated[str, Query()]): ...
