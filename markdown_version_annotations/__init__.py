"""Version-annotations plugin for Markdown."""
import re
from typing import List

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class VersionAnnotationsPreprocessor(Preprocessor):
    """Turn special notes into standardized Markdown admonitions."""

    def __init__(self, md, config):
        super().__init__(md)
        self.admonition_tag = config["admonition_tag"]
        self.version_added_admonition = config["version_added_admonition"]
        self.version_added_title = config["version_added_title"]
        self.version_changed_admonition = config["version_changed_admonition"]
        self.version_changed_title = config["version_changed_title"]
        self.version_removed_admonition = config["version_removed_admonition"]
        self.version_removed_title = config["version_removed_title"]

    # Match and remove any leading whitespace so that we can handle nested annotations
    LEADING_WHITESPACE = re.compile(r"^(\s*)(.*)$")
    # Match `+++ 1.0.0` or `+++ 1.0.0 "info string"`
    VERSION_ADDED_ANNOTATION = re.compile(r'^\+\+\+\s+([0-9.]+)\s*(?:"(.*)")?$')
    # Match `+/- 1.0.0` or `+/- 1.0.0 "info string"`
    VERSION_CHANGED_ANNOTATION = re.compile(r'^\+/-\s+([0-9.]+)\s*(?:"(.*)")?$')
    # Match `--- 1.0.0` or `--- 1.0.0 "info string"`
    VERSION_REMOVED_ANNOTATION = re.compile(r'^---\s+([0-9.]+)\s*(?:"(.*)")?$')
    # Match title string ending in ` — "` as a side effect of the above regexps in cases with no "info string"
    NO_TITLE = re.compile(r'\s+—\s+"$')

    def run(self, lines: List[str]) -> List[str]:
        """Preprocess the provided Markdown source text.

        Looks for any lines that match any of the ANNOTATION regexes, for example:

        - `+++ 1.1.0`
        - `+/- 0.1`
        - `    --- 2.0 "Support for older PostgreSQL versions"`

        and converts them to the standard `!!!` admonitions used elsewhere.

        Args:
            lines: List of strings corresponding to the lines of the input file.

        Returns:
            List of processed strings.
        """
        new_lines = []
        for line in lines:
            leading_whitespace, line = self.LEADING_WHITESPACE.match(line).groups()
            line = self.VERSION_ADDED_ANNOTATION.sub(
                rf'{self.admonition_tag} {self.version_added_admonition} "{self.version_added_title} — \2"', line
            )
            line = self.VERSION_CHANGED_ANNOTATION.sub(
                rf'{self.admonition_tag} {self.version_changed_admonition} "{self.version_changed_title} — \2"', line
            )
            line = self.VERSION_REMOVED_ANNOTATION.sub(
                rf'{self.admonition_tag} {self.version_removed_admonition} "{self.version_removed_title} — \2"', line
            )
            line = self.NO_TITLE.sub('"', line)
            if leading_whitespace:
                line = leading_whitespace + line
            new_lines.append(line)

        return new_lines


class VersionAnnotations(Extension):
    """Extension to the Markdown library providing the VersionAnnotationsPreprocessor pre-processor class."""

    def __init__(self, **kwargs):
        self.config = {
            "admonition_tag": ["!!!", "Admonition 'tag' to use for all version annotations"],
            "version_added_admonition": ["version-added", "Admonition type string to use for +++ annotations"],
            "version_added_title": [r"Added in version \1", "Regex substitution for the title of +++ annotations"],
            "version_changed_admonition": ["version-changed", "Admonition type string to use for +/- annotations"],
            "version_changed_title": [r"Changed in version \1", "Regex substitution for the title of +/- annotations"],
            "version_removed_admonition": ["version-removed", "Admonition type string to use for --- annotations"],
            "version_removed_title": [r"Removed in version \1", "Regex substitution for the title of --- annotations"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """Register the VersionAnnotationsPreprocessor as a Markdown pre-processor class."""
        md.preprocessors.register(VersionAnnotationsPreprocessor(md, self.getConfigs()), "version-annotations", 100)


def makeExtension(**kwargs):  # pylint: disable=invalid-name
    """Function auto-called by Markdown library to discover/register extensions."""
    return VersionAnnotations(**kwargs)
