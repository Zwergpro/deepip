from typing import Optional


class RequirementInfo:
    """
    Class to wrap pkg_resources.Requirement and represent package requirement information.

    https://setuptools.pypa.io/en/latest/pkg_resources.html#requirement-objects
    """

    _requirement = None

    def __init__(self, requirement: Optional = None):
        self._requirement = requirement

    @property
    def specifier(self) -> str:
        """Return required package version"""
        return str(self._requirement.specifier)
