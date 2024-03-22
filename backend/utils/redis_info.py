#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.database.db_redis import redis_client
from backend.utils.server_info import server_info


class RedisInfo:
    @staticmethod
    async def get_info():
        info = await redis_client.info()
        fmt_info = {}
        for key, value in info.items():
            if isinstance(value, dict):
                value = ','.join({f'{k}={v}' for k, v in value.items()})
            else:
                value = str(value)
            fmt_info[key] = value
        db_size = await redis_client.dbsize()
        fmt_info.update({'keys_num': db_size})
        fmt_uptime = server_info.fmt_seconds(fmt_info.get('uptime_in_seconds', 0))
        fmt_info.update({'uptime_in_seconds': fmt_uptime})
        return fmt_info

    @staticmethod
    async def get_stats():
        stats_list = []
        command_stats = await redis_client.info('commandstats')
        for k, v in command_stats.items():
            stats_list.append({'name': k.split('_')[-1], 'value': str(v.get('calls', ''))})
        return stats_list


redis_info = RedisInfo()
