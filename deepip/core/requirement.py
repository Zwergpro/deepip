from typing import Optional


class RequirementInfo:
    _requirement = None

    def __init__(self, requirement: Optional = None):
        self._requirement = requirement
