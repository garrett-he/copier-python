# Agent Guidance

A [Copier](https://github.com/copier-org/copier) template for scaffolding modern Python
libraries.

## Structure

- `copier/` — Template config, questions, and custom Jinja2 extensions
- `template/` — Template files rendered by Copier (Jinja2 syntax, `.jinja` suffix
  stripped)
- `tests/` — Template tests using `pytest-copie`

## Environment

- Python >= 3.12 (tested on 3.12, 3.13, 3.14)
- [uv](https://docs.astral.sh/uv/) for dependency management
- [just](https://github.com/casey/just) for tasks

## Commands

| Command            | Description                       |
|--------------------|-----------------------------------|
| `just install-dev` | Install deps and pre-commit hooks |
| `just lint`        | Run ruff linter and format check  |
| `just typecheck`   | Run strict mypy                   |
| `just format`      | Auto-format with ruff             |
| `just test`        | Run pytest                        |

## Style

- Line length: 120
- Single quotes, 4 spaces, LF endings
- Google docstrings (`D` rules)
- Ruff rules: `E`, `W`, `F`, `I`, `N`, `UP`, `D`, `B`, `SIM`, `C4`, `TCH`, `RUF`
- Strict mypy

## Notes

- `copier/extensions/context.py` injects `git_user_name`, `git_user_email`, and current
  date into the rendering context.
- `copier/extensions/version.py` adds a `version_list` Jinja2 filter.
- When modifying `template/`, use Jinja2 syntax; file/dir names can also be
  expressions (e.g., `src/{{project_package}}/__init__.py.jinja`).
