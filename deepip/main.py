import operator
import sys
from typing import Dict

import pkg_resources


class Requirement:
    """pkg_resources.Requirement wrapper"""

    _package: 'Package'
    _requirement: pkg_resources.Requirement

    @property
    def name(self):
        return self._package.name

    def __init__(self, requirement: pkg_resources.Requirement, package: 'Package'):
        self._requirement = requirement
        self._package = package

    def __str__(self) -> str:
        require = f'require:{self._requirement.specifier}; ' if self._requirement.specifier else ''
        version = f'installed:{self._package.version}'
        return f'{self._requirement.name} [{require}{version}]'

    def print_requirement_tree(self, level: int = 0, is_last: bool = False):
        tree_characters = '└── ' if is_last else '├── '

        if level == 0:
            sys.stdout.write(f'{self}\n')
        else:
            sys.stdout.write(' ' * 3 * level + tree_characters + str(self) + '\n')

        requirements = sorted(self._package.requirements.values(), key=operator.attrgetter('name'))
        for require in requirements:
            require.print_requirement_tree(level + 1)


class Package:
    """pkg_resources.DistInfoDistribution wrapper"""

    requirements: Dict[str, Requirement]
    has_parent: bool
    _package: pkg_resources.DistInfoDistribution

    def __init__(self, source: pkg_resources.DistInfoDistribution):
        self._package = source
        self.requirements = {}
        self.has_parent = False

    @property
    def name(self) -> str:
        return self._package.key

    @property
    def version(self) -> str:
        return self._package.version

    def add_requirement(self, package: 'Package', requirement: pkg_resources.Requirement):
        self.requirements[package.name] = Requirement(requirement, package)
        package.has_parent = True

    @property
    def has_requires(self) -> bool:
        return bool(self._package.requires())

    def get_requires(self, installed_packages: Dict[str, 'Package']) -> ('Package', pkg_resources.Requirement):
        return [(installed_packages[require.key], require) for require in self._package.requires()]

    def __str__(self) -> str:
        return f'{self.name} [{self.version}]'

    def print_requirement_tree(self, level: int = 0, is_last: bool = False):
        tree_characters = '└── ' if is_last else '├── '

        if level == 0:
            sys.stdout.write(f'\033[96m{self}\033[0m\n')
        else:
            sys.stdout.write(' ' * 3 * level + tree_characters + str(self) + '\n')

        requirements = sorted(self.requirements.values(), key=operator.attrgetter('name'))
        for require in requirements:
            require.print_requirement_tree(level + 1)


class DependencyTree:
    packages: Dict[str, Package]

    def __init__(self, packages: Dict[str, Package]):
        self.packages = packages

    def values(self):
        return self.packages.values()


def build_requirements_tree() -> DependencyTree:
    installed_packages = {}

    for pak in pkg_resources.working_set:
        installed_packages[pak.key] = Package(pak)

    for package in installed_packages.values():
        for requirement_package, requirement in package.get_requires(installed_packages):
            package.add_requirement(requirement_package, requirement)

    return DependencyTree(packages=installed_packages)


def simple_print_dep_tree(dep_tree: DependencyTree):
    dependencies = sorted(dep_tree.values(), key=operator.attrgetter('name'))

    for value in dependencies:
        if value.has_parent:
            continue

        value.print_requirement_tree()


def print_dep_tree():
    dep_tree = build_requirements_tree()
    simple_print_dep_tree(dep_tree)


def print_dep_tree_for_package(package_name: str):
    dep_tree = build_requirements_tree()
    package = dep_tree.packages[package_name]
    package.print_requirement_tree()
