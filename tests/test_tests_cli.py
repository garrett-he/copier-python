"""Integration tests for CLI test file generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_tests_cli_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/test_cli.py is generated when with_cli is true."""
    answers = {**base_answers, 'with_cli': True}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    test_cli = result.project_dir / 'tests' / 'test_cli.py'
    assert test_cli.exists()


def test_tests_cli_not_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/test_cli.py is not generated when with_cli is false."""
    answers = {**base_answers, 'with_cli': False}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    test_cli = result.project_dir / 'tests' / 'test_cli.py'
    assert not test_cli.exists()


def test_tests_cli_contains_import(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/test_cli.py imports the CLI app."""
    answers = {**base_answers, 'with_cli': True}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    package = base_answers['project_package']
    content = (result.project_dir / 'tests' / 'test_cli.py').read_text()
    assert f'from {package}.cli import app' in content


def test_tests_cli_contains_test_function(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tests/test_cli.py contains test function."""
    answers = {**base_answers, 'with_cli': True}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    content = (result.project_dir / 'tests' / 'test_cli.py').read_text()
    assert 'def test_cli_prints_hello_world()' in content
    assert 'Hello, world!' in content
