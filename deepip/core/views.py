import operator
import sys
from typing import Optional

from deepip.core.node import DepNode


MIDDLE_NODE_TREE_CHARACTER = '├── '
LAST_NODE_TREE_CHARACTER = '└── '


class SimpleView:
    root_node: DepNode
    options = None

    def __init__(self, root: DepNode, options: Optional = None):
        self.root_node = root
        self.options = options

    def show(self):
        """Print dependencies tree"""
        self._print_tree(self.root_node)

    @staticmethod
    def _print_package_info(node: DepNode) -> None:
        """Print information about package"""
        sys.stdout.write(f'\033[96m{node.name}\033[0m {node.version}\n')

    @staticmethod
    def _print_requirement_info(node: DepNode, level: int = 0, is_last: bool = False) -> None:
        """Print information about package requirement"""
        tree_character = LAST_NODE_TREE_CHARACTER if is_last else MIDDLE_NODE_TREE_CHARACTER
        sys.stdout.write(' ' * 3 * level + tree_character + node.name + f' {node.version}\n')

    def _print_tree(self, node: DepNode, level: int = 0, is_last: bool = False) -> None:
        """Print information about specified node and all child nodes"""
        if node.is_root:
            self._print_subtree(node, level=0)
            return

        if node.parent.is_root and node.package.ref_counter > 1:
            return  # don't show packages with several references, they will be showed in subtree

        if level == 0:
            self._print_package_info(node)
        else:
            self._print_requirement_info(node, level, is_last)

        self._print_subtree(node, level=level + 1)

    def _print_subtree(self, node: DepNode, level: int) -> None:
        """Print information about all child nodes"""
        requirements = sorted(node.children, key=operator.attrgetter('name'))
        for index, requirement in enumerate(requirements, start=1):
            self._print_tree(requirement, level=level, is_last=index == len(node.children))
