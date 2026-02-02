import io
import os
import re
import zipfile

import anyio

from anyio import open_file
from dulwich import porcelain
from fastapi import UploadFile
from starlette.concurrency import run_in_threadpool

from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import ENV_FILE_PATH, PLUGIN_DIR
from backend.database.redis import redis_client
from backend.plugin.requirements import install_requirements_async
from backend.utils.locks import acquire_distributed_reload_lock
from backend.utils.pattern_validate import is_git_url


async def _append_env_example(plugin_path: anyio.Path) -> None:
    """
    追加主 .env 文件

    :param plugin_path: 插件目录路径
    :return:
    """
    env_example_path = plugin_path / '.env.example'
    if not await env_example_path.exists():
        return

    async with await open_file(env_example_path, mode='r', encoding='utf-8') as f:
        env_example_content = await f.read()

    if not env_example_content.strip():
        return

    env_path = anyio.Path(ENV_FILE_PATH)
    existing_content = ''
    if await env_path.exists():
        async with await open_file(env_path, mode='r', encoding='utf-8') as f:
            existing_content = await f.read()

    separator = '\n' if existing_content and not existing_content.endswith('\n') else ''
    new_content = f'{existing_content}{separator}{env_example_content}'

    async with await open_file(env_path, mode='w', encoding='utf-8') as f:
        await f.write(new_content)


async def install_zip_plugin(file: UploadFile | str) -> str:
    """
    安装 ZIP 插件

    :param file: FastAPI 上传文件对象或文件完整路径
    :return:
    """
    if isinstance(file, str):
        async with await open_file(file, mode='rb') as fb:
            contents = await fb.read()
    else:
        contents = await file.read()
    file_bytes = io.BytesIO(contents)
    if not zipfile.is_zipfile(file_bytes):
        raise errors.RequestError(msg='插件压缩包格式非法')

    async with acquire_distributed_reload_lock():
        with zipfile.ZipFile(file_bytes) as zf:
            # 校验压缩包
            plugin_namelist = zf.namelist()
            plugin_dir_name = plugin_namelist[0].split('/')[0]
            if not plugin_namelist:
                raise errors.RequestError(msg='插件压缩包内容非法')
            if (
                len(plugin_namelist) <= 3
                or f'{plugin_dir_name}/plugin.toml' not in plugin_namelist
                or f'{plugin_dir_name}/README.md' not in plugin_namelist
            ):
                raise errors.RequestError(msg='插件压缩包内缺少必要文件')

            # 插件是否可安装
            plugin_name = re.match(
                r'^([a-zA-Z0-9_]+)',
                file.split(os.sep)[-1].split('.')[0].strip()
                if isinstance(file, str)
                else file.filename.split('.')[0].strip(),
            ).group()
            full_plugin_path = anyio.Path(PLUGIN_DIR / plugin_name)
            if await full_plugin_path.exists():
                raise errors.ConflictError(msg='此插件已安装')
            await full_plugin_path.mkdir(parents=True, exist_ok=True)

            # 解压（安装）
            members = []
            for member in zf.infolist():
                if member.filename.startswith(plugin_dir_name):
                    new_filename = member.filename.replace(plugin_dir_name, '')
                    if new_filename:
                        member.filename = new_filename
                        members.append(member)
            await run_in_threadpool(zf.extractall, full_plugin_path, members)

        await _append_env_example(full_plugin_path)
        await install_requirements_async(plugin_dir_name)
        await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'true')

    return plugin_name


async def install_git_plugin(repo_url: str) -> str:
    """
    安装 Git 插件

    :param repo_url:
    :return:
    """
    match = is_git_url(repo_url)
    if not match:
        raise errors.RequestError(msg='Git 仓库地址格式非法，仅支持 HTTP/HTTPS 协议')
    repo_name = match.group('repo')
    path = anyio.Path(PLUGIN_DIR / repo_name)
    if await path.exists():
        raise errors.ConflictError(msg=f'{repo_name} 插件已安装')

    async with acquire_distributed_reload_lock():
        try:
            await run_in_threadpool(porcelain.clone, repo_url, PLUGIN_DIR / repo_name, checkout=True)
        except Exception as e:
            log.error(f'插件安装失败: {e}')
            raise errors.ServerError(msg='插件安装失败，请稍后重试') from e

        await _append_env_example(path)
        await install_requirements_async(repo_name)
        await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'true')

    return repo_name
