@_default:
    just --list --unsorted

# Install development dependencies
install-dev:
    uv sync --extra dev
    uv run pre-commit install

# Check the codes
check:
    uv run ruff check copier/extensions tests
    uv run ruff format --check copier/extensions tests
    uv run pyrefly check
    uv run pyproject-fmt --check pyproject.toml
    uv run rumdl check .

# Format the codes
format:
    uv run ruff format copier/extensions tests
    uv run pyproject-fmt pyproject.toml
    uv run rumdl check --fix .

# Run tests
test:
    uv run pytest --template .
