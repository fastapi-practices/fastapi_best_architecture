#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import httpx
from XdbSearchIP.xdbSearcher import XdbSearcher
from httpx import HTTPError
from fastapi import Request

from backend.app.core.path_conf import IP2REGION_XDB


async def get_request_ip(request: Request) -> str:
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


async def get_location_online(ipaddr: str, user_agent: str) -> str:
    """
    在线获取 ip 地址属地，无法保证可用性，准确率较高

    :param ipaddr:
    :param user_agent:
    :return:
    """
    async with httpx.AsyncClient(timeout=3) as client:
        ip_api_url = f'http://ip-api.com/json/{ipaddr}?lang=zh-CN'
        whois_url = f'http://whois.pconline.com.cn/ipJson.jsp?ip={ipaddr}&json=true'
        headers = {'User-Agent': user_agent}
        try:
            resp1 = await client.get(ip_api_url, headers=headers)
            city = resp1.json()['city']
        except (HTTPError, KeyError):
            try:
                resp2 = await client.get(whois_url, headers=headers)
                city = resp2.json()['city']
            except (HTTPError, KeyError):
                city = None
    return city or '未知' if city != '' else '未知'


def get_location_offline(ipaddr: str) -> str:
    """
    离线获取 ip 地址属地，无法保证准确率，100%可用

    :param ipaddr:
    :return:
    """
    cb = XdbSearcher.loadContentFromFile(dbfile=IP2REGION_XDB)
    searcher = XdbSearcher(contentBuff=cb)
    data = searcher.search(ipaddr)
    searcher.close()
    location_info = data.split('|')
    country = location_info[0]
    province = location_info[2]
    city = location_info[3]
    return city if city != '0' else province if province != '0' else country if country != '0' else '未知'
