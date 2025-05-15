#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def search_string(pattern: str, text: str) -> re.Match[str] | None:
    """
    全字段正则匹配

    :param pattern: 正则表达式模式
    :param text: 待匹配的文本
    :return:
    """
    if not pattern or not text:
        return

    result = re.search(pattern, text)
    return result


def match_string(pattern: str, text: str) -> re.Match[str] | None:
    """
    从字段开头正则匹配

    :param pattern: 正则表达式模式
    :param text: 待匹配的文本
    :return:
    """
    if not pattern or not text:
        return

    result = re.match(pattern, text)
    return result


def is_phone(number: str) -> re.Match[str] | None:
    """
    检查手机号码格式

    :param number: 待检查的手机号码
    :return:
    """
    if not number:
        return

    phone_pattern = r'^1[3-9]\d{9}$'
    return match_string(phone_pattern, number)


def is_git_url(url: str) -> re.Match[str] | None:
    """
    检查 git URL 格式

    :param url: 待检查的 URL
    :return:
    """
    if not url:
        return

    git_pattern = r'^(?!(git\+ssh|ssh)://|git@)(?P<scheme>git|https?|file)://(?P<host>[^/]*)(?P<path>(?:/[^/]*)*/)(?P<repo>[^/]+?)(?:\.git)?$'
    return match_string(git_pattern, url)


if __name__ == '__main__':
    test_urls = [
        # 合法协议地址 (git/http/https/file)
        'git://github.com/user/repo.git',
        'git://gitlab.com/group/project.git',
        'git://example.com:8080/custom/repo.git',  # 带端口
        'http://github.com/user/repo.git',
        'https://gitlab.com/group/project.git',
        'http://example.com:8080/custom/repo.git',
        'file:///path/to/local/repo',  # Unix路径
        'file:///C:/Projects/repo',  # Windows路径
        'https://github.com/user/repo.with.dots',  # 特殊字符
        # 无效协议地址 (应被正则排除)
        'git://host.com',  # 最小格式（无路径）
        'git@github.com:user/repo.git',  # SSH格式
        'ssh://git@github.com/user/repo.git',
        'git+ssh://git@github.com/user/repo.git',
        'github.com/user/repo.git',  # 无协议
        'ftp://example.com/repo.git',  # 非法协议
    ]
    for url in test_urls:
        print(bool(is_git_url(url)))
