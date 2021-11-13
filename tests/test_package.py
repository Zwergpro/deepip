import pytest

from deepip.core.package import Package
from tests.factories.pkg_resources.package import package_factory
from tests.factories.pkg_resources.requirement import requirement_factory


@pytest.fixture(scope='function', autouse=True)
def flush_package_global_storage():
    Package.flush_storage()


def test_package_reference_to_original():
    row_package = package_factory()
    package = Package(row_package)

    assert package._package == row_package, 'not root package should have reference to original package'


def test_package_global_storage():
    packages = [Package(package_factory()), Package(package_factory())]
    expected_packages = {package.name: package for package in packages}

    assert Package.get_global_storage_copy() == expected_packages, 'global storage should store all packages'


def test_ref_counter_initialization():
    package = Package(package_factory())

    assert package.ref_counter == 0, 'init value should be 0'


def test_increment_ref_counter():
    package = Package(package_factory())
    package.ref_counter = 0

    package.incr_ref_counter()

    assert package.ref_counter == 1, 'function should increase the counter by 1'


def test_get_package_name():
    test_name = 'test-lib'
    package = Package(package_factory(project_name=test_name))

    assert package.name == test_name, 'package name and project name should be same'


def test_package_name_with_underline():
    test_name = 'test_lib'
    package = Package(package_factory(project_name=test_name))

    assert package.name == test_name.replace('_', '-'), 'package name must not contains underlines'


def test_some_packages_with_same_name():
    package = Package(package_factory())

    with pytest.raises(Exception, match=f'Package {package.name} already exists'):
        Package(package_factory(project_name=package.name))


def test_package_version():
    version = '1.5.0'
    package = Package(package_factory(version=version))

    assert package.version == version, 'package version should be same'


def test_package_without_requirements():
    package = Package(package_factory())

    assert package.get_requirements() == [], 'package must not contains requirements'


def test_package_get_requirements():
    requirement_packages = [Package(package_factory()), Package(package_factory())]
    requirements = (requirement_factory(package.name) for package in requirement_packages)

    package = Package(package_factory(requirements=requirements))
    expected_requirements = [(package, requirement) for package, requirement in zip(requirement_packages, requirements)]

    assert package.get_requirements() == expected_requirements, 'package should contains requirements'
