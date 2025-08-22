#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件操作辅助工具
提供文件操作相关的辅助函数
"""
import os
from typing import List


def ensure_dir_exists(directory: str) -> None:
    """
    确保目录存在，如果不存在则创建
    
    :param directory: 目录路径
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            # 记录错误但不抛出异常
            print(f"创建目录失败: {directory}, 错误: {e}")


def list_files(directory: str, extension: str = None) -> List[str]:
    """
    列出目录下的所有文件
    
    :param directory: 目录路径
    :param extension: 文件扩展名过滤，例如 '.json'
    :return: 文件路径列表
    """
    ensure_dir_exists(directory)
    files = []
    
    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                if extension is None or file_name.endswith(extension):
                    files.append(file_path)
    except Exception as e:
        print(f"列出目录文件失败: {directory}, 错误: {e}")
    
    return files