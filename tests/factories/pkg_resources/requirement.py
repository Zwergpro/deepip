from typing import List, Optional

from pkg_resources import Requirement
import faker

fake = faker.Faker()
faker.Faker.seed(0)


def requirement_factory(name: Optional[str] = None, versions: Optional[List[str]] = None) -> Requirement:
    """Return instance of pkg_resources.Requirement with fake name if not specified"""
    if name is None:
        name = 'package_' + fake.pystr(max_chars=10)

    if versions is None:
        # TODO: add version factory
        versions = ['>=1.4.4', '<2.0.0']

    return Requirement.parse(name + ','.join(versions))
