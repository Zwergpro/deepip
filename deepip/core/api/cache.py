import time
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

    def __new__(cls, *args, **kwargs):
        if cls.__item is None:
            cls.__item = super().__new__(cls, *args, **kwargs)
        return cls.__item

    def __init__(self, path: Optional[Path] = None, expire: Optional[int] = None):
        self._meta = {'expire': expire or Cache.DEFAULT_EXPIRE_TIMEOUT}
        self._cache = {}
        self._path = path or Cache.DEFAULT_CACHE_PATH

    def __getitem__(self, item):
        return self._cache[item]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise CacheKeyError(f'Cache key should be str, not {type(key)}')

        if key in self._cache:
            raise CacheAlreadyExists(f'{key} already exists in cache')

        self._cache[key] = value

    def load(self) -> bool:
        """Load cache from file if self cache does not exist"""
        return bool(self._cache) or self._load()

    def reload(self) -> bool:
        """Try to reload cache"""
        return self._load()

    def dump(self):
        """Dump cache if exists to file in json format"""
        if not self._cache:
            raise CacheEmpty('Cache empty')

        with open(self._path, 'w', encoding='utf-8') as cache_file:
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
