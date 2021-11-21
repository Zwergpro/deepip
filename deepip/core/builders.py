import pkg_resources

from deepip.core.api.pypi_api import get_package_meta
from deepip.core.node import DepNode
from deepip.core.package import Package
from deepip.core.requirement import RequirementInfo


def build_sub_tree(root_node: DepNode) -> None:
    """Recursively build dependencies subtree of given node"""
    requirements = root_node.package.get_requirements()
    for package, requirement in requirements:
        node = root_node.add_child(package, RequirementInfo(requirement=requirement))
        node.parent = root_node
        build_sub_tree(node)


def build_dep_tree(with_meta: bool = False) -> DepNode:
    """
    Build dependencies tree and return root node.

    Depends on pkg_resources module.
    """
    packages = []
    working_set = list(pkg_resources.working_set)
    for pak in working_set:
        package = Package(pak)
        packages.append(package)
        if with_meta:
            package.meta = get_package_meta(package.name)

    root = DepNode(package=None)

    for package in packages:
        node = root.add_child(package)
        build_sub_tree(node)

    return root
