"""Integration tests for pyproject.toml generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_pyproject_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that pyproject.toml is generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    pyproject = result.project_dir / 'pyproject.toml'
    assert pyproject.exists()


def test_pyproject_metadata(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test pyproject.toml contains correct metadata."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / 'pyproject.toml').read_text()
    assert f'name = "{base_answers["project_name"]}"' in content
    assert f'description = "{base_answers["project_description"]}"' in content


def test_pyproject_urls(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test pyproject.toml contains correct URLs."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / 'pyproject.toml').read_text()
    github_path = base_answers['vcs_github_path']
    assert f'https://github.com/{github_path}' in content


def test_pyproject_version_list_filter(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that version_list Jinja2 filter renders Python classifiers correctly."""
    answers = {**base_answers, 'python_version': '>=3.13'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / 'pyproject.toml').read_text()
    assert '"Programming Language :: Python :: 3.13"' in content
    assert '"Programming Language :: Python :: 3.14"' in content
    assert '"Programming Language :: Python :: 3.12"' not in content


def test_pyproject_with_cli(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test pyproject.toml includes CLI dependencies when with_cli is true."""
    answers = {**base_answers, 'with_cli': True}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / 'pyproject.toml').read_text()
    assert 'typer>=0.26.7' in content
    assert f'scripts.{base_answers["project_name"]} = "{base_answers["project_package"]}.cli:app"' in content


def test_pyproject_without_cli(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test pyproject.toml excludes CLI dependencies when with_cli is false."""
    answers = {**base_answers, 'with_cli': False}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / 'pyproject.toml').read_text()
    assert 'typer' not in content
    assert 'scripts.' not in content
