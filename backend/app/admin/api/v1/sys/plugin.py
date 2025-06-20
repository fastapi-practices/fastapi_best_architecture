#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Path, UploadFile
from fastapi.params import Query
from starlette.responses import StreamingResponse

from backend.app.admin.service.plugin_service import plugin_service
from backend.common.enums import PluginType
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


@router.get('/changed', summary='是否存在插件变更', dependencies=[DependsJwtAuth])
async def plugin_changed() -> ResponseSchemaModel[bool]:
    plugins = await plugin_service.changed()
    return response_base.success(data=bool(plugins))


@router.post(
    '',
    summary='安装插件',
    description='使用插件 zip 压缩包或 git 仓库地址进行安装',
    dependencies=[
        Depends(RequestPermission('sys:plugin:install')),
        DependsRBAC,
    ],
)
async def install_plugin(
    type: Annotated[PluginType, Query(description='插件类型')],
    file: Annotated[UploadFile | None, File()] = None,
    repo_url: Annotated[str | None, Query(description='插件 git 仓库地址')] = None,
) -> ResponseModel:
    await plugin_service.install(type=type, file=file, repo_url=repo_url)
    return response_base.success(res=CustomResponseCode.PLUGIN_INSTALL_SUCCESS)


@router.delete(
    '/{plugin}',
    summary='卸载插件',
    description='此操作会直接删除插件依赖，但不会直接删除插件，而是将插件移动到备份目录',
    dependencies=[
        Depends(RequestPermission('sys:plugin:uninstall')),
        DependsRBAC,
    ],
)
async def uninstall_plugin(plugin: Annotated[str, Path(description='插件名称')]) -> ResponseModel:
    await plugin_service.uninstall(plugin=plugin)
    return response_base.success(res=CustomResponseCode.PLUGIN_UNINSTALL_SUCCESS)


@router.put(
    '/{plugin}/status',
    summary='更新插件状态',
    dependencies=[
        Depends(RequestPermission('sys:plugin:edit')),
        DependsRBAC,
    ],
)
async def update_plugin_status(plugin: Annotated[str, Path(description='插件名称')]) -> ResponseModel:
    await plugin_service.update_status(plugin=plugin)
    return response_base.success()


@router.get('/{plugin}', summary='下载插件', dependencies=[DependsJwtAuth])
async def download_plugin(plugin: Annotated[str, Path(description='插件名称')]) -> StreamingResponse:
    bio = await plugin_service.build(plugin=plugin)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={plugin}.zip'},
    )
