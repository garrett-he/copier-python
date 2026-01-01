default:
    just --list

install-dev:
    uv sync --extra dev
    uv run pre-commit install

lint:
    uv run ruff check copier/extensions tests
    uv run ruff format --check copier/extensions tests

typecheck:
    uv run mypy copier/extensions tests

format:
    uv run ruff format copier/extensions tests

test:
    uv run pytest
