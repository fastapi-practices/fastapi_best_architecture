import io
import os
import re
import zipfile

import anyio

from anyio import open_file
from dulwich import porcelain
from fastapi import UploadFile
from sqlparse import split

from backend.common.enums import FileType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR, UPLOAD_DIR
from backend.database.redis import redis_client
from backend.plugin.tools import install_requirements_async
from backend.utils.re_verify import is_git_url
from backend.utils.timezone import timezone


def build_filename(file: UploadFile) -> str:
    """
    构建文件名

    :param file: FastAPI 上传文件对象
    :return:
    """
    timestamp = int(timezone.now().timestamp())
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    new_filename = f'{filename.replace(f".{file_ext}", f"_{timestamp}")}.{file_ext}'
    return new_filename


def upload_file_verify(file: UploadFile) -> None:
    """
    文件验证

    :param file: FastAPI 上传文件对象
    :return:
    """
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    if not file_ext:
        raise errors.RequestError(msg='未知的文件类型')

    if file_ext == FileType.image:
        if file_ext not in settings.UPLOAD_IMAGE_EXT_INCLUDE:
            raise errors.RequestError(msg='此图片格式暂不支持')
        if file.size > settings.UPLOAD_IMAGE_SIZE_MAX:
            raise errors.RequestError(msg='图片超出最大限制，请重新选择')
    elif file_ext == FileType.video:
        if file_ext not in settings.UPLOAD_VIDEO_EXT_INCLUDE:
            raise errors.RequestError(msg='此视频格式暂不支持')
        if file.size > settings.UPLOAD_VIDEO_SIZE_MAX:
            raise errors.RequestError(msg='视频超出最大限制，请重新选择')


async def upload_file(file: UploadFile) -> str:
    """
    上传文件

    :param file: FastAPI 上传文件对象
    :return:
    """
    filename = build_filename(file)
    try:
        async with await open_file(UPLOAD_DIR / filename, mode='wb') as fb:
            while True:
                content = await file.read(settings.UPLOAD_READ_SIZE)
                if not content:
                    break
                await fb.write(content)
    except Exception as e:
        log.error(f'上传文件 {filename} 失败：{e!s}')
        raise errors.RequestError(msg='上传文件失败')
    await file.close()
    return filename


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
        zf.extractall(full_plugin_path, members)

    await install_requirements_async(plugin_dir_name)
    await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    return plugin_name


async def install_git_plugin(repo_url: str) -> str:
    """
    安装 Git 插件

    :param repo_url:
    :return:
    """
    match = is_git_url(repo_url)
    if not match:
        raise errors.RequestError(msg='Git 仓库地址格式非法')
    repo_name = match.group('repo')
    path = anyio.Path(PLUGIN_DIR / repo_name)
    if await path.exists():
        raise errors.ConflictError(msg=f'{repo_name} 插件已安装')
    try:
        porcelain.clone(repo_url, PLUGIN_DIR / repo_name, checkout=True)
    except Exception as e:
        log.error(f'插件安装失败: {e}')
        raise errors.ServerError(msg='插件安装失败，请稍后重试') from e

    await install_requirements_async(repo_name)
    await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    return repo_name


async def parse_sql_script(filepath: str) -> list[str]:
    """
    解析 SQL 脚本

    :param filepath: 脚本文件路径
    :return:
    """
    path = anyio.Path(filepath)
    if not await path.exists():
        raise errors.NotFoundError(msg='SQL 脚本文件不存在')

    async with await open_file(filepath, encoding='utf-8') as f:
        contents = await f.read(1024)
        while additional_contents := await f.read(1024):
            contents += additional_contents

    statements = split(contents)
    for statement in statements:
        if not any(statement.lower().startswith(_) for _ in ['select', 'insert']):
            raise errors.RequestError(msg='SQL 脚本文件中存在非法操作，仅允许 SELECT 和 INSERT')

    return statements
