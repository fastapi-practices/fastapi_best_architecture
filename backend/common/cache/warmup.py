from backend.common.log import log
from backend.database.db import async_db_session
from backend.plugin.config.enums import ConfigType


async def cache_warmup() -> None:
    """缓存预热"""
    await _warmup_config()
    await _warmup_dict()


async def _warmup_config() -> None:
    """预热参数配置缓存"""
    try:
        from backend.plugin.config.service.config_service import config_service

        async with async_db_session() as db:
            for type in ConfigType.get_member_values():
                await config_service.get_all(db=db, type=type)
    except ImportError:
        pass
    except Exception as e:
        log.warning(f'[Warmup] 参数配置缓存预热失败: {e}')


async def _warmup_dict() -> None:
    """预热数据字典缓存"""
    try:
        from backend.plugin.dict.service.dict_data_service import dict_data_service

        async with async_db_session() as db:
            await dict_data_service.get_all(db=db)
    except ImportError:
        pass
    except Exception as e:
        log.warning(f'[Warmup] 数据字典缓存预热失败: {e}')
