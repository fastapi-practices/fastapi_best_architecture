#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import json
import os
import shutil
import zipfile

from typing import Any

from dulwich import porcelain
from fastapi import UploadFile

from backend.common.enums import StatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import redis_client
from backend.plugin.tools import install_requirements_async, uninstall_requirements_async
from backend.utils.re_verify import is_git_url
from backend.utils.timezone import timezone


class PluginService:
    """插件服务类"""

    @staticmethod
    async def get_all() -> list[dict[str, Any]]:
        """获取所有插件"""
        keys = []
        result = []

        async for key in redis_client.scan_iter(f'{settings.PLUGIN_REDIS_PREFIX}:info:*'):
            keys.append(key)

        for info in await redis_client.mget(*keys):
            result.append(json.loads(info))

        return result

    @staticmethod
    async def changed() -> str | None:
        """插件状态是否变更"""
        return await redis_client.get(f'{settings.PLUGIN_REDIS_PREFIX}:changed')

    @staticmethod
    async def install_zip(*, file: UploadFile) -> None:
        """
        通过 zip 压缩包安装插件

        :param file: 插件 zip 压缩包
        :return:
        """
        contents = await file.read()
        file_bytes = io.BytesIO(contents)
        if not zipfile.is_zipfile(file_bytes):
            raise errors.ForbiddenError(msg='插件压缩包格式非法')
        with zipfile.ZipFile(file_bytes) as zf:
            # 校验压缩包
            plugin_namelist = zf.namelist()
            plugin_name = plugin_namelist[0].split('/')[0]
            if not plugin_namelist or plugin_name not in file.filename:
                raise errors.ForbiddenError(msg='插件压缩包内容非法')
            if (
                len(plugin_namelist) <= 3
                or f'{plugin_name}/plugin.toml' not in plugin_namelist
                or f'{plugin_name}/README.md' not in plugin_namelist
            ):
                raise errors.ForbiddenError(msg='插件压缩包内缺少必要文件')

            # 插件是否可安装
            full_plugin_path = os.path.join(PLUGIN_DIR, plugin_name)
            if os.path.exists(full_plugin_path):
                raise errors.ForbiddenError(msg='此插件已安装')
            else:
                os.makedirs(full_plugin_path, exist_ok=True)

            # 解压（安装）
            members = []
            for member in zf.infolist():
                if member.filename.startswith(plugin_name):
                    new_filename = member.filename.replace(plugin_name, '')
                    if new_filename:
                        member.filename = new_filename
                        members.append(member)
            zf.extractall(os.path.join(PLUGIN_DIR, plugin_name), members)

        await install_requirements_async(plugin_name)
        await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    @staticmethod
    async def install_git(*, repo_url: str):
        """
        通过 git 安装插件

        :param repo_url: git 存储库的 URL
        :return:
        """
        match = is_git_url(repo_url)
        if not match:
            raise errors.ForbiddenError(msg='Git 仓库地址格式非法')
        repo_name = match.group('repo')
        plugins = await redis_client.lrange(settings.PLUGIN_REDIS_PREFIX, 0, -1)
        if repo_name in plugins:
            raise errors.ForbiddenError(msg=f'{repo_name} 插件已安装')
        try:
            porcelain.clone(repo_url, os.path.join(PLUGIN_DIR, repo_name), checkout=True)
        except Exception as e:
            log.error(f'插件安装失败: {e}')
            raise errors.ServerError(msg='插件安装失败，请稍后重试') from e
        else:
            await install_requirements_async(repo_name)
        await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    @staticmethod
    async def uninstall(*, plugin: str):
        """
        卸载插件

        :param plugin: 插件名称
        :return:
        """
        plugin_dir = os.path.join(PLUGIN_DIR, plugin)
        if not os.path.exists(plugin_dir):
            raise errors.ForbiddenError(msg='插件不存在')
        await uninstall_requirements_async(plugin)
        bacup_dir = os.path.join(PLUGIN_DIR, f'{plugin}.{timezone.now().strftime("%Y%m%d%H%M%S")}.backup')
        shutil.move(plugin_dir, bacup_dir)
        await redis_client.delete(f'{settings.PLUGIN_REDIS_PREFIX}:info:{plugin}')
        await redis_client.hdel(f'{settings.PLUGIN_REDIS_PREFIX}:status', plugin)
        await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    @staticmethod
    async def update_status(*, plugin: str):
        """
        更新插件状态

        :param plugin: 插件名称
        :return:
        """
        plugin_info = await redis_client.get(f'{settings.PLUGIN_REDIS_PREFIX}:info:{plugin}')
        if not plugin_info:
            raise errors.ForbiddenError(msg='插件不存在')
        plugin_info = json.loads(plugin_info)

        # 更新持久缓存状态
        new_status = (
            str(StatusType.enable.value)
            if plugin_info['plugin']['enable'] == str(StatusType.disable.value)
            else str(StatusType.disable.value)
        )
        plugin_info['plugin']['enable'] = new_status
        await redis_client.set(
            f'{settings.PLUGIN_REDIS_PREFIX}:info:{plugin}', json.dumps(plugin_info, ensure_ascii=False)
        )
        await redis_client.hset(f'{settings.PLUGIN_REDIS_PREFIX}:status', plugin, new_status)

    @staticmethod
    async def build(*, plugin: str) -> io.BytesIO:
        """
        打包插件为 zip 压缩包

        :param plugin: 插件名称
        :return:
        """
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
                    zf.write(file_path, os.path.join(plugin, arcname))

        bio.seek(0)
        return bio


plugin_service: PluginService = PluginService()
