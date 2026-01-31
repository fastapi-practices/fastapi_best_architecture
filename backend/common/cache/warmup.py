from backend.common.log import log
from backend.database.db import async_db_session


async def cache_warmup():
    """执行缓存预热"""
    await _warmup_menu()
    await _warmup_role()
    await _warmup_dict()


async def _warmup_menu():
    """预热菜单缓存"""
    try:
        from backend.app.admin.service.menu_service import menu_service

        async with async_db_session() as db:
            await menu_service.get_tree(db=db, title=None, status=None)
    except Exception as e:
        log.warning(f'[Warmup] 菜单预热失败: {e}')


async def _warmup_role():
    """预热角色缓存"""
    try:
        from backend.app.admin.service.role_service import role_service

        async with async_db_session() as db:
            await role_service.get_all(db=db)
    except Exception as e:
        log.warning(f'[Warmup] 角色预热失败: {e}')


async def _warmup_dict():
    """预热字典缓存"""
    try:
        from backend.plugin.dict.service.dict_data_service import dict_data_service

        async with async_db_session() as db:
            await dict_data_service.get_all(db=db)
    except ImportError:
        pass
    except Exception as e:
        log.warning(f'[Warmup] 字典预热失败: {e}')
