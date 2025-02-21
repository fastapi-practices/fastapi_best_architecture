#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import aiofiles

from fastapi import UploadFile

from backend.common.enums import FileType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import UPLOAD_DIR
from backend.utils.timezone import timezone


def build_filename(file: UploadFile):
    """
    构建文件名

    :param file:
    :return:
    """
    timestamp = int(timezone.now().timestamp())
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    new_filename = f'{filename.replace(f".{file_ext}", f"_{timestamp}")}.{file_ext}'
    return new_filename


def file_verify(file: UploadFile, file_type: FileType) -> None:
    """
    文件验证

    :param file:
    :param file_type:
    :return:
    """
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    if not file_ext:
        raise errors.ForbiddenError(msg='未知的文件类型')
    if file_type == FileType.image:
        if file_ext not in settings.UPLOAD_IMAGE_EXT_INCLUDE:
            raise errors.ForbiddenError(msg='此图片格式暂不支持')
        if file.size > settings.UPLOAD_IMAGE_SIZE_MAX:
            raise errors.ForbiddenError(msg='图片超出最大限制，请重新选择')
    elif file_type == FileType.video:
        if file_ext not in settings.UPLOAD_VIDEO_EXT_INCLUDE:
            raise errors.ForbiddenError(msg='此视频格式暂不支持')
        if file.size > settings.UPLOAD_VIDEO_SIZE_MAX:
            raise errors.ForbiddenError(msg='视频超出最大限制，请重新选择')


async def upload_file(file: UploadFile):
    """
    上传文件

    :param file:
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
        raise errors.RequestError(msg='上传文件失败')
    finally:
        await file.close()
    return filename
