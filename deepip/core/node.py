import operator
import sys
from typing import Dict, List, Optional, Tuple

import pkg_resources


class RequirementInfo:
    _requirement = None

    def __init__(self, requirement=None):
        self._requirement = requirement


class Package:
    __all_packages: Dict[str, 'Package'] = {}

    _package = None
    ref_counter: int

    def __init__(self, package):
        self._package = package

        if package.key in self.__all_packages:
            raise Exception(f'Package {package.key} already exists')

        self.__all_packages[package.key] = self
        self.ref_counter = 1

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


class DepNode:
    _requirement: Optional[RequirementInfo]
    children: List['DepNode']
    parent: Optional['DepNode']
    package: Package

    def __init__(self, package, requirement: Optional[RequirementInfo] = None):
        self._requirement = requirement
        self.package = package
        self.children = []

    @property
    def name(self):
        return self.package.name if self.package else ''

    def __repr__(self):
        return 'root_node' if self.is_root else self.name

    @property
    def is_root(self) -> bool:
        return self._requirement is None

    def add_child(self, package, requirement: RequirementInfo) -> 'DepNode':
        child_node = DepNode(package, requirement)
        self.children.append(child_node)
        child_node.package.incr_ref_counter()
        return child_node

    def print_tree(self, level: int = 0, is_last: bool = False):
        tree_characters = '└── ' if is_last else '├── '

        if self.is_root:
            self.print_subtree(level=0)
            return

        if level == 0:
            sys.stdout.write(f'\033[96m{self.name}\033[0m\n')
        else:
            sys.stdout.write(' ' * 3 * level + tree_characters + self.name + '\n')

        self.print_subtree(level=level + 1)

    def print_subtree(self, level):
        requirements = sorted(self.children, key=operator.attrgetter('name'))
        for index, requirement in enumerate(requirements, start=1):
            requirement.print_tree(level=level, is_last=index == len(self.children))


def build_sub_tree(root_node: DepNode):
    requirements = root_node.package.get_requirements()
    for package, requirement in requirements:
        node = root_node.add_child(package, RequirementInfo(requirement=requirement))
        node.parent = root_node
        build_sub_tree(node)


def build_dep_tree() -> DepNode:
    packages = []
    for pak in pkg_resources.working_set:
        packages.append(Package(pak))

    root = DepNode(package=None)

    for package in packages:
        node = root.add_child(package, RequirementInfo())
        build_sub_tree(node)

    return root
