"""mkdocs-version-annotations plugin for MkDocs."""
import re

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class MkDocsVersionAnnotationsPlugin(BasePlugin):
    """MkDocs plugin entry point for mkdocs-version-annotations."""

    config_scheme = (
        ("version_added_admonition", config_options.Type(str, default="version-added")),
        ("version_added_title", config_options.Type(str, default=r"Added in version \1")),
        ("version_changed_admonition", config_options.Type(str, default="version-changed")),
        ("version_changed_title", config_options.Type(str, default=r"Changed in version \1")),
        ("version_removed_admonition", config_options.Type(str, default="version-removed")),
        ("version_removed_title", config_options.Type(str, default=r"Removed in version \1")),
    )

    VERSION_ADDED_ANNOTATION = re.compile(r"^\+\+\+\s+([0-9.]+)", flags=re.MULTILINE)
    VERSION_CHANGED_ANNOTATION = re.compile(r"^\+/-\s+([0-9.]+)", flags=re.MULTILINE)
    VERSION_REMOVED_ANNOTATION = re.compile(r"^---\s+([0-9.]+)", flags=re.MULTILINE)

    def on_page_markdown(self, markdown, **kwargs):  # pylint: disable=unused-argument
        """Transform the raw Markdown of any given documentation page."""
        markdown = self.VERSION_ADDED_ANNOTATION.sub(
            f"!!! {self.config['version_added_admonition']} \"{self.config['version_added_title']}\"", markdown
        )
        markdown = self.VERSION_CHANGED_ANNOTATION.sub(
            f"!!! {self.config['version_changed_admonition']} \"{self.config['version_changed_title']}\"", markdown
        )
        markdown = self.VERSION_REMOVED_ANNOTATION.sub(
            f"!!! {self.config['version_removed_admonition']} \"{self.config['version_removed_title']}\"", markdown
        )
        return markdown
