"""Custom context hook for enriching Copier template context."""

from __future__ import annotations

import os
from configparser import ConfigParser
from pathlib import Path
from typing import TypedDict, cast, override

from copier_template_extensions import ContextHook


class CopierContext(TypedDict, total=False):
    """Typed context dictionary injected by ContextUpdater."""

    git_user_name: str
    git_user_email: str


def _get_git_user_info() -> tuple[str, str]:
    """Read git user.name and user.email from gitconfig files.

    Returns:
        Tuple of (name, email), empty strings if not configured.
    """
    parser = ConfigParser()
    parser.read(
        [
            Path.home() / '.gitconfig',
            Path.home() / '.config' / 'git' / 'config',
        ]
    )
    name = os.environ.get('GIT_AUTHOR_NAME') or parser.get('user', 'name', fallback='')
    email = os.environ.get('GIT_AUTHOR_EMAIL') or parser.get('user', 'email', fallback='')
    return name, email


class ContextUpdater(ContextHook):
    """Inject dynamic values into the Copier rendering context."""

    @override
    def hook(self, context: dict[str, object]) -> None:
        """Populate context with git derived values."""
        ctx = cast('CopierContext', context)
        ctx['git_user_name'], ctx['git_user_email'] = _get_git_user_info()
