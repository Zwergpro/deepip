import time
from contextlib import suppress
from pathlib import Path
import json
from typing import Optional


class CacheKeyError(Exception):
    """Error with cache key"""


class CacheAlreadyExists(Exception):
    """Information already exists in cache"""


class CacheEmpty(Exception):
    """There is nothing in cache"""


class Cache:
    """Cache singleton object"""

    DEFAULT_EXPIRE_TIMEOUT: int = 60 * 60 * 24  # 1 day
    DEFAULT_CACHE_PATH: Path = Path('/tmp/.deepip_cache')

    _path: Path
    _cache: dict
    _meta: dict

    __item: Optional['Cache'] = None

    def __new__(cls, path: Optional[Path] = None, expire: Optional[int] = None):
        if cls.__item is None:
            cls.__item = super().__new__(cls)
            cls.__item._meta = {'expire': expire or Cache.DEFAULT_EXPIRE_TIMEOUT}
            cls.__item._path = path or Cache.DEFAULT_CACHE_PATH
            cls.__item._cache = {}

        return cls.__item

    def __getitem__(self, item):
        return self._cache[item]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise CacheKeyError(f'Cache key should be str, not {type(key)}')

        if key in self._cache:
            raise CacheAlreadyExists(f'{key} already exists in cache')

        self._cache[key] = value

    def __contains__(self, item):
        return item in self._cache

    @classmethod
    def init(cls, fake: bool = False):
        """Init cache singleton and load data if not fake"""
        cache = cls()
        if not fake:
            with suppress(CacheEmpty):
                cache._load()

    @classmethod
    def dump(cls):
        """Dump cache"""
        cache = cls()
        cache._dump()

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
            raise CacheEmpty('Cache does not exists')

        with open(self._path, 'r', encoding='utf-8') as cache_file:
            cache = json.load(cache_file)

        meta = cache['meta']
        if time.time() > meta['timestamp'] + meta['expire']:
            self._path.unlink(missing_ok=True)
            raise CacheEmpty('Timeout expired')

        self._meta = cache['meta']
        self._cache = cache['data']

        return bool(self._cache)
