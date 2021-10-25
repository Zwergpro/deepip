import operator
import sys
from typing import List, Optional

from deepip.core.package import Package
from deepip.core.requirement import RequirementInfo


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
        child_node.parent = self
        return child_node

    def get_child(self, package_name) -> Optional['DepNode']:
        for child in self.children:
            if child.package.name == package_name:
                return child
        return None

    def print_tree(self, level: int = 0, is_last: bool = False):
        tree_characters = '└── ' if is_last else '├── '

        if self.is_root:
            self.print_subtree(level=0)
            return

        if self.parent.is_root and self.package.ref_counter > 1:
            return  # don't show packages with several references, they will be showed in subtree

        if level == 0:
            sys.stdout.write(f'\033[96m{self.name}\033[0m\n')
        else:
            sys.stdout.write(' ' * 3 * level + tree_characters + self.name + '\n')

        self.print_subtree(level=level + 1)

    def print_subtree(self, level):
        requirements = sorted(self.children, key=operator.attrgetter('name'))
        for index, requirement in enumerate(requirements, start=1):
            requirement.print_tree(level=level, is_last=index == len(self.children))
