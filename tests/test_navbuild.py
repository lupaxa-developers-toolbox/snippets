from datetime import UTC, datetime
from pathlib import Path

from snippets_mkdocs.models import Snippet
from snippets_mkdocs.navbuild import extra_nav, snippet_language_prefixes


def _snip(language: str, slug: str) -> Snippet:
    return Snippet(
        language=language,
        slug=slug,
        path=Path(f"{language}/{slug}.sh"),
        title=slug,
        card_title=slug,
        summary="s",
        tags=("retry",),
        added=datetime(2026, 1, 1, tzinfo=UTC),
        submitted_by="Lupraxus",
        runnable=False,
        caveats=None,
        body="x\n",
        extension=".sh",
    )


def test_extra_nav_empty() -> None:
    assert extra_nav([]) == [
        {"Snippets": "snippets.md"},
        {"Languages": "languages.md"},
    ]


def test_extra_nav_snippets_then_languages() -> None:
    nav = extra_nav([_snip("shell", "retry"), _snip("python", "retry")])
    assert nav == [
        {"Snippets": "snippets.md"},
        {"Languages": "languages.md"},
    ]


def test_snippet_language_prefixes_are_unique_and_sorted() -> None:
    assert snippet_language_prefixes(
        [_snip("shell", "retry"), _snip("python", "retry"), _snip("shell", "pause")]
    ) == ["python", "shell"]
