"""Shared fixtures for integration tests."""

import random

import pytest
from chance import chance  # type: ignore[import-untyped]


@pytest.fixture(scope='function')
def licenses() -> dict[str, dict[str, object]]:
    """Return metadata for each supported copyright license."""
    return {
        'Apache-2.0': {'stub': 'Apache License', 'with_holder': False},
        'BSD-3-Clause': {'stub': 'BSD 3-Clause License', 'with_holder': True},
        'GPL-3.0-or-later': {'stub': 'GNU General Public License', 'with_holder': False},
        'LGPL-3.0-or-later': {'stub': 'GNU Lesser General Public License', 'with_holder': False},
        'MIT': {'stub': 'MIT License', 'with_holder': True},
        'MPL-2.0': {'stub': 'Mozilla Public License', 'with_holder': False},
        'Proprietary': {'stub': 'Proprietary Software License', 'with_holder': True},
        'Unlicense': {'stub': 'http://unlicense.org/', 'with_holder': False},
    }


@pytest.fixture(scope='function')
def copier_answers(licenses: dict[str, dict[str, object]]) -> dict[str, object]:
    """Return a randomized set of valid Copier answers."""
    return {
        'project_name': f'{chance.word()}-{chance.word()}',
        'project_package': f'{chance.word()}_{chance.word()}',
        'project_description': chance.sentence(),
        'project_version': f'{random.randint(0, 10)}.{random.randint(0, 10)}.{random.randint(0, 10)}',
        'project_keywords': f'{chance.word()},{chance.word()},{chance.word()}',
        'copyright_holder_name': chance.name(),
        'copyright_holder_email': chance.email(),
        'copyright_license': chance.pickone(list(licenses.keys())),
        'copyright_year': str(random.randint(2000, 2024)),
        'vcs_github_path': f'{chance.word()}/{chance.word()}-{chance.word()}'.lower(),
        'python_version': chance.pickone(['>=3.10', '>=3.11', '>=3.12']),
    }
