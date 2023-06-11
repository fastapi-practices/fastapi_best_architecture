#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import httpx
from XdbSearchIP.xdbSearcher import XdbSearcher
from asgiref.sync import sync_to_async
from fastapi import Request
from user_agents import parse

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.core.path_conf import IP2REGION_XDB


@sync_to_async
def get_request_ip(request: Request) -> str:
    """获取请求的 ip 地址"""
    real = request.headers.get('X-Real-IP')
    if real:
        ip = real
    else:
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            ip = forwarded.split(',')[0]
        else:
            ip = request.client.host
    return ip


async def get_location_online(ip: str, user_agent: str) -> dict | None:
    """
    在线获取 ip 地址属地，无法保证可用性，准确率较高

    :param ip:
    :param user_agent:
    :return:
    """
    async with httpx.AsyncClient(timeout=3) as client:
        ip_api_url = f'http://ip-api.com/json/{ip}?lang=zh-CN'
        headers = {'User-Agent': user_agent}
        try:
            response = await client.get(ip_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            log.error(f'在线获取 ip 地址属地失败，错误信息：{e}')
            return None


@sync_to_async
def get_location_offline(ip: str) -> list[str] | None:
    """
    离线获取 ip 地址属地，无法保证准确率，100%可用

    :param ip:
    :return:
    """
    try:
        cb = XdbSearcher.loadContentFromFile(dbfile=IP2REGION_XDB)
        searcher = XdbSearcher(contentBuff=cb)
        data = searcher.search(ip)
        searcher.close()
        location_info = data.split('|')
        return location_info
    except Exception as e:
        log.error(f'离线获取 ip 地址属地失败，错误信息：{e}')
        return None


async def parse_ip_info(request: Request) -> tuple[str, str, str, str]:
    country, region, city = None, None, None
    ip = await get_request_ip(request)
    if settings.LOCATION_PARSE == 'online':
        location_info = await get_location_online(ip, request.headers.get('User-Agent'))
        if location_info:
            country = location_info.get('country')
            region = location_info.get('regionName')
            city = location_info.get('city')
    elif settings.LOCATION_PARSE == 'offline':
        location_info = await get_location_offline(ip)
        if location_info:
            country = location_info[0] if location_info[0] != '0' else None
            region = location_info[2] if location_info[2] != '0' else None
            city = location_info[3] if location_info[3] != '0' else None
    return ip, country, region, city


@sync_to_async
def parse_user_agent_info(request: Request) -> tuple[str, str, str, str]:
    user_agent = request.headers.get('User-Agent')
    _user_agent = parse(user_agent)
    device = _user_agent.get_device()
    os = _user_agent.get_os()
    browser = _user_agent.get_browser()
    return user_agent, device, os, browser
