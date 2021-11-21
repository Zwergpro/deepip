import requests

from deepip.core.api.cache import Cache

PYPI_URL = 'https://pypi.org/pypi/'


def get_pypi_package_info(package_name: str) -> dict:
    """Fetch and return package information from pypi"""
    response = requests.get(PYPI_URL + package_name + '/json')
    response.raise_for_status()  # TODO: add bad status handler
    return response.json()


def get_package_meta(package_name: str) -> dict:
    """Return meta information for a package from cache or external service"""
    cache = Cache()
    if package_name in cache:
        return cache[package_name]

    try:
        meta = get_pypi_package_info(package_name)
    except requests.exceptions.HTTPError:
        return {}

    cache[package_name] = meta
    return meta
