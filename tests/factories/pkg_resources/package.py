from typing import Optional, Iterable

import faker
from pkg_resources import DistInfoDistribution, Requirement

fake = faker.Faker()
faker.Faker.seed(0)


def package_factory(
    project_name: Optional[str] = None,
    version: Optional[str] = None,
    requirements: Optional[Iterable[Requirement]] = None,
) -> DistInfoDistribution:
    """Return new instance of pkg_resources.DistInfoDistribution with requirements"""
    if project_name is None:
        project_name = 'package_' + fake.pystr(max_chars=10)

    if version is None:
        # TODO: add version factory
        version = '1.0.0'

    distribution = DistInfoDistribution(project_name=project_name, version=version)

    if requirements:
        for requirement in requirements:
            assert isinstance(requirement, Requirement), \
                'requirements should contains only pkg_resources.Requirement instances'
        setattr(distribution, '_DistInfoDistribution__dep_map', {None: requirements})

    return distribution
