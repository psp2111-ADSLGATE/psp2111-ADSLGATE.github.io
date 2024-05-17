# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from pathlib import Path
from typing import Callable, TypeVar

from cachetools import TTLCache

from resources.lib.utils.persistentcache import PersistentCache

T = TypeVar('T')


class Cache:

    def __init__(self, cache_name: str, storage_path: Path = None, cache_ttl: timedelta = timedelta()):
        assert cache_name
        self._logger: logging.Logger = logging.getLogger(cache_name)
        if cache_ttl.total_seconds() > 0:
            self._cache = PersistentCache(
                TTLCache,
                filename=storage_path.as_posix(),
                maxsize=1024 * 1024 * 100,
                ttl=cache_ttl.total_seconds())
        else:
            self._cache = None

    def get(self, key, default: T = None) -> T:
        if self._cache is None:
            self._logger.debug("Returning from default (disabled) value for '%s'" % (key))
            return default
        value = self._cache.get(key)
        if value:
            self._logger.debug("Returning from cache value for '%s'" % (key))
            return value
        self._logger.debug("Returning value from default (not found) for '%s'" % (key))
        return default

    def get_or_initialize(self, key, initializer: Callable[[], T]) -> T:
        if self._cache is None:
            value = initializer()
            self._logger.debug("Returning from initializer (disabled) value for '%s'" % (key))
            return value
        value = self._cache.get(key)
        if value:
            self._logger.debug("Returning from cache value for '%s'" % (key))
            return value
        value = initializer()
        self._logger.debug("Returning value from initializer (not found) for '%s'" % (key))
        self.set(key, value)
        return value

    def set(self, key, value) -> None:
        if self._cache is not None:
            self._cache[key] = value

    def delete(self, key) -> None:
        if self._cache is not None:
            self._cache.delete(key)
