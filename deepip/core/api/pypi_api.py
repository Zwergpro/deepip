import requests

PYPI_URL = 'https://pypi.org/pypi/'


def get_pypi_package_info(package_name: str) -> dict:
    """Fetch and return package information from pypi"""
    response = requests.get(PYPI_URL + package_name + '/json')
    response.raise_for_status()  # TODO: add bad status handler
    return response.json()
