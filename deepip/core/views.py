import operator
import sys

from deepip.core.node import DepNode


class SimpleView:
    root_node: DepNode

    def __init__(self, root: DepNode):
        self.root_node = root

    def show(self):
        self._print_tree(self.root_node)

    def _print_tree(self, node: DepNode, level: int = 0, is_last: bool = False):
        tree_characters = '└── ' if is_last else '├── '

        if node.is_root:
            self._print_subtree(node, level=0)
            return

        if node.parent.is_root and node.package.ref_counter > 1:
            return  # don't show packages with several references, they will be showed in subtree

        if level == 0:
            sys.stdout.write(f'\033[96m{node.name}\033[0m {node.version}\n')
        else:
            sys.stdout.write(' ' * 3 * level + tree_characters + node.name + f' {node.version}\n')

        self._print_subtree(node, level=level + 1)

    def _print_subtree(self, node: DepNode, level):
        requirements = sorted(node.children, key=operator.attrgetter('name'))
        for index, requirement in enumerate(requirements, start=1):
            self._print_tree(requirement, level=level, is_last=index == len(node.children))
