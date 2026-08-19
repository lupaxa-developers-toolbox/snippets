"""Walk snippets/<language>/<file> and load catalogue entries."""

from __future__ import annotations

from pathlib import Path

from snippets_mkdocs.errors import SnippetError
from snippets_mkdocs.header import parse_header
from snippets_mkdocs.models import Snippet

SKIP_NAMES = frozenset({"README", "README.md"})
RESERVED_LANGUAGES = frozenset({"tags"})


def scan_snippets(root: Path) -> list[Snippet]:
    """Load every non-skipped snippet under ``root``.

    Raises:
        SnippetError: missing root, bad layout, duplicate slug, or bad header.
    """
    if not root.is_dir():
        raise SnippetError(f"missing snippets directory: {root}", path=str(root))

    found: list[Snippet] = []
    seen: set[tuple[str, str]] = set()

    for child in sorted(root.iterdir()):
        if child.name.startswith("."):
            continue
        if child.is_file():
            raise SnippetError(
                "files must live at snippets/<language>/<file>",
                path=str(child),
            )
        language = child.name.lower()
        if language in RESERVED_LANGUAGES:
            raise SnippetError(
                "language folder name 'tags' is reserved",
                path=str(child),
            )
        for entry in sorted(child.iterdir()):
            if entry.name.startswith(".") or entry.name in SKIP_NAMES:
                continue
            if entry.is_dir():
                raise SnippetError(
                    "files must live at snippets/<language>/<file>",
                    path=str(entry),
                )
            slug = entry.stem
            key = (language, slug)
            if key in seen:
                raise SnippetError(
                    f"duplicate language + slug: {language}/{slug}",
                    path=str(entry),
                )
            seen.add(key)
            text = entry.read_text(encoding="utf-8")
            meta, body = parse_header(text, path=str(entry))
            found.append(
                Snippet(
                    language=language,
                    slug=slug,
                    path=entry,
                    title=meta.title,
                    card_title=meta.card_title,
                    summary=meta.summary,
                    tags=meta.tags,
                    added=meta.added,
                    submitted_by=meta.submitted_by,
                    runnable=meta.runnable,
                    caveats=meta.caveats,
                    body=body,
                    extension=entry.suffix,
                )
            )
    return found
