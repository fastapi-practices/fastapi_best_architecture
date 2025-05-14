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


def build_filename(file: UploadFile) -> str:
    """
    Build filename

    :param file: FastAPI upload file objects
    :return:
    """
    timestamp = int(timezone.now().timestamp())
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    new_filename = f'{filename.replace(f".{file_ext}", f"_{timestamp}")}.{file_ext}'
    return new_filename


def file_verify(file: UploadFile, file_type: FileType) -> None:
    """
    File Authentication

    :param file: FastAPI upload file objects
    :param file_type: list of file types
    :return:
    """
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    if not file_ext:
        raise errors.ForbiddenError(msg='Unknown file type')

    if file_type == FileType.image:
        if file_ext not in settings.UPLOAD_IMAGE_EXT_INCLUDE:
            raise errors.ForbiddenError(msg='This picture format is not supported')
        if file.size > settings.UPLOAD_IMAGE_SIZE_MAX:
            raise errors.ForbiddenError(msg='Pictures exceed maximum limit. Select again')
    elif file_type == FileType.video:
        if file_ext not in settings.UPLOAD_VIDEO_EXT_INCLUDE:
            raise errors.ForbiddenError(msg='This video format is not supported')
        if file.size > settings.UPLOAD_VIDEO_SIZE_MAX:
            raise errors.ForbiddenError(msg='Video exceeding maximum limit. Select again')


async def upload_file(file: UploadFile) -> str:
    """
    Upload File

    :param file: FastAPI upload file objects
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
        log.error(f'uploading file {filename} failed: {str(e)}')
        raise errors.RequestError(msg='Failed to upload file')
    finally:
        await file.close()
    return filename
