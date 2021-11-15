import pytest

from deepip.core.node import DepNode
from deepip.core.package import Package
from deepip.core.requirement import RequirementInfo
from tests.factories.pkg_resources.package import package_factory
from tests.factories.pkg_resources.requirement import requirement_factory


@pytest.fixture(scope='function')
def root():
    return DepNode(package=None)


@pytest.fixture(scope='function')
def package():
    return Package(package_factory())


def test_root_node_without_name(root):
    assert root.name == DepNode.ROOT_NODE_NAME, 'root node should have ROOT_NODE_NAME in name'


def test_node_with_name(root, package):
    child = root.add_child(package)

    assert child.name == package.name, 'node should have same name with package'


def test_repr_root_node_without_name(root):
    assert repr(root) == DepNode.ROOT_NODE_NAME, 'root node should have ROOT_NODE_NAME'


def test_repr_node_with_name(root, package):
    child = root.add_child(package)

    assert repr(child) == package.name, 'node should have same name with package'


def test_root_node_is_root(root):
    assert root.is_root, 'root node should return True'


def test_child_node_is_root(root, package):
    child = root.add_child(package)

    assert not child.is_root, 'child node should return False'


def test_child_node_has_parent(root):
    child = root.add_child(Package(package_factory()))

    assert child.parent == root, 'child node should have parent'


def test_parent_node_has_child(root):
    child = root.add_child(Package(package_factory()))

    assert root.children == [child], 'parent node should have list of children'


def test_node_without_children_try_to_get_child_by_name(root):
    assert root.get_child('test_name') is None, 'can not get child from node without children'


def test_node_with_children_try_to_get_child_by_name(root):
    root.add_child(Package(package_factory()))
    child = root.add_child(Package(package_factory()))

    assert root.get_child(child.name) == child, 'node with children should return child node'


def test_node_version_without_requirement(root):
    version = '1.1.1'
    package = Package(package_factory(version=version))
    child = root.add_child(package)

    assert child.version == f'({version})', 'node without requirement should return only installed version'


def test_node_version_with_requirement(root):
    package = Package(package_factory())
    requirement = RequirementInfo(requirement_factory())
    child = root.add_child(package, requirement)
    expected_version = f'[required: {requirement.specifier}, installed: {package.version}]'

    assert child.version == expected_version, 'node with requirement should return only installed and required versions'


def test_node_version_with_requirement_without_version(root):
    package = Package(package_factory())
    requirement = RequirementInfo(requirement_factory(versions=['']))
    child = root.add_child(package, requirement)
    expected_version = f'[required: {requirement.ANY_VERSION}, installed: {package.version}]'

    assert (
        child.version == expected_version
    ), 'node with requirement without version should return only installed versions and Any'
