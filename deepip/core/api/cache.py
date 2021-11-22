import os
import sys
import time
from contextlib import suppress
from pathlib import Path
import json
from typing import Optional


class CacheKeyError(Exception):
    """Error with cache key"""


class CacheAlreadyExistsError(Exception):
    """Information already exists in cache"""


class CacheEmptyError(Exception):
    """There is nothing in cache"""


class CachePathError(Exception):
    """Invalid cache path"""


class Cache:
    """Cache singleton object"""

    DEFAULT_EXPIRE_TIMEOUT: int = 60 * 60 * 24  # 1 day
    DEFAULT_CACHE_PATH: Path = Path('/tmp/.deepip_cache')

    CACHE_EXPIRE_ENV_KEY = 'DEEPIP_CACHE_EXPIRE'
    CACHE_PATH_ENV_KEY = 'DEEPIP_CACHE_PATH'

    _path: Path
    _cache: dict
    _meta: dict

    __item: Optional['Cache'] = None

    def __new__(cls, path: Optional[Path] = None, expire: Optional[int] = None):
        if cls.__item is None:
            cls.__item = super().__new__(cls)
            cls.__item._path = path or os.getenv(Cache.CACHE_PATH_ENV_KEY) or Cache.DEFAULT_CACHE_PATH
            expire_timeout = expire or os.getenv(Cache.CACHE_EXPIRE_ENV_KEY) or Cache.DEFAULT_EXPIRE_TIMEOUT
            cls.__item._meta = {'expire': expire_timeout}
            cls.__item._cache = {}

        return cls.__item

    def __getitem__(self, item):
        return self._cache[item]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise CacheKeyError(f'Cache key should be str, not {type(key)}')

        if key in self._cache:
            raise CacheAlreadyExistsError(f'{key} already exists in cache')

        self._cache[key] = value

    def __contains__(self, item):
        return item in self._cache

    @classmethod
    def init(cls, *args, fake: bool = False, **kwargs):
        """Init cache singleton and load data if not fake"""
        cache = cls(*args, **kwargs)
        if not fake:
            with suppress(CacheEmptyError):
                cache._load()

    @classmethod
    def dump(cls):
        """Dump cache"""
        cache = cls()
        cache._dump()

    @staticmethod
    def convert_to_cache_file(row_path: str) -> Path:
        """Convert string to path to cache file"""
        path = Path(row_path)
        if path.is_file():
            return path
        if path.is_dir():
            return path / '.deepip_cache'
        raise CachePathError('Cache path should be file or directory')

    def load(self) -> bool:
        """Load cache from file if self cache does not exist"""
        return bool(self._cache) or self._load()

    def reload(self) -> bool:
        """Try to reload cache"""
        return self._load()

    def _dump(self):
        """Dump cache to file in json format"""
        with open(self._path, 'w', encoding='utf-8') as cache_file:
            if 'timestamp' not in self._meta:
                self._meta['timestamp'] = time.time()
            json.dump({'meta': self._meta, 'data': self._cache}, cache_file)

    def _load(self) -> bool:
        """Try to load cache from file if it doesn't expired'"""
        if not self._path.exists():
            raise CacheEmptyError('Cache does not exists')

        with open(self._path, 'r', encoding='utf-8') as cache_file:
            cache = json.load(cache_file)

        meta = cache['meta']
        expire_changed = meta['expire'] != self._meta['expire']
        cache_expired = time.time() > meta['timestamp'] + meta['expire']
        if expire_changed or cache_expired:
            self._path.unlink(missing_ok=True)
            raise CacheEmptyError('Timeout expired')

        self._meta = cache['meta']
        self._cache = cache['data']

        sys.stdout.write('Cache used!\n')
        return bool(self._cache)
