"""Integration tests for license generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_copie.plugin import Copie

LICENSE_TYPES = [
    'MIT',
    'Apache-2.0',
    'BSD-3-Clause',
    'GPL-3.0-or-later',
    'LGPL-3.0-or-later',
    'MPL-2.0',
    'Proprietary',
    'Unlicense',
]

# Licenses that are static files (not Jinja2 templates) and don't include copyright information
STATIC_LICENSES = {
    'Apache-2.0',
    'GPL-3.0-or-later',
    'LGPL-3.0-or-later',
    'MPL-2.0',
    'Unlicense',
}

LICENSE_SIGNATURES: dict[str, str] = {
    'MIT': 'MIT License',
    'Apache-2.0': 'Apache License',
    'BSD-3-Clause': 'BSD 3-Clause License',
    'GPL-3.0-or-later': 'GNU GENERAL PUBLIC LICENSE',
    'LGPL-3.0-or-later': 'GNU LESSER GENERAL PUBLIC LICENSE',
    'MPL-2.0': 'Mozilla Public License Version 2.0',
    'Proprietary': 'Proprietary Software License',
    'Unlicense': 'This is free and unencumbered software released into the public domain.',
}


def verify_license_type(license_path: Path, license_type: str) -> None:
    """Verify LICENSE file is the correct type.

    Args:
        license_path: Path to the LICENSE file.
        license_type: Expected license type (e.g., 'MIT', 'Apache-2.0').
    """
    assert license_path.exists(), f'LICENSE file not found at {license_path}'
    content = license_path.read_text()
    signature = LICENSE_SIGNATURES[license_type]
    assert signature in content, f'Expected {license_type} signature "{signature}" not found in LICENSE'


def verify_license_content(
    license_path: Path,
    holder_name: str,
    year: int,
    email: str,
    check_copyright: bool = True,
) -> None:
    """Verify LICENSE file contains expected copyright information.

    Args:
        license_path: Path to the LICENSE file.
        holder_name: Expected copyright holder name.
        year: Expected copyright year.
        email: Expected copyright holder email.
        check_copyright: Whether to check for copyright information.
            Set to False for static license files that don't include
            copyright information (e.g., Apache-2.0, GPL, LGPL, MPL, Unlicense).
    """
    assert license_path.exists(), f'LICENSE file not found at {license_path}'
    content = license_path.read_text()
    if check_copyright:
        assert str(year) in content, f'Year {year} not found in LICENSE'
        assert holder_name, 'holder_name is empty'
        assert holder_name in content, f"Holder name '{holder_name}' not found in LICENSE"
        assert email, 'email is empty'
        assert email in content, f"Email '{email}' not found in LICENSE"
    else:
        assert content.strip(), f'LICENSE file is empty at {license_path}'


@pytest.mark.parametrize('license_type', LICENSE_TYPES)
def test_license_generation(
    copie: Copie,
    base_answers: dict[str, str],
    license_type: str,
) -> None:
    """Test that project generates correct LICENSE for each license type."""
    answers = {**base_answers, 'copyright_license': license_type}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0, f'Project generation failed with exit code {result.exit_code}'
    assert result.exception is None, f'Project generation raised exception: {result.exception}'
    assert result.project_dir is not None, 'Project directory not created'
    assert result.project_dir.is_dir(), 'Project directory is not a directory'

    # Find LICENSE file (may have different names)
    license_files = list(result.project_dir.glob('LICENSE*')) + list(result.project_dir.glob('UNLICENSE*'))
    assert len(license_files) > 0, f'No LICENSE file found for {license_type}'
    license_path = license_files[0]

    # Verify correct license type was generated
    verify_license_type(license_path, license_type)

    # Verify content using answers from result
    # Static licenses don't include copyright information
    check_copyright = license_type not in STATIC_LICENSES
    verify_license_content(
        license_path=license_path,
        holder_name=result.answers.get('copyright_holder_name', ''),
        year=result.answers['copyright_year'],
        email=result.answers.get('copyright_holder_email', ''),
        check_copyright=check_copyright,
    )


def test_context_injection(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that context.py extension injects dynamic values."""
    answers = {**base_answers, 'copyright_license': 'MIT'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None

    # Verify copyright_year default renders via now.year
    assert 'copyright_year' in result.answers
    assert isinstance(result.answers['copyright_year'], int)
    assert result.answers['copyright_year'] > 2000

    # Verify git values are available (may be empty in CI)
    assert 'copyright_holder_name' in result.answers
    assert 'copyright_holder_email' in result.answers
