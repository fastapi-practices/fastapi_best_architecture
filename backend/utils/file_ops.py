#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os
import re
import zipfile

import aiofiles

from dulwich import porcelain
from fastapi import UploadFile
from sqlparse import split

from backend.common.enums import FileType
from backend.common.exception import errors
from backend.common.i18n import t
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
        raise errors.RequestError(msg=t('error.file_type_unknown'))

    if file_ext == FileType.image:
        if file_ext not in settings.UPLOAD_IMAGE_EXT_INCLUDE:
            raise errors.RequestError(msg=t('error.image.format_not_supported'))
        if file.size > settings.UPLOAD_IMAGE_SIZE_MAX:
            raise errors.RequestError(msg=t('error.image.size_exceeded'))
    elif file_ext == FileType.video:
        if file_ext not in settings.UPLOAD_VIDEO_EXT_INCLUDE:
            raise errors.RequestError(msg=t('error.video.format_not_supported'))
        if file.size > settings.UPLOAD_VIDEO_SIZE_MAX:
            raise errors.RequestError(msg=t('error.video.size_exceeded'))


async def upload_file(file: UploadFile) -> str:
    """
    上传文件

    :param file: FastAPI 上传文件对象
    :return:
    """
    filename = build_filename(file)
    try:
        async with aiofiles.open(os.path.join(UPLOAD_DIR, filename), mode='wb') as fb:
            while True:
                content = await file.read(settings.UPLOAD_READ_SIZE)
                if not content:
                    break
                await fb.write(content)
    except Exception as e:
        log.error(f'上传文件 {filename} 失败：{str(e)}')
        raise errors.RequestError(msg=t('error.upload_file_failed'))
    await file.close()
    return filename


async def install_zip_plugin(file: UploadFile | str) -> str:
    """
    安装 ZIP 插件

    :param file: FastAPI 上传文件对象或文件完整路径
    :return:
    """
    if isinstance(file, str):
        async with aiofiles.open(file, mode='rb') as fb:
            contents = await fb.read()
    else:
        contents = await file.read()
    file_bytes = io.BytesIO(contents)
    if not zipfile.is_zipfile(file_bytes):
        raise errors.RequestError(msg=t('error.plugin.zip_invalid'))
    with zipfile.ZipFile(file_bytes) as zf:
        # 校验压缩包
        plugin_namelist = zf.namelist()
        plugin_dir_name = plugin_namelist[0].split('/')[0]
        if not plugin_namelist:
            raise errors.RequestError(msg=t('error.plugin.zip_content_invalid'))
        if (
            len(plugin_namelist) <= 3
            or f'{plugin_dir_name}/plugin.toml' not in plugin_namelist
            or f'{plugin_dir_name}/README.md' not in plugin_namelist
        ):
            raise errors.RequestError(msg=t('error.plugin.zip_missing_files'))

        # 插件是否可安装
        plugin_name = re.match(
            r'^([a-zA-Z0-9_]+)',
            file.split(os.sep)[-1].split('.')[0].strip()
            if isinstance(file, str)
            else file.filename.split('.')[0].strip(),
        ).group()
        full_plugin_path = os.path.join(PLUGIN_DIR, plugin_name)
        if os.path.exists(full_plugin_path):
            raise errors.ConflictError(msg=t('error.plugin.already_installed'))
        else:
            os.makedirs(full_plugin_path, exist_ok=True)

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
        raise errors.RequestError(msg=t('error.plugin.git_url_invalid'))
    repo_name = match.group('repo')
    if os.path.exists(os.path.join(PLUGIN_DIR, repo_name)):
        raise errors.ConflictError(msg=t('error.plugin.already_installed'))
    try:
        porcelain.clone(repo_url, os.path.join(PLUGIN_DIR, repo_name), checkout=True)
    except Exception as e:
        log.error(f'插件安装失败: {e}')
        raise errors.ServerError(msg=t('error.plugin.install_failed')) from e

    await install_requirements_async(repo_name)
    await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    return repo_name


async def parse_sql_script(filepath: str) -> list[str]:
    """
    解析 SQL 脚本

    :param filepath: 脚本文件路径
    :return:
    """
    if not os.path.exists(filepath):
        raise errors.NotFoundError(msg=t('error.sql.file_not_found'))

    async with aiofiles.open(filepath, mode='r', encoding='utf-8') as f:
        contents = await f.read(1024)
        while additional_contents := await f.read(1024):
            contents += additional_contents

    statements = split(contents)
    for statement in statements:
        if not any(statement.lower().startswith(_) for _ in ['select', 'insert']):
            raise errors.RequestError(msg=t('error.sql.syntax_not_allowed'))

    return statements
