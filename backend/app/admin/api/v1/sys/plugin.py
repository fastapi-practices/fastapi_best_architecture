#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Path, UploadFile
from fastapi.params import Query
from starlette.responses import StreamingResponse

from backend.app.admin.service.plugin_service import plugin_service
from backend.common.response.response_code import CustomResponseCode
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('', summary='获取所有插件', dependencies=[DependsJwtAuth])
async def get_all_plugins() -> ResponseSchemaModel[list[dict[str, Any]]]:
    plugins = await plugin_service.get_all()
    return response_base.success(data=plugins)


@router.get('/changes', summary='插件状态是否变更', dependencies=[DependsJwtAuth])
async def plugin_changed() -> ResponseSchemaModel[bool]:
    plugins = await plugin_service.changed()
    return response_base.success(data=bool(plugins))


@router.post(
    '/zip',
    summary='安装 zip 插件',
    description='使用插件 zip 压缩包进行安装',
    dependencies=[
        Depends(RequestPermission('sys:plugin:zip')),
        DependsRBAC,
    ],
)
async def install_zip_plugin(file: Annotated[UploadFile, File()]) -> ResponseModel:
    await plugin_service.install_zip(file=file)
    return response_base.success(res=CustomResponseCode.PLUGIN_INSTALL_SUCCESS)


@router.post(
    '/git',
    summary='安装 git 插件',
    description='使用插件 git 仓库地址进行安装，不限制平台；如果需要凭证，需在 git 仓库地址中添加凭证信息',
    dependencies=[
        Depends(RequestPermission('sys:plugin:git')),
        DependsRBAC,
    ],
)
async def install_git_plugin(repo_url: Annotated[str, Query(description='插件 git 仓库地址')]) -> ResponseModel:
    await plugin_service.install_git(repo_url=repo_url)
    return response_base.success(res=CustomResponseCode.PLUGIN_INSTALL_SUCCESS)


@router.delete(
    '/{plugin}',
    summary='卸载插件',
    description='此操作会直接删除插件依赖，但不会直接删除插件，而是将插件移动到备份目录',
    dependencies=[
        Depends(RequestPermission('sys:plugin:del')),
        DependsRBAC,
    ],
)
async def uninstall_plugin(plugin: Annotated[str, Path(description='插件名称')]) -> ResponseModel:
    await plugin_service.uninstall(plugin=plugin)
    return response_base.success(res=CustomResponseCode.PLUGIN_UNINSTALL_SUCCESS)


@router.post(
    '/{plugin}/status',
    summary='更新插件状态',
    dependencies=[
        Depends(RequestPermission('sys:plugin:status')),
        DependsRBAC,
    ],
)
async def update_plugin_status(plugin: Annotated[str, Path(description='插件名称')]) -> ResponseModel:
    await plugin_service.update_status(plugin=plugin)
    return response_base.success()


@router.get(
    '/{plugin}',
    summary='打包并下载插件',
    dependencies=[
        Depends(RequestPermission('sys:plugin:zip')),
        DependsRBAC,
    ],
)
async def build_plugin(plugin: Annotated[str, Path(description='插件名称')]) -> StreamingResponse:
    bio = await plugin_service.build(plugin=plugin)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={plugin}.zip'},
    )
