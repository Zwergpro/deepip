from deepip.core.requirement import RequirementInfo
from tests.factories.pkg_resources.requirement import requirement_factory


class TestRequirementSpecifier:

    def test_specifier_version_with_two_borders(self):
        versions = ['<2.2.0', '>=1.0.1']
        requirement = RequirementInfo(requirement_factory(versions=versions))

        assert requirement.specifier == ','.join(versions)

    def test_specifier_version_with_two_borders_and_reverse_order(self):
        versions = ['>=1.0.1', '<2.2.0']
        requirement = RequirementInfo(requirement_factory(versions=versions))

        assert requirement.specifier == ','.join(reversed(versions))

    def test_specifier_version_with_three_borders(self):
        versions = ['<2.2.0', '>=0.5.0', '>=1.0.1']
        requirement = RequirementInfo(requirement_factory(versions=versions))

        assert requirement.specifier == ','.join(versions)

    def test_specifier_version_with_one_border(self):
        versions = ['>=1.0.1']
        requirement = RequirementInfo(requirement_factory(versions=versions))

        assert requirement.specifier == ','.join(versions)

    def test_specifier_version_without_borders(self):
        requirement = RequirementInfo(requirement_factory(versions=[]))

        assert requirement.specifier == ''
