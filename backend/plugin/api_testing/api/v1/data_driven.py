#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据驱动测试API
"""
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Body, Path, Query, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pandas as pd
import json
import os
import tempfile

from backend.common.response.response_schema import response_base
from backend.plugin.api_testing.utils.data_driven import (
    DataDriverManager, DataDrivenConfig, DataSourceConfig,
    DataSourceType, DatabaseType, TestCaseParameter, TestIteration
)

router = APIRouter()


@router.post("/config", summary="创建或更新数据驱动测试配置")
async def create_data_driven_config(config: DataDrivenConfig) -> JSONResponse:
    """
    创建或更新数据驱动测试配置
    """
    try:
        if config.data_source and config.data_source.type != DataSourceType.PARAMETER:
            # 检查文件是否存在
            if config.data_source.file_path:
                file_path = config.data_source.file_path
                if not os.path.isabs(file_path):
                    from backend.core.path_conf import PLUGIN_DIR
                    file_path = os.path.join(PLUGIN_DIR, 'api_testing', file_path)
                    
                if not os.path.exists(file_path):
                    return response_base.fail(msg=f"文件不存在: {file_path}")
        
        # 准备测试迭代数据
        iterations = await DataDriverManager.prepare_iterations(config)
        config.iterations = iterations
        
        return response_base.success(data=config.model_dump(), msg="数据驱动测试配置创建成功")
    except Exception as e:
        return response_base.fail(msg=f"数据驱动测试配置创建失败: {str(e)}")


@router.post("/upload/csv", summary="上传CSV数据文件")
async def upload_csv_file(
    file: UploadFile = File(...),
    directory: str = Form("data")
) -> JSONResponse:
    """
    上传CSV数据文件
    
    保存到插件目录的指定子目录中
    """
    try:
        # 确保目录存在
        from backend.core.path_conf import PLUGIN_DIR
        save_dir = os.path.join(PLUGIN_DIR, 'api_testing', directory)
        os.makedirs(save_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(save_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # 读取CSV预览数据
        df = pd.read_csv(file_path, nrows=5)
        preview = df.to_dict(orient='records')
        
        return response_base.success(
            data={
                "file_path": os.path.join(directory, file.filename),
                "columns": list(df.columns),
                "preview": preview,
                "rows": len(pd.read_csv(file_path))
            },
            msg="CSV文件上传成功"
        )
    except Exception as e:
        return response_base.fail(msg=f"CSV文件上传失败: {str(e)}")


@router.post("/upload/excel", summary="上传Excel数据文件")
async def upload_excel_file(
    file: UploadFile = File(...),
    directory: str = Form("data")
) -> JSONResponse:
    """
    上传Excel数据文件
    
    保存到插件目录的指定子目录中
    """
    try:
        # 确保目录存在
        from backend.core.path_conf import PLUGIN_DIR
        save_dir = os.path.join(PLUGIN_DIR, 'api_testing', directory)
        os.makedirs(save_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(save_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # 读取Excel预览数据
        xls = pd.ExcelFile(file_path)
        sheet_info = {}
        
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=5)
            sheet_info[sheet_name] = {
                "columns": list(df.columns),
                "preview": df.to_dict(orient='records'),
                "rows": len(pd.read_excel(file_path, sheet_name=sheet_name))
            }
            
        return response_base.success(
            data={
                "file_path": os.path.join(directory, file.filename),
                "sheets": sheet_info
            },
            msg="Excel文件上传成功"
        )
    except Exception as e:
        return response_base.fail(msg=f"Excel文件上传失败: {str(e)}")


@router.post("/upload/json", summary="上传JSON数据文件")
async def upload_json_file(
    file: UploadFile = File(...),
    directory: str = Form("data")
) -> JSONResponse:
    """
    上传JSON数据文件
    
    保存到插件目录的指定子目录中
    """
    try:
        # 确保目录存在
        from backend.core.path_conf import PLUGIN_DIR
        save_dir = os.path.join(PLUGIN_DIR, 'api_testing', directory)
        os.makedirs(save_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(save_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # 读取JSON预览数据
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            
        # 如果是数组，取前5个元素作为预览
        preview = json_data
        items_count = 1
        
        if isinstance(json_data, list):
            items_count = len(json_data)
            preview = json_data[:5] if len(json_data) > 5 else json_data
            
        # 如果不是数组，则包装成数组方便处理
        elif isinstance(json_data, dict):
            preview = [json_data]
            
        return response_base.success(
            data={
                "file_path": os.path.join(directory, file.filename),
                "preview": preview,
                "items_count": items_count
            },
            msg="JSON文件上传成功"
        )
    except Exception as e:
        return response_base.fail(msg=f"JSON文件上传失败: {str(e)}")


@router.post("/validate-data-source", summary="验证数据源配置")
async def validate_data_source(config: DataSourceConfig) -> JSONResponse:
    """
    验证数据源配置
    
    加载部分数据验证数据源配置是否正确
    """
    try:
        # 加载前5条数据
        data = await DataDriverManager.load_data_source(config)
        preview = data[:5] if len(data) > 5 else data
        
        return response_base.success(
            data={
                "valid": True,
                "rows_count": len(data),
                "preview": preview,
                "columns": list(preview[0].keys()) if preview else []
            },
            msg="数据源配置验证成功"
        )
    except Exception as e:
        return response_base.fail(
            data={"valid": False},
            msg=f"数据源配置验证失败: {str(e)}"
        )


@router.post("/prepare-iterations", summary="准备测试迭代数据")
async def prepare_iterations(config: DataDrivenConfig) -> JSONResponse:
    """
    准备测试迭代数据
    
    根据数据驱动配置生成测试迭代数据
    """
    try:
        iterations = await DataDriverManager.prepare_iterations(config)
        
        return response_base.success(
            data={
                "iterations_count": len(iterations),
                "iterations": [iter.model_dump() for iter in iterations]
            },
            msg="测试迭代数据准备成功"
        )
    except Exception as e:
        return response_base.fail(msg=f"测试迭代数据准备失败: {str(e)}")


@router.get("/data-directories", summary="获取数据目录列表")
async def get_data_directories() -> JSONResponse:
    """
    获取数据目录列表
    
    获取插件目录下可用于存放数据文件的目录列表
    """
    try:
        # 插件根目录
        from backend.core.path_conf import PLUGIN_DIR
        plugin_dir = os.path.join(PLUGIN_DIR, 'api_testing')
        
        # 默认数据目录
        data_dir = os.path.join(plugin_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # 获取所有目录
        directories = []
        for root, dirs, files in os.walk(plugin_dir):
            if os.path.abspath(root) != os.path.abspath(plugin_dir):
                rel_path = os.path.relpath(root, plugin_dir)
                directories.append(rel_path)
                
        return response_base.success(data=directories, msg="获取数据目录列表成功")
    except Exception as e:
        return response_base.fail(msg=f"获取数据目录列表失败: {str(e)}")


@router.get("/data-files/{directory}", summary="获取数据目录下的文件")
async def get_data_files(directory: str = Path(..., description="目录路径")) -> JSONResponse:
    """
    获取数据目录下的文件
    
    获取指定数据目录下的所有文件
    """
    try:
        # 插件目录下的指定目录
        from backend.core.path_conf import PLUGIN_DIR
        dir_path = os.path.join(PLUGIN_DIR, 'api_testing', directory)
        
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            return response_base.fail(msg=f"目录不存在: {directory}")
            
        # 获取目录下的所有文件
        files = []
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                files.append({
                    "name": filename,
                    "path": os.path.join(directory, filename),
                    "size": os.path.getsize(file_path),
                    "type": os.path.splitext(filename)[1].lstrip('.')
                })
                
        return response_base.success(data=files, msg="获取数据文件列表成功")
    except Exception as e:
        return response_base.fail(msg=f"获取数据文件列表失败: {str(e)}")