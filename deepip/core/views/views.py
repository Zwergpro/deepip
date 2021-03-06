import operator
import sys

from deepip.core.views.formating import Color
from deepip.core.node import DepNode


MIDDLE_NODE_TREE_CHARACTER = '├──'
LAST_NODE_TREE_CHARACTER = '└──'
CHILD_OFFSET = ' ' * 3


class SimpleView:
    """Class for dependencies tree representation"""

    root_node: DepNode
    show_version: bool = False

    def __init__(self, root: DepNode, show_version: bool = False):
        self.root_node = root
        self.show_version = show_version

    def show(self):
        """Print dependencies tree"""
        self._print_tree(self.root_node)

    @staticmethod
    def get_formatted_version(node: DepNode) -> str:
        """Return versions in string format"""
        version = node.get_version()

        if version.specifier is None:
            if version.latest:
                latest_version = version.latest
                if version.installed != latest_version:
                    latest_version = Color.fill(latest_version, Color.CYELLOW2)
                return f'({version.installed}, latest: {latest_version})'  # top level package

            return f'({version.installed})'

        version_specification = version.as_dict()
        if version.latest and version.latest != version.installed:
            version_specification['latest'] = Color.fill(version.latest, Color.CYELLOW2)

        version_info = ', '.join(f'{key}: {value}' for key, value in version_specification.items())
        return f'[{version_info}]'

    def _print_package_info(self, node: DepNode) -> None:
        """Print information about package"""
        information = [Color.fill(node.name, Color.CBEIGE2)]
        if self.show_version:
            information.append(self.get_formatted_version(node))

        sys.stdout.write(' '.join(information) + '\n')

    def _print_requirement_info(self, node: DepNode, level: int = 0, is_last: bool = False) -> None:
        """Print information about package requirement"""
        tree_character = LAST_NODE_TREE_CHARACTER if is_last else MIDDLE_NODE_TREE_CHARACTER
        offset = CHILD_OFFSET * level
        str_prefix = offset + tree_character

        information = [str_prefix, Color.fill(node.name, Color.CBLUE2)]
        if self.show_version:
            information.append(self.get_formatted_version(node))

        sys.stdout.write(' '.join(information) + '\n')

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
