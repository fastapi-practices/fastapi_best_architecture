#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import httpx
from httpx import HTTPError


async def get_location(ipaddr: str, user_agent: str) -> str:
    """获取ip地址归属地(临时)"""
    async with httpx.AsyncClient() as client:
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
