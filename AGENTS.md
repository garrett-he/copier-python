# AGENTS.md

## Project Overview

This is a Copier template for creating new projects. It provides a complete project scaffold with tests, CI, linting,
and documentation.

## Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: uv
- **Task Runner**: just
- **Linter/Formatter**: ruff (line-length: 120, single quotes, LF line endings)
- **Type Checker**: pyrefly (strict preset)
- **Testing**: pytest with pytest-copie
- **Markdown Linter**: rumdl
-

## Development Commands

```bash
# Install dependencies
just install-dev

# Run linters and type checkers
just check

# Format code
just format

# Run tests
just test
```

## Project Structure

- `copier/` - Copier template configuration and extensions for template
- `template/` - Files that will be copied to generated projects
- `tests/` - Tests to verify template generation works correctly
- `copier.yml` - Main Copier configuration

## Code Style

- **Indentation**: 4 spaces
- **Quotes**: Single quotes
- **Line Endings**: LF
- **Max Line Length**: 120 characters
- **Docstrings**: Google style
- **Imports**: Sorted by ruff (isort compatible)
-

## Testing

Tests use `pytest-copie` to test project generation.

Key test patterns:

- `base_answers` fixture provides random test data via `chance` library
- Tests verify file existence, content, and template variable substitution

## Commit Convention

Use Conventional Commits format:

- Prefixes: `feat | fix | ci | refactor | chore | docs | test`
- English language
- Max 70 characters per line in body

## Important Notes

- Always run `just test` before committing
- Template files use Jinja2 syntax with `{% raw %}` blocks for literal curly braces
- License templates are conditionally generated based on `copyright_license` variable
