from deepip.core.requirement import RequirementInfo
from tests.factories.pkg_resources.requirement import requirement_factory


def test_specifier_version_with_two_borders():
    versions = ['<2.2.0', '>=1.0.1']
    requirement = RequirementInfo(requirement_factory(versions=versions))

    assert requirement.specifier == ','.join(versions), 'requirement should specify correct versions'


def test_specifier_version_with_two_borders_and_reverse_order():
    versions = ['>=1.0.1', '<2.2.0']
    requirement = RequirementInfo(requirement_factory(versions=versions))

    assert requirement.specifier == ','.join(reversed(versions)), 'requirement should specify correct order'


def test_specifier_version_with_three_borders():
    versions = ['<2.2.0', '>=0.5.0', '>=1.0.1']
    requirement = RequirementInfo(requirement_factory(versions=versions))

    assert requirement.specifier == ','.join(versions), 'requirement should specify correct versions'


def test_specifier_version_with_one_border():
    versions = ['>=1.0.1']
    requirement = RequirementInfo(requirement_factory(versions=versions))

    assert requirement.specifier == ','.join(versions), 'requirement should specify correct version'


def test_specifier_version_without_borders():
    requirement = RequirementInfo(requirement_factory(versions=[]))

    assert requirement.specifier == RequirementInfo.ANY_VERSION, 'requirement should specify Any version'
