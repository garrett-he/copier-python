"""Integration tests for tests/__init__.py generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_tests_init_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/__init__.py is generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    init_py = result.project_dir / 'tests' / '__init__.py'
    assert init_py.exists()


def test_tests_init_contains_package_name(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/__init__.py contains the package name in docstring."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers.get('project_package', 'test_project')
    content = (result.project_dir / 'tests' / '__init__.py').read_text()
    assert package in content
