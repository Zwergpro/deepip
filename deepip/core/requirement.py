from typing import Optional


class RequirementInfo:
    """
    Class to wrap pkg_resources.Requirement and represent package requirement information.

    https://setuptools.pypa.io/en/latest/pkg_resources.html#requirement-objects
    """

    ANY_VERSION = 'Any'

    _requirement = None

    def __init__(self, requirement: Optional = None):
        self._requirement = requirement

    @property
    def specifier(self) -> str:
        """Return required package version"""
        return str(self._requirement.specifier) if self._requirement.specifier else self.ANY_VERSION

    def __eq__(self, other: 'RequirementInfo') -> bool:
        """Compare two RequirementInfo objects"""
        return self._requirement == other._requirement
