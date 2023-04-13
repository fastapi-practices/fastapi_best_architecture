#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.app.core.path_conf import AvatarPath


def cut_path(path: str = AvatarPath, split_point: str = 'app') -> list:
    """
    切割路径

    :param path:
    :param split_point:
    :return:
    """
    after_path = path.split(split_point)
    return after_path
