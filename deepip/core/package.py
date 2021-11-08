from typing import Dict, List, Tuple

from deepip.core.requirement import RequirementInfo


class Package:
    """
    Class to wrap pkg_resources and represent package instance.

    The pkg_resources module distributed with setuptools provides runtime facilities for finding, introspecting,
    activating and using installed Python distributions.

    https://setuptools.pypa.io/en/latest/pkg_resources.html
    """
    __all_packages: Dict[str, 'Package'] = {}  # global repository for all installed packages

    _package = None
    ref_counter: int

    def __init__(self, package):
        self._package = package

        if package.key in self.__all_packages:
            raise Exception(f'Package {package.key} already exists')

        self.__all_packages[package.key] = self
        self.ref_counter = 0

    def get_requirements(self) -> List[Tuple['Package', RequirementInfo]]:
        """Return all package requirements"""
        requirements = []
        for requirement in self._package.requires():
            requirements.append((self.__all_packages[requirement.key], RequirementInfo(requirement)))
        return requirements

    @property
    def name(self):
        """Return package name"""
        return self._package.key

    def incr_ref_counter(self):
        """
        Increment package reference counter.

        If ref_counter == 0:
            current package is root
        If ref_counter == 1:
            there is no package which require current
        If ref_counter > 1:
            there are some package which require current
        """
        self.ref_counter += 1

    @property
    def version(self) -> str:
        """Return installed package version"""
        return self._package.version
