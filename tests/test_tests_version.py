"""Integration tests for test_version.py generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_tests_version_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/test_version.py is generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    test_version = result.project_dir / 'tests' / 'test_version.py'
    assert test_version.exists()


def test_tests_version_contains_import(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/test_version.py imports the package."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers.get('project_package', 'test_project')
    content = (result.project_dir / 'tests' / 'test_version.py').read_text()
    assert f'import {package}' in content


def test_tests_version_contains_version_tests(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/test_version.py contains version test functions."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / 'tests' / 'test_version.py').read_text()
    assert 'test_version_is_string' in content
    assert 'test_version_format' in content
