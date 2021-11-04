import operator
import sys
from typing import Optional

from deepip.core.node import DepNode


MIDDLE_NODE_TREE_CHARACTER = '├──'
LAST_NODE_TREE_CHARACTER = '└──'
CHILD_OFFSET = ' ' * 3


class Color:
    CEND = '0m'
    CBOLD = '1m'
    CITALIC = '3m'
    CURL = '4m'
    CBLINK = '5m'
    CBLINK2 = '6m'
    CSELECTED = '7m'

    CBLACK = '30m'
    CRED = '31m'
    CGREEN = '32m'
    CYELLOW = '33m'
    CBLUE = '34m'
    CVIOLET = '35m'
    CBEIGE = '36m'
    CWHITE = '37m'

    CBLACKBG = '40m'
    CREDBG = '41m'
    CGREENBG = '42m'
    CYELLOWBG = '43m'
    CBLUEBG = '44m'
    CVIOLETBG = '45m'
    CBEIGEBG = '46m'
    CWHITEBG = '47m'

    CGREY = '90m'
    CRED2 = '91m'
    CGREEN2 = '92m'
    CYELLOW2 = '93m'
    CBLUE2 = '94m'
    CVIOLET2 = '95m'
    CBEIGE2 = '96m'
    CWHITE2 = '97m'

    CGREYBG = '100m'
    CREDBG2 = '101m'
    CGREENBG2 = '102m'
    CYELLOWBG2 = '103m'
    CBLUEBG2 = '104m'
    CVIOLETBG2 = '105m'
    CBEIGEBG2 = '106m'
    CWHITEBG2 = '107m'

    @staticmethod
    def fill(string: str, color_code: str) -> str:
        """Set the color design of the string to output to the console"""
        return f'\033[{color_code}{string}\033[0m'


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
        name = Color.fill(node.name, Color.CBEIGE2)
        sys.stdout.write(f'{name} {node.version}\n')

    @staticmethod
    def _print_requirement_info(node: DepNode, level: int = 0, is_last: bool = False) -> None:
        """Print information about package requirement"""
        tree_character = LAST_NODE_TREE_CHARACTER if is_last else MIDDLE_NODE_TREE_CHARACTER
        offset = CHILD_OFFSET * level
        str_prefix = offset + tree_character

        sys.stdout.write(f'{str_prefix} {node.name} {node.version}\n')

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
