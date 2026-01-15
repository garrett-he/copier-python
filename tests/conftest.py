"""Test fixtures and configuration."""

from __future__ import annotations

import pytest
from chance import chance


@pytest.fixture
def base_answers() -> dict[str, str]:
    """Return random project answers generated via chance."""
    holder = chance.name()
    project_name = chance.word() + '-' + chance.word()
    project_package = project_name.replace('-', '_')
    major = chance.random.randint(0, 10)
    minor = chance.random.randint(0, 50)
    patch = chance.random.randint(0, 100)
    return {
        'project_name': project_name,
        'project_package': project_package,
        'project_description': f'A test project by {holder}.',
        'project_version': f'{major}.{minor}.{patch}',
        'project_keywords': f'{chance.word()}, {chance.word()}',
        'vcs_github_path': f'{holder.lower().replace(" ", "-")}/{project_name}',
        'copyright_holder_name': holder,
        'copyright_holder_email': chance.email(),
    }
