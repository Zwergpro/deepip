from typing import Dict, List, Tuple

from deepip.core.requirement import RequirementInfo


class Package:
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
        requirements = []
        for requirement in self._package.requires():
            requirements.append((self.__all_packages[requirement.key], RequirementInfo(requirement)))
        return requirements

    @property
    def name(self):
        return self._package.key

    def incr_ref_counter(self):
        self.ref_counter += 1

    @property
    def version(self) -> str:
        return self._package.version
