#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import httpx

from asgiref.sync import sync_to_async
from fastapi import Request
from ip2loc import XdbSearcher
from user_agents import parse

from backend.common.dataclasses import IpInfo, UserAgentInfo
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import IP2REGION_XDB
from backend.database.redis import redis_client


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
    # 忽略 pytest
    if ip == 'testclient':
        ip = '127.0.0.1'
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
def get_location_offline(ip: str) -> dict | None:
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
        data = data.split('|')
        return {
            'country': data[0] if data[0] != '0' else None,
            'regionName': data[2] if data[2] != '0' else None,
            'city': data[3] if data[3] != '0' else None,
        }
    except Exception as e:
        log.error(f'离线获取 ip 地址属地失败，错误信息：{e}')
        return None


async def parse_ip_info(request: Request) -> IpInfo:
    country, region, city = None, None, None
    ip = get_request_ip(request)
    location = await redis_client.get(f'{settings.IP_LOCATION_REDIS_PREFIX}:{ip}')
    if location:
        country, region, city = location.split('|')
        return IpInfo(ip=ip, country=country, region=region, city=city)
    if settings.IP_LOCATION_PARSE == 'online':
        location_info = await get_location_online(ip, request.headers.get('User-Agent'))
    elif settings.IP_LOCATION_PARSE == 'offline':
        location_info = await get_location_offline(ip)
    else:
        location_info = None
    if location_info:
        country = location_info.get('country')
        region = location_info.get('regionName')
        city = location_info.get('city')
        await redis_client.set(
            f'{settings.IP_LOCATION_REDIS_PREFIX}:{ip}',
            f'{country}|{region}|{city}',
            ex=settings.IP_LOCATION_EXPIRE_SECONDS,
        )
    return IpInfo(ip=ip, country=country, region=region, city=city)


def parse_user_agent_info(request: Request) -> UserAgentInfo:
    user_agent = request.headers.get('User-Agent')
    _user_agent = parse(user_agent)
    os = _user_agent.get_os()
    browser = _user_agent.get_browser()
    device = _user_agent.get_device()
    return UserAgentInfo(user_agent=user_agent, device=device, os=os, browser=browser)
