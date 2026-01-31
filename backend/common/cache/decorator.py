import functools
import hashlib
import json
from typing import Any, Callable, ParamSpec, TypeVar

from cachebox import make_hash_key

from backend.common.cache.local import local_cache_manager
from backend.common.context import ctx
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.database.redis import redis_client

P = ParamSpec('P')
T = TypeVar('T')

# 哈希缓存键排序参数
_EXCLUDE_PARAMS = frozenset({'db', 'session', 'self', 'cls', 'request', 'response'})


def user_key_builder() -> str:
    """基于当前用户 ID 生成缓存 Key"""
    user_id = ctx.user_id
    if user_id is None:
        raise errors.ServerError(msg='用户缓存键构建失败')
    return str(user_id)


def cached(
    name: str,
    *,
    key: str | None = None,
    key_builder: Callable[..., str] | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    缓存装饰器

    :param name: 缓存名称（通常为缓存 Key 前缀）
    :param key: 从方法参数中获取指定参数名的值作为缓存 Key，与 key_builder 互斥
    :param key_builder: 自定义 Key 生成函数，与 key 互斥
    :return:
    """
    if key is not None and key_builder is not None:
        raise errors.ServerError(msg='缓存 key 和 key_builder 不能同时使用')

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = _build_cache_key(name, key, key_builder, *args, **kwargs)

            # L1: 本地缓存
            if settings.CACHE_LOCAL_ENABLED:
                local_value = local_cache_manager.get(cache_key)
                if local_value is not None:
                    return local_value

            # L2: Redis 缓存
            try:
                redis_value = await redis_client.get(cache_key)
                if redis_value is not None:
                    try:
                        result = json.loads(redis_value)
                        if settings.CACHE_LOCAL_ENABLED:
                            local_cache_manager.set(cache_key, result)
                    except json.JSONDecodeError:
                        return redis_value
                    return result
            except Exception as e:
                log.warning(f'[Cache] GET error: {e}')

            # 缓存未命中
            result = await func(*args, **kwargs)

            if result is not None:
                try:
                    if settings.CACHE_LOCAL_ENABLED:
                        local_cache_manager.set(cache_key, result)
                    serialized = json.dumps(result, ensure_ascii=False)
                    if settings.CACHE_REDIS_TTL:
                        await redis_client.setex(cache_key, settings.CACHE_REDIS_TTL, serialized)
                    else:
                        await redis_client.set(cache_key, serialized)
                except Exception as e:
                    log.warning(f'[Cache] SET error: {e}')

            return result

        return wrapper

    return decorator


def cache_evict(
        name: str,
        *,
        key: str | None = None,
        key_builder: Callable[..., str] | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    缓存失效装饰器

    :param name: 缓存名称（通常为缓存 Key 前缀）
    :param key: 从方法参数中获取指定参数名的值作为缓存 Key，与 key_builder 互斥
    :param key_builder: 自定义 Key 生成函数，与 key 互斥
    :return:
    """
    if key is not None and key_builder is not None:
        raise errors.ServerError(msg='缓存 key 和 key_builder 不能同时使用')

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            result = await func(*args, **kwargs)

            try:
                evict_key = _build_cache_key(name, key, key_builder, *args, **kwargs)
                if evict_key == name:
                    await redis_client.delete(evict_key)
                    local_cache_manager.delete(evict_key)
                else:
                    await redis_client.delete_prefix(evict_key)
                    local_cache_manager.delete_prefix(evict_key)
            except Exception as e:
                log.warning(f'[Cache] EVICT error: {e}')

            return result

        return wrapper

    return decorator


def _build_cache_key(
        name: str,
        key: str | None,
        key_builder: Callable[..., str] | None,
        *args: Any,
        **kwargs: Any,
) -> str:
    """构建缓存 Key"""
    if key_builder:
        return f'{name}:{key_builder(*args, **kwargs)}'

    if key:
        value = kwargs.get(key)
        if value is None:
            raise errors.ServerError(msg=f'缓存键构建失败，参数 "{key}" 不存在或值为空')
        return f'{name}:{value}'

    filtered = {k: v for k, v in kwargs.items() if k not in _EXCLUDE_PARAMS and v is not None}

    if filtered:
        hash_suffix = make_hash_key(*args, **kwargs)
        return f'{name}:{hash_suffix}'

    return name
