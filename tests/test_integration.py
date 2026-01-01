"""Integration tests for the copier-python template."""

from typing import Any


def _answers_with(answers: dict[str, object], **overrides: object) -> dict[str, object]:
    """Return a copy of copier answers with unsupported fields removed and overrides applied."""
    merged = dict(answers)
    merged.pop('with_tox', None)
    merged.update(overrides)
    return merged


def test_generate_default(copie: Any, copier_answers: dict[str, object]) -> None:
    """The template generates successfully with valid answers."""
    result = copie.copy(extra_answers=_answers_with(copier_answers))
    assert result.exit_code == 0
    assert result.project_dir.joinpath('pyproject.toml').exists()


def test_generated_project_structure(copie: Any, copier_answers: dict[str, object]) -> None:
    """The generated project contains the expected files and directories."""
    result = copie.copy(extra_answers=_answers_with(copier_answers))
    assert result.exit_code == 0

    project_dir = result.project_dir
    package = str(copier_answers['project_package'])

    assert project_dir.joinpath('pyproject.toml').is_file()
    assert project_dir.joinpath('README.md').is_file()
    assert project_dir.joinpath('LICENSE').is_file()
    assert project_dir.joinpath('justfile').is_file()
    assert project_dir.joinpath('.pre-commit-config.yaml').is_file()
    assert project_dir.joinpath(f'src/{package}/__init__.py').is_file()
    assert project_dir.joinpath(f'src/{package}/py.typed').is_file()
    assert project_dir.joinpath('tests/__init__.py').is_file()
    assert project_dir.joinpath('tests/test_version.py').is_file()
    assert project_dir.joinpath('.github/workflows/ci.yml').is_file()


def test_generated_pyproject_toml(copie: Any, copier_answers: dict[str, object]) -> None:
    """pyproject.toml is rendered with the provided answers."""
    result = copie.copy(extra_answers=_answers_with(copier_answers))
    assert result.exit_code == 0

    pyproject = result.project_dir.joinpath('pyproject.toml').read_text()
    assert f'name = "{copier_answers["project_name"]}"' in pyproject
    assert f'version = "{copier_answers["project_version"]}"' in pyproject
    assert f'description = "{copier_answers["project_description"]}"' in pyproject
    assert f'requires-python = "{copier_answers["python_version"]}"' in pyproject
    assert f'license = {{ text = "{copier_answers["copyright_license"]}" }}' in pyproject
    assert str(copier_answers['copyright_holder_name']) in pyproject
    assert str(copier_answers['copyright_holder_email']) in pyproject
    assert f'https://github.com/{copier_answers["vcs_github_path"]}' in pyproject


def test_license_files(copie: Any, copier_answers: dict[str, object], licenses: dict[str, dict[str, object]]) -> None:
    """Each license choice produces the correct LICENSE file and content."""
    for license_name, spec in licenses.items():
        result = copie.copy(extra_answers=_answers_with(copier_answers, copyright_license=license_name))
        assert result.exit_code == 0

        filename = 'UNLICENSE' if license_name == 'Unlicense' else 'LICENSE'
        license_path = result.project_dir.joinpath(filename)
        assert license_path.is_file(), f'{license_name}: expected {filename}'

        content = license_path.read_text()
        assert spec['stub'] in content, f'{license_name}: expected stub "{spec["stub"]}"'

        readme = result.project_dir.joinpath('README.md').read_text()
        if license_name == 'Unlicense':
            assert 'public domain' in readme
        else:
            assert 'see [LICENSE](./LICENSE)' in readme
            if spec['with_holder']:
                assert str(copier_answers['copyright_holder_name']) in readme


def test_ci_python_matrix(copie: Any, copier_answers: dict[str, object]) -> None:
    """The CI workflow matrix includes only Python versions matching the specifier."""
    result = copie.copy(extra_answers=_answers_with(copier_answers, python_version='>=3.13'))
    assert result.exit_code == 0

    ci_yml = result.project_dir.joinpath('.github/workflows/ci.yml').read_text()
    assert '"3.13"' in ci_yml
    assert '"3.14"' in ci_yml
    assert '"3.12"' not in ci_yml
