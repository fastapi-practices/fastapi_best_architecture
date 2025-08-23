#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境和变量管理API
"""
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse

from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.plugin.api_testing.utils.environment import (
    EnvironmentManager, EnvironmentModel, VariableManager, VariableModel,
    VariableScope, EnvironmentType
)

router = APIRouter()


# 环境管理接口
@router.post("/environments", summary="创建环境")
async def create_environment(environment: EnvironmentModel) -> ResponseModel | ResponseSchemaModel:
    """
    创建环境
    """
    success = await EnvironmentManager.create_environment(environment)
    if success:
        return response_base.success(data=environment.model_dump())
    else:
        return response_base.fail()


@router.get("/environments/{environment_id}", summary="获取环境信息")
async def get_environment(environment_id: int = Path(description="环境ID")) -> ResponseModel | ResponseSchemaModel:
    """
    获取环境信息
    """
    environment = await EnvironmentManager.get_environment(environment_id)
    if environment:
        return response_base.success(data=environment.model_dump())
    else:
        return response_base.fail()


@router.put("/environments/{environment_id}", summary="更新环境信息")
async def update_environment(
        environment: EnvironmentModel,
        environment_id: int = Path(description="环境ID")
) -> ResponseModel | ResponseSchemaModel:
    """
    更新环境信息
    """
    # 确保路径参数和请求体ID一致
    if environment.id != environment_id:
        return response_base.fail()
    success = await EnvironmentManager.update_environment(environment)
    if success:
        return response_base.success(data=environment.model_dump())
    else:
        return response_base.fail()


@router.delete("/environments/{environment_id}", summary="删除环境")
async def delete_environment(environment_id: int = Path(description="环境ID")) -> ResponseModel | ResponseSchemaModel:
    """
    删除环境
    """
    success = await EnvironmentManager.delete_environment(environment_id)
    if success:
        return response_base.success(data=f"删除环境ID为:{environment_id} 成功")
    else:
        return response_base.fail()


@router.get("/environments", summary="获取环境列表")
async def list_environments(project_id: int = Query(..., description="项目ID")) -> ResponseModel | ResponseSchemaModel:
    """
    获取项目环境列表
    """
    environments = await EnvironmentManager.list_environments(project_id)
    return response_base.success(data=[env.model_dump() for env in environments])


@router.get("/environments/default", summary="获取默认环境")
async def get_default_environment(project_id: int = Query(..., description="项目ID")) -> JSONResponse:
    """
    获取项目默认环境
    """
    environment = await EnvironmentManager.get_default_environment(project_id)
    if environment:
        return response_base.success(data=environment.model_dump(), msg="获取默认环境成功")
    else:
        return response_base.success(data=None, msg="项目未设置默认环境")


@router.put("/environments/{environment_id}/default", summary="设置默认环境")
async def set_default_environment(
        project_id: int = Query(..., description="项目ID"),
        environment_id: int = Path(..., description="环境ID")
) -> JSONResponse:
    """
    设置项目默认环境
    """
    success = await EnvironmentManager.set_default_environment(project_id, environment_id)
    if success:
        return response_base.success(msg="设置默认环境成功")
    else:
        return response_base.fail(msg="设置默认环境失败")


# 变量管理接口
@router.post("/variables", summary="创建变量")
async def create_variable(variable: VariableModel) -> JSONResponse:
    """
    创建变量
    """
    success = await VariableManager.set_variable(variable)
    if success:
        return response_base.success(data=variable.model_dump(), msg="变量创建成功")
    else:
        return response_base.fail(msg="变量创建失败")


@router.get("/variables", summary="获取变量列表")
async def list_variables(
        scope: VariableScope,
        project_id: Optional[int] = Query(None, description="项目ID"),
        environment_id: Optional[int] = Query(None, description="环境ID"),
        case_id: Optional[int] = Query(None, description="用例ID")
) -> JSONResponse:
    """
    获取变量列表
    """
    variables = await VariableManager.list_variables(
        scope=scope,
        project_id=project_id,
        environment_id=environment_id,
        case_id=case_id
    )
    return response_base.success(
        data=[var.model_dump() for var in variables],
        msg="获取变量列表成功"
    )


@router.get("/variables/{name}", summary="获取变量")
async def get_variable(
        name: str = Path(..., description="变量名"),
        scope: VariableScope = Query(..., description="变量作用域"),
        project_id: Optional[int] = Query(None, description="项目ID"),
        environment_id: Optional[int] = Query(None, description="环境ID"),
        case_id: Optional[int] = Query(None, description="用例ID")
) -> JSONResponse:
    """
    获取变量
    """
    variable = await VariableManager.get_variable(
        name=name,
        scope=scope,
        project_id=project_id,
        environment_id=environment_id,
        case_id=case_id
    )
    if variable:
        return response_base.success(data=variable.model_dump(), msg="获取变量成功")
    else:
        return response_base.fail(msg="变量不存在")


@router.delete("/variables/{name}", summary="删除变量")
async def delete_variable(
        name: str = Path(..., description="变量名"),
        scope: VariableScope = Query(..., description="变量作用域"),
        project_id: Optional[int] = Query(None, description="项目ID"),
        environment_id: Optional[int] = Query(None, description="环境ID"),
        case_id: Optional[int] = Query(None, description="用例ID")
) -> JSONResponse:
    """
    删除变量
    """
    success = await VariableManager.delete_variable(
        name=name,
        scope=scope,
        project_id=project_id,
        environment_id=environment_id,
        case_id=case_id
    )
    if success:
        return response_base.success(msg="删除变量成功")
    else:
        return response_base.fail(msg="删除变量失败")


@router.post("/variables/process-template", summary="处理变量模板")
async def process_template(
        template: str = Body(..., description="模板字符串"),
        project_id: Optional[int] = Body(None, description="项目ID"),
        environment_id: Optional[int] = Body(None, description="环境ID"),
        case_id: Optional[int] = Body(None, description="用例ID"),
        temp_variables: Optional[Dict[str, Any]] = Body(None, description="临时变量")
) -> JSONResponse:
    """
    处理变量模板，替换模板中的变量引用
    """
    result = await VariableManager.process_template(
        template=template,
        project_id=project_id,
        environment_id=environment_id,
        case_id=case_id,
        temp_variables=temp_variables
    )
    return response_base.success(data={"result": result}, msg="处理变量模板成功")
