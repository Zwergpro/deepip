from typing import Optional


class RequirementInfo:
    _requirement = None

    def __init__(self, requirement: Optional = None):
        self._requirement = requirement

    @property
    def specifier(self) -> str:
        return str(self._requirement.specifier)
