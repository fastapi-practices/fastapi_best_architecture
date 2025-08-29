#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
接口历史记录管理
提供接口请求历史记录的存储和查询功能
"""
import datetime
import json
import os
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from backend.common.log import log
from backend.core.path_conf import PLUGIN_DIR
from backend.plugin.api_testing.utils.file_helper import ensure_dir_exists


class RequestHistoryItem(BaseModel):
    """接口请求历史记录项"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="历史记录ID")
    name: str = Field(description="请求名称")
    url: str = Field(description="请求URL")
    method: str = Field(description="请求方法")
    headers: Dict[str, str] = Field(default_factory=dict, description="请求头")
    params: Optional[Dict[str, Any]] = Field(default=None, description="查询参数")
    body: Optional[Any] = Field(default=None, description="请求体")
    status_code: Optional[int] = Field(default=None, description="响应状态码")
    response_headers: Optional[Dict[str, str]] = Field(default=None, description="响应头")
    response_body: Optional[Any] = Field(default=None, description="响应体")
    response_time: Optional[float] = Field(default=None, description="响应时间(ms)")
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, description="请求时间"
    )
    project_id: Optional[str] = Field(default=None, description="项目ID")
    environment_id: Optional[str] = Field(default=None, description="环境ID")
    test_case_id: Optional[str] = Field(default=None, description="测试用例ID")
    test_step_id: Optional[str] = Field(default=None, description="测试步骤ID")
    assertions: Optional[List[Dict[str, Any]]] = Field(default=None, description="断言结果")
    error: Optional[str] = Field(default=None, description="错误信息")
    tags: List[str] = Field(default_factory=list, description="标签")

    def get_duration(self) -> Optional[float]:
        """获取请求持续时间（毫秒）"""
        return self.response_time

    def is_successful(self) -> bool:
        """判断请求是否成功"""
        if self.error:
            return False
        if self.status_code is None:
            return False
        return 200 <= self.status_code < 400


