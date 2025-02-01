from tmdbhelper.lib.addon.logger import kodi_traceback
from tmdbhelper.lib.files.scache import SimpleCache, SimpleCacheMem
from tmdbhelper.lib.addon.plugin import get_setting
import jurialmunkey.bcache

use_simple_cache = jurialmunkey.bcache.use_simple_cache


def factory_simple_cache():
    if get_setting('mem_cache_level', 'int') == 2:  # Always = 2
        return SimpleCacheMem
    return SimpleCache


class BasicCache(jurialmunkey.bcache.BasicCache):
    _simplecache = factory_simple_cache()

    @staticmethod
    def kodi_traceback(exc, log_msg):
        kodi_traceback(exc, log_msg)


class BasicCacheMem(BasicCache):
    _simplecache = SimpleCacheMem
    _queue_limit = 250


class BasicCacheServiceMem(BasicCacheMem):
    _queue_limit = 20



