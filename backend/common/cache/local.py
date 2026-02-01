from typing import Any

import cachebox

from backend.core.conf import settings


class LocalCacheManager:
    """本地缓存管理器"""

    def __init__(self) -> None:
        self.hot_cache: cachebox.TTLCache = cachebox.TTLCache(100000, ttl=settings.CACHE_LOCAL_TTL)

    def get(self, key: str) -> Any:
        """获取缓存"""
        try:
            return self.hot_cache[key]
        except KeyError:
            return None

    def set(self, key: str, value: Any) -> None:
        """设置缓存"""
        self.hot_cache[key] = value

    def delete(self, key: str) -> bool:
        """删除缓存"""
        if self.get(key) is not None:
            del self.hot_cache[key]
            return True
        return False

    def clear(self) -> None:
        """清空缓存"""
        self.hot_cache.clear()

    def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None) -> None:
        """
        删除指定前缀的缓存

        :param prefix: 要删除的键前缀
        :param exclude: 要排除的键或键列表
        :return:
        """
        exclude_set = set(exclude) if isinstance(exclude, list) else {exclude} if isinstance(exclude, str) else set()
        keys_to_delete = [k for k in self.hot_cache.keys() if k.startswith(prefix) and k not in exclude_set]
        for key in keys_to_delete:
            if self.get(key) is not None:
                del self.hot_cache[key]


local_cache_manager = LocalCacheManager()
