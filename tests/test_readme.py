"""Integration tests for README.md generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
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

LICENSE_SIGNATURES: dict[str, str] = {
    'MIT': 'MIT License',
    'Apache-2.0': 'Apache License, Version 2.0',
    'BSD-3-Clause': 'BSD 3-Clause License',
    'GPL-3.0-or-later': 'GNU General Public License (GPL) version 3',
    'LGPL-3.0-or-later': 'GNU Lesser General Public License (GPL) version 3',
    'MPL-2.0': 'Mozilla Public License 2.0',
    'Proprietary': 'Proprietary Software License',
}


def test_readme_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that README.md is generated."""
    answers = {**base_answers, 'copyright_license': 'MIT'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    readme = result.project_dir / 'README.md'
    assert readme.exists()
    content = readme.read_text()
    assert f'# {answers["project_name"]}' in content
    assert answers['project_description'] in content
    assert answers['vcs_github_path'] in content


def test_readme_title(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test README title matches project_name."""
    answers = {**base_answers, 'copyright_license': 'MIT', 'project_name': 'foo-bar'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None
    readme = result.project_dir / 'README.md'
    content = readme.read_text()
    assert content.startswith('# foo-bar\n')


def test_readme_license_badge_present(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test license badge appears for non-Unlicense licenses."""
    answers = {**base_answers, 'copyright_license': 'MIT'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None
    readme = result.project_dir / 'README.md'
    content = readme.read_text()
    assert f'img.shields.io/github/license/{answers["vcs_github_path"]}' in content


def test_readme_license_badge_absent_for_unlicense(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test license badge is absent for Unlicense."""
    answers = {**base_answers, 'copyright_license': 'Unlicense'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None
    readme = result.project_dir / 'README.md'
    content = readme.read_text()
    assert 'img.shields.io/github/license' not in content


@pytest.mark.parametrize('license_type', LICENSE_TYPES)
def test_readme_license_section(
    copie: Copie,
    base_answers: dict[str, str],
    license_type: str,
) -> None:
    """Test README license section content for each license type."""
    answers = {**base_answers, 'copyright_license': license_type}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    readme = result.project_dir / 'README.md'
    assert readme.exists()
    content = readme.read_text()

    assert '## License' in content

    if license_type == 'Unlicense':
        assert 'free and unencumbered software' in content
    else:
        signature = LICENSE_SIGNATURES[license_type]
        assert signature in content
        assert 'Copyright (C)' in content
        assert result.answers['copyright_holder_name'] in content
        assert result.answers['copyright_holder_email'] in content
        assert str(result.answers['copyright_year']) in content


def test_readme_ci_badge(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test CI badge uses vcs_github_path."""
    answers = {**base_answers, 'copyright_license': 'MIT', 'vcs_github_path': 'my-org/my-repo'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None
    readme = result.project_dir / 'README.md'
    content = readme.read_text()
    assert 'my-org/my-repo' in content
    assert 'github.com/my-org/my-repo/actions' in content


def test_readme_proprietary_license_name(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test Proprietary license uses holder name in description."""
    answers = {**base_answers, 'copyright_license': 'Proprietary', 'copyright_holder_name': 'ACME Corp'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None
    readme = result.project_dir / 'README.md'
    content = readme.read_text()
    assert 'ACME Corp Proprietary Software License' in content
