from fastapi import APIRouter

from backend.app.admin.schema.monitor import RedisCommandStat, RedisMonitorInfo, RedisServerInfo
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.redis import redis_client
from backend.utils.format import fmt_seconds

router = APIRouter()


@router.get('', summary='Redis 监控', dependencies=[DependsJwtAuth])
async def get_redis_info() -> ResponseSchemaModel[RedisMonitorInfo]:
    info = await redis_client.info()
    db_size = await redis_client.dbsize()

    server_info = RedisServerInfo(
        redis_version=str(info.get('redis_version', '')),
        redis_mode=str(info.get('redis_mode', '')),
        role=str(info.get('role', '')),
        tcp_port=str(info.get('tcp_port', '')),
        uptime=str(fmt_seconds(int(info.get('uptime_in_seconds', 0)))),
        connected_clients=str(info.get('connected_clients', '')),
        blocked_clients=str(info.get('blocked_clients', '')),
        used_memory_human=str(info.get('used_memory_human', '')),
        used_memory_rss_human=str(info.get('used_memory_rss_human', '')),
        maxmemory_human=str(info.get('maxmemory_human', '0B')),
        mem_fragmentation_ratio=str(info.get('mem_fragmentation_ratio', '0')),
        instantaneous_ops_per_sec=str(info.get('instantaneous_ops_per_sec', '')),
        total_commands_processed=str(info.get('total_commands_processed', '')),
        rejected_connections=str(info.get('rejected_connections', '')),
        keys_num=str(db_size),
    )

    command_stats = await redis_client.info('commandstats')
    stats_list = []
    for key, value in command_stats.items():
        if isinstance(value, dict):
            stats_list.append(RedisCommandStat(name=key.split('_')[-1], value=str(value.get('calls', '0'))))

    data = RedisMonitorInfo(info=server_info, stats=stats_list)
    return response_base.success(data=data)
