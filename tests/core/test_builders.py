import pytest
from pkg_resources import WorkingSet
from pytest_mock import MockerFixture

from deepip.core.builders import build_dep_tree
from tests.factories.pkg_resources.package import package_factory
from tests.factories.pkg_resources.requirement import requirement_factory


@pytest.fixture(scope='function')
def working_set_mock(mocker: MockerFixture) -> WorkingSet:
    """Mock and return global pkg_resources.working_set"""
    working_set = WorkingSet([])
    mocker.patch('pkg_resources.working_set', working_set)
    return working_set


def test_builder_with_top_level_packages_return_root(working_set_mock):
    row_package = package_factory()
    working_set_mock.add(row_package, entry='/')

    root = build_dep_tree()

    assert root.is_root, 'build_dep_tree should return root node'


def test_builder_with_top_level_packages(working_set_mock):
    row_package = package_factory()
    working_set_mock.add(row_package, entry='/')

    root = build_dep_tree()

    assert len(root.children) == 1, 'root node should contain one child node'
    assert root.children[0].package._package == row_package, 'child node should reference to row package'


def test_builder_with_two_children_on_top_level(working_set_mock):
    required_package = package_factory()
    working_set_mock.add(required_package, entry='/')
    main_package = package_factory(requirements=[requirement_factory(required_package.key)])
    working_set_mock.add(main_package, entry='/')

    root = build_dep_tree()

    packages = set(node.package._package for node in root.children)
    assert packages == {main_package, required_package}, 'root node should have two children node'


def test_builder_with_sub_tree(working_set_mock):
    required_package = package_factory()
    working_set_mock.add(required_package, entry='/')
    main_package = package_factory(requirements=[requirement_factory(required_package.key)])
    working_set_mock.add(main_package, entry='/')

    root = build_dep_tree()

    parent_node = root.get_child_by_name(main_package.key)
    child_node = root.get_child_by_name(required_package.key)
    assert parent_node.get_child_by_name(child_node.name) is not None, 'parent node should contain required child node'
