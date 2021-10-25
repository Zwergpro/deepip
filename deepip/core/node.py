import operator
import sys
from typing import Dict, List, Optional, Tuple

import pkg_resources


class RequirementInfo:
    _requirement = None
    _package = None

    def __init__(self, package=None, requirement=None):
        self._package = package
        self._requirement = requirement


class Package:
    __all_packages: Dict[str, 'Package'] = {}

    _package = None

    def __init__(self, package):
        self._package = package
        self.__all_packages[package.key] = self

    def get_requirements(self) -> List[Tuple['Package', RequirementInfo]]:
        requirements = []
        for requirement in self._package.requires():
            requirements.append((self.__all_packages[requirement.key], RequirementInfo(requirement)))
        return requirements

    @property
    def name(self):
        return self._package.key


class DepNode:
    _requirement: Optional[RequirementInfo]
    children: List['DepNode']
    parent: Optional['DepNode']
    package: Package

    def __init__(self, requirement: Optional[RequirementInfo] = None):
        self._requirement = requirement
        self.package = requirement._package if requirement is not None else None
        self.children = []

    @property
    def name(self):
        return self.package.name if self.package else ''

    def __repr__(self):
        return 'root_node' if self.is_root else self.name

    @property
    def is_root(self) -> bool:
        return self._requirement is None

    def add_child(self, requirement: RequirementInfo) -> 'DepNode':
        child_node = DepNode(requirement)
        self.children.append(child_node)
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
    requirements = root_node._requirement._package.get_requirements()
    for package, requirement in requirements:
        node = root_node.add_child(RequirementInfo(package=package, requirement=requirement))
        node.parent = root_node
        build_sub_tree(node)


def build_dep_tree() -> DepNode:
    packages = []
    for pak in pkg_resources.working_set:
        packages.append(Package(pak))

    root = DepNode()

    for package in packages:
        node = root.add_child(RequirementInfo(package=package))
        build_sub_tree(node)

    return root
