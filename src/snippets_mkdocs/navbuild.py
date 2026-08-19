"""Build extra MkDocs nav entries for the Snippets page."""

from __future__ import annotations

from snippets_mkdocs.models import Snippet


def extra_nav(_snippets: list[Snippet]) -> list[dict[str, object]]:
    """Top-level Snippets (catalogue) and Languages. No per-snippet children."""
    return [{"Snippets": "snippets.md"}, {"Languages": "languages.md"}]


def snippet_language_prefixes(snippets: list[Snippet]) -> list[str]:
    """Language folders used so the header Snippets tab stays active."""
    return sorted({item.language for item in snippets})
