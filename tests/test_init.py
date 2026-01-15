"""Integration tests for __init__.py generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_init_py_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that __init__.py is generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    package = base_answers.get('project_package', 'test_project')
    init_py = result.project_dir / 'src' / package / '__init__.py'
    assert init_py.exists()


def test_init_py_contains_docstring(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that __init__.py contains the project description as docstring."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers.get('project_package', 'test_project')
    content = (result.project_dir / 'src' / package / '__init__.py').read_text()
    assert base_answers['project_description'] in content


def test_init_py_contains_version(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that __init__.py defines __version__."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers.get('project_package', 'test_project')
    content = (result.project_dir / 'src' / package / '__init__.py').read_text()
    assert '__version__' in content
