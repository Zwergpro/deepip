from typing import List, Optional

from deepip.core.package import Package
from deepip.core.requirement import RequirementInfo


class DepNode:
    """Node of dependencies tree"""

    package: Package
    requirement: Optional[RequirementInfo]
    children: List['DepNode']
    parent: Optional['DepNode'] = None

    def __init__(self, package, requirement: Optional[RequirementInfo] = None):
        self.requirement = requirement
        self.package = package
        self.children = []

    @property
    def name(self):
        """Return name of represented package if it's not root node'"""
        return self.package.name if self.package else ''

    @property
    def version(self) -> str:
        """
        Return version of represented package.

        Top level packages don't have 'parents' and required version, only installed version.
        """
        if self.requirement is None:
            return f'({self.package.version})'  # top level package

        required = self.requirement.specifier or 'Any'
        return f'[required: {required}, installed: {self.package.version}]'

    def __repr__(self):
        return 'root_node' if self.is_root else self.name

    @property
    def is_root(self) -> bool:
        """Is it root node without parents"""
        return self.parent is None

    def add_child(self, package, requirement: Optional[RequirementInfo] = None) -> 'DepNode':
        """Add child node to current node"""
        child_node = DepNode(package, requirement)
        self.children.append(child_node)
        child_node.package.incr_ref_counter()
        child_node.parent = self
        return child_node

    def get_child(self, package_name) -> Optional['DepNode']:
        """Return child node by name"""
        for child in self.children:
            if child.package.name == package_name:
                return child
        return None
