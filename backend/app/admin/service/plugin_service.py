from __future__ import annotations

import io
import os
import json
import shutil
import zipfile

from typing import TYPE_CHECKING, Any

import anyio

from backend.core.conf import settings
from backend.common.enums import PluginType, StatusType
from backend.plugin.tools import uninstall_requirements_async
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import redis_client
from backend.utils.file_ops import install_git_plugin, install_zip_plugin
from backend.utils.timezone import timezone
from backend.common.exception import errors

if TYPE_CHECKING:
    from fastapi import UploadFile


class PluginService:
    """插件服务类"""

    @staticmethod
    async def get_all() -> list[dict[str, Any]]:
        """获取所有插件"""

        keys = [key async for key in redis_client.scan_iter(f'{settings.PLUGIN_REDIS_PREFIX}:*')]

        result = [json.loads(info) for info in await redis_client.mget(*keys)]

        return result

    @staticmethod
    async def changed() -> str | None:
        """检查插件是否发生变更"""
        return await redis_client.get(f'{settings.PLUGIN_REDIS_PREFIX}:changed')

    @staticmethod
    async def install(*, type: PluginType, file: UploadFile | None = None, repo_url: str | None = None) -> str:
        """
        安装插件

        :param type: 插件类型
        :param file: 插件 zip 压缩包
        :param repo_url: git 仓库地址
        :return:
        """
        if type == PluginType.zip:
            if not file:
                raise errors.RequestError(msg='ZIP 压缩包不能为空')
            return await install_zip_plugin(file)
        if not repo_url:
            raise errors.RequestError(msg='Git 仓库地址不能为空')
        return await install_git_plugin(repo_url)

    @staticmethod
    async def uninstall(*, plugin: str) -> None:
        """
        卸载插件

        :param plugin: 插件名称
        :return:
        """
        plugin_dir = anyio.Path(PLUGIN_DIR / plugin)
        if not await plugin_dir.exists():
            raise errors.NotFoundError(msg='插件不存在')
        await uninstall_requirements_async(plugin)
        bacup_dir = PLUGIN_DIR / f'{plugin}.{timezone.now().strftime("%Y%m%d%H%M%S")}.backup'
        shutil.move(plugin_dir, bacup_dir)
        await redis_client.delete(f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}')
        await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    @staticmethod
    async def update_status(*, plugin: str) -> None:
        """
        更新插件状态

        :param plugin: 插件名称
        :return:
        """
        plugin_info = await redis_client.get(f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}')
        if not plugin_info:
            raise errors.NotFoundError(msg='插件不存在')
        plugin_info = json.loads(plugin_info)

        # 更新持久缓存状态
        new_status = (
            str(StatusType.enable.value)
            if plugin_info['plugin']['enable'] == str(StatusType.disable.value)
            else str(StatusType.disable.value)
        )
        plugin_info['plugin']['enable'] = new_status
        await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}', json.dumps(plugin_info, ensure_ascii=False))

    @staticmethod
    async def build(*, plugin: str) -> io.BytesIO:
        """
        打包插件为 zip 压缩包

        :param plugin: 插件名称
        :return:
        """
        plugin_dir = anyio.Path(PLUGIN_DIR / plugin)
        if not await plugin_dir.exists():
            raise errors.NotFoundError(msg='插件不存在')

        bio = io.BytesIO()
        with zipfile.ZipFile(bio, 'w') as zf:
            for root, dirs, files in os.walk(plugin_dir):
                dirs[:] = [d for d in dirs if d != '__pycache__']
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=plugin_dir)  # noqa: ASYNC240
                    zf.write(file_path, os.path.join(plugin, arcname))

        bio.seek(0)
        return bio


plugin_service: PluginService = PluginService()
