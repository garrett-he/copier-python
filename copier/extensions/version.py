"""Custom Jinja2 extension providing version filtering utilities."""

from jinja2 import Environment
from jinja2.ext import Extension
from packaging.specifiers import SpecifierSet


def version_list(value: str, versions: list[str]) -> list[str]:
    """Filter a list of version strings by a PEP 440 specifier string."""
    return list(SpecifierSet(value).filter(versions))


class VersionExtension(Extension):
    """Jinja2 extension registering the version_list filter."""

    def __init__(self, environment: Environment) -> None:
        """Register filters on the Jinja2 environment."""
        super().__init__(environment)

        environment.filters['version_list'] = version_list  # pyrefly: ignore[unsupported-operation]
