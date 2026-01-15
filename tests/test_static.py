"""Integration tests for static file generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie

STATIC_FILES = [
    '.editorconfig',
    '.gitattributes',
    '.gitignore',
    'CHANGELOG.md',
    'justfile',
    '.pre-commit-config.yaml',
]


def test_static_files_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that all static files are generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    for filename in STATIC_FILES:
        filepath = result.project_dir / filename
        assert filepath.exists(), f'Static file {filename} not found'


def test_py_typed_marker_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that py.typed marker file is generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers.get('project_package', 'test_project')
    py_typed = result.project_dir / 'src' / package / 'py.typed'
    assert py_typed.exists(), f'py.typed marker not found at {py_typed}'
