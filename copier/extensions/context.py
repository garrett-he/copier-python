"""Custom context hook for enriching Copier template context."""

import subprocess
from datetime import date

from copier_template_extensions import ContextHook


class ContextUpdater(ContextHook):
    """Inject dynamic values into the Copier rendering context."""

    def hook(self, context: dict[str, object]) -> None:
        """Populate context with git and date derived values."""
        self.set_git_values(context)
        self.set_date_values(context)

    def set_git_values(self, context: dict[str, object]) -> None:
        """Add git user name and email to context."""
        for key, cmd in (
            ('git_user_name', ['git', 'config', 'user.name']),
            ('git_user_email', ['git', 'config', 'user.email']),
        ):
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )
            value = result.stdout.strip() if result.returncode == 0 else ''
            context[key] = value

    def set_date_values(self, context: dict[str, object]) -> None:
        """Add current year, month and day to context."""
        today = date.today()
        context['current_year'] = today.year
        context['current_month'] = today.month
        context['current_day'] = today.day
