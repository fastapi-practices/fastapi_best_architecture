from contextlib import asynccontextmanager

import anyio

from backend.core.path_conf import RELOAD_LOCK_FILE


@asynccontextmanager
async def reload_lock():
    """批量文件操作时暂停热重载"""
    lock_path = anyio.Path(RELOAD_LOCK_FILE)
    await lock_path.touch()
    try:
        yield
    finally:
        await lock_path.unlink(missing_ok=True)