class HistoryManager:
    """历史记录管理器"""
    # 历史记录存储目录
    HISTORY_DIR = os.path.join(PLUGIN_DIR, 'api_testing', 'history')
    # 初始化时确保目录存在
    ensure_dir_exists(HISTORY_DIR)

    # 内存中的历史记录缓存，按项目ID分组
    _history_cache: Dict[str, List[RequestHistoryItem]] = {}
    # 是否已从磁盘加载
    _loaded_from_disk = False

    @classmethod
    async def add_history(cls, history: RequestHistoryItem) -> str:
        """
        添加历史记录
        
        :param history: 历史记录项
        :return: 历史记录ID
        """
        # 确保从磁盘加载了历史记录
        if not cls._loaded_from_disk:
            await cls._load_from_disk()

        # 获取项目ID，如果为空则使用'default'
        project_id = history.project_id or 'default'

        # 将历史记录添加到缓存
        if project_id not in cls._history_cache:
            cls._history_cache[project_id] = []
        cls._history_cache[project_id].append(history)

        # 限制每个项目的历史记录数量，最多保留1000条
        if len(cls._history_cache[project_id]) > 1000:
            cls._history_cache[project_id] = cls._history_cache[project_id][-1000:]

        # 异步保存到磁盘
        await cls._save_to_disk(project_id)

        return history.id

    @classmethod
    async def get_history(cls, history_id: str, project_id: Optional[str] = None) -> Optional[RequestHistoryItem]:
        """
        获取历史记录
        
        :param history_id: 历史记录ID
        :param project_id: 项目ID，如果为空则搜索所有项目
        :return: 历史记录项，如果不存在则返回None
        """
        # 确保从磁盘加载了历史记录
        if not cls._loaded_from_disk:
            await cls._load_from_disk()

        if project_id:
            # 如果指定了项目ID，只在该项目中搜索
            project_histories = cls._history_cache.get(project_id, [])
            for history in project_histories:
                if history.id == history_id:
                    return history
        else:
            # 如果没有指定项目ID，在所有项目中搜索
            for project_histories in cls._history_cache.values():
                for history in project_histories:
                    if history.id == history_id:
                        return history

        return None

    @classmethod
    async def get_history_list(
            cls,
            project_id: Optional[str] = None,
            limit: int = 100,
            skip: int = 0,
            start_time: Optional[datetime.datetime] = None,
            end_time: Optional[datetime.datetime] = None,
            url_contains: Optional[str] = None,
            method: Optional[str] = None,
            tags: Optional[List[str]] = None,
            successful: Optional[bool] = None
    ) -> List[RequestHistoryItem]:
        """
        获取历史记录列表
        
        :param project_id: 项目ID，如果为空则返回所有项目
        :param limit: 返回记录数量限制
        :param skip: 跳过记录数量
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param url_contains: URL包含的字符串
        :param method: HTTP方法
        :param tags: 标签列表
        :param successful: 是否成功
        :return: 历史记录列表
        """
        # 确保从磁盘加载了历史记录
        if not cls._loaded_from_disk:
            await cls._load_from_disk()

        # 收集所有符合条件的历史记录
        all_histories = []
        if project_id:
            # 如果指定了项目ID，只获取该项目的历史记录
            all_histories.extend(cls._history_cache.get(project_id, []))
        else:
            # 如果没有指定项目ID，获取所有项目的历史记录
            for project_histories in cls._history_cache.values():
                all_histories.extend(project_histories)

        # 按时间倒序排序
        all_histories.sort(key=lambda x: x.timestamp, reverse=True)

        # 应用过滤条件
        filtered_histories = []
        for history in all_histories:
            # 时间范围过滤
            if start_time and history.timestamp < start_time:
                continue
            if end_time and history.timestamp > end_time:
                continue

            # URL过滤
            if url_contains and url_contains.lower() not in history.url.lower():
                continue

            # HTTP方法过滤
            if method and history.method.upper() != method.upper():
                continue

            # 标签过滤
            if tags:
                if not all(tag in history.tags for tag in tags):
                    continue

            # 成功状态过滤
            if successful is not None:
                if history.is_successful() != successful:
                    continue

            filtered_histories.append(history)

        # 应用分页
        result = filtered_histories[skip:skip + limit] if limit > 0 else filtered_histories[skip:]

        return result

    @classmethod
    async def delete_history(cls, history_id: str, project_id: Optional[str] = None) -> bool:
        """
        删除历史记录
        
        :param history_id: 历史记录ID
        :param project_id: 项目ID，如果为空则搜索所有项目
        :return: 是否成功删除
        """
        # 确保从磁盘加载了历史记录
        if not cls._loaded_from_disk:
            await cls._load_from_disk()

        # 标记是否找到并删除
        deleted = False

        if project_id:
            # 如果指定了项目ID，只在该项目中搜索
            if project_id in cls._history_cache:
                project_histories = cls._history_cache[project_id]
                for i, history in enumerate(project_histories):
                    if history.id == history_id:
                        project_histories.pop(i)
                        deleted = True
                        break
        else:
            # 如果没有指定项目ID，在所有项目中搜索
            for pid, project_histories in cls._history_cache.items():
                for i, history in enumerate(project_histories):
                    if history.id == history_id:
                        project_histories.pop(i)
                        project_id = pid  # 设置为实际的项目ID
                        deleted = True
                        break
                if deleted:
                    break

        # 如果找到并删除了记录，更新磁盘存储
        if deleted and project_id:
            await cls._save_to_disk(project_id)

        return deleted

    @classmethod
    async def clear_history(cls, project_id: Optional[str] = None) -> int:
        """
        清空历史记录
        
        :param project_id: 项目ID，如果为空则清空所有项目
        :return: 清空的记录数量
        """
        # 确保从磁盘加载了历史记录
        if not cls._loaded_from_disk:
            await cls._load_from_disk()

        count = 0

        if project_id:
            # 如果指定了项目ID，只清空该项目
            if project_id in cls._history_cache:
                count = len(cls._history_cache[project_id])
                cls._history_cache[project_id] = []
                # 更新磁盘存储
                await cls._save_to_disk(project_id)
        else:
            # 如果没有指定项目ID，清空所有项目
            for pid, project_histories in cls._history_cache.items():
                count += len(project_histories)
                cls._history_cache[pid] = []
                # 更新磁盘存储
                await cls._save_to_disk(pid)

        return count

    @classmethod
    async def _load_from_disk(cls) -> None:
        """从磁盘加载历史记录"""
        try:
            # 确保目录存在
            ensure_dir_exists(cls.HISTORY_DIR)

            # 遍历历史记录目录
            for file_name in os.listdir(cls.HISTORY_DIR):
                if file_name.endswith('.json'):
                    try:
                        # 从文件名获取项目ID
                        project_id = file_name[:-5]  # 移除'.json'后缀
                        file_path = os.path.join(cls.HISTORY_DIR, file_name)

                        # 读取文件内容
                        with open(file_path, 'r', encoding='utf-8') as f:
                            history_data = json.load(f)

                        # 转换为历史记录对象
                        histories = []
                        for item_data in history_data:
                            # 转换时间戳字符串为datetime对象
                            if 'timestamp' in item_data and isinstance(item_data['timestamp'], str):
                                try:
                                    item_data['timestamp'] = datetime.datetime.fromisoformat(item_data['timestamp'])
                                except ValueError:
                                    item_data['timestamp'] = datetime.datetime.now()

                            # 创建历史记录对象
                            try:
                                history = RequestHistoryItem(**item_data)
                                histories.append(history)
                            except Exception as e:
                                log.warning(f"无法解析历史记录项: {e}")

                        # 更新缓存
                        cls._history_cache[project_id] = histories
                    except Exception as e:
                        log.error(f"加载历史记录文件 {file_name} 失败: {e}")

            # 标记为已加载
            cls._loaded_from_disk = True
            log.info(f"已加载 {sum(len(histories) for histories in cls._history_cache.values())} 条历史记录")
        except Exception as e:
            log.error(f"加载历史记录失败: {e}")

    @classmethod
    async def _save_to_disk(cls, project_id: str) -> None:
        """
        将项目历史记录保存到磁盘
        
        :param project_id: 项目ID
        """
        try:
            # 确保目录存在
            ensure_dir_exists(cls.HISTORY_DIR)

            # 获取项目历史记录
            histories = cls._history_cache.get(project_id, [])

            # 序列化为JSON
            history_data = []
            for history in histories:
                history_dict = history.model_dump()
                # 将datetime对象转换为ISO格式字符串
                if 'timestamp' in history_dict and isinstance(history_dict['timestamp'], datetime.datetime):
                    history_dict['timestamp'] = history_dict['timestamp'].isoformat()
                history_data.append(history_dict)

            # 保存到文件
            file_path = os.path.join(cls.HISTORY_DIR, f"{project_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)

            log.debug(f"已保存 {len(histories)} 条历史记录到 {file_path}")
        except Exception as e:
            log.error(f"保存历史记录失败: {e}")
