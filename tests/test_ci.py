"""Integration tests for CI workflow generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_ci_workflow_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CI workflow file is generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    ci_yml = result.project_dir / '.github' / 'workflows' / 'ci.yml'
    assert ci_yml.exists()


def test_ci_workflow_contains_required_jobs(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CI workflow contains lint-and-typecheck and test jobs."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / '.github' / 'workflows' / 'ci.yml').read_text()
    assert 'lint-and-typecheck:' in content
    assert 'test:' in content


def test_ci_workflow_contains_required_tools(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CI workflow sets up required tools."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / '.github' / 'workflows' / 'ci.yml').read_text()
    assert 'actions/checkout@v4' in content
    assert 'extractions/setup-just@v4' in content
    assert 'astral-sh/setup-uv@v5' in content


def test_ci_workflow_contains_commands(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CI workflow runs expected commands."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / '.github' / 'workflows' / 'ci.yml').read_text()
    assert 'just install-dev' in content
    assert 'just check' in content
    assert 'just test' in content


def test_ci_workflow_python_matrix_default(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test CI workflow Python version matrix includes correct versions."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / '.github' / 'workflows' / 'ci.yml').read_text()
    assert '"3.12"' in content
    assert '"3.13"' in content
    assert '"3.14"' in content


def test_ci_workflow_python_matrix_custom(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test CI workflow Python version matrix with custom specifier."""
    answers = {**base_answers, 'python_version': '>=3.13'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / '.github' / 'workflows' / 'ci.yml').read_text()
    assert '"3.13"' in content
    assert '"3.14"' in content
    assert '"3.12"' not in content
