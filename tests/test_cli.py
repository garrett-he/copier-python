"""Integration tests for CLI module generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_cli_module_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CLI module is generated when with_cli is true."""
    answers = {**base_answers, 'with_cli': True}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    package = base_answers['project_package']
    cli_py = result.project_dir / 'src' / package / 'cli.py'
    assert cli_py.exists()


def test_cli_module_not_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CLI module is not generated when with_cli is false."""
    answers = {**base_answers, 'with_cli': False}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers['project_package']
    cli_py = result.project_dir / 'src' / package / 'cli.py'
    assert not cli_py.exists()


def test_cli_module_contains_app(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CLI module contains typer app."""
    answers = {**base_answers, 'with_cli': True}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers['project_package']
    content = (result.project_dir / 'src' / package / 'cli.py').read_text()
    assert 'import typer' in content
    assert 'app = typer.Typer()' in content


def test_cli_module_contains_main_command(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that CLI module contains main command."""
    answers = {**base_answers, 'with_cli': True}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers['project_package']
    content = (result.project_dir / 'src' / package / 'cli.py').read_text()
    assert '@app.command()' in content
    assert 'def main()' in content
    assert 'Hello, world!' in content
