"""Load the language catalogue from data/languages.yml."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from snippets_mkdocs.errors import SnippetError
from snippets_mkdocs.models import Snippet

_SLUG = re.compile(r"^[a-z][a-z0-9]*$")
_KEYS = frozenset({"slug", "name", "summary"})
_RESERVED = frozenset({"code"})


@dataclass(frozen=True)
class Language:
    """One catalogue language row."""

    slug: str
    name: str
    summary: str


@dataclass(frozen=True)
class Catalogue:
    """Loaded catalogue plus optional mark directory for existence checks."""

    languages: tuple[Language, ...]
    marks_dir: Path | None = None


def load_languages(path: Path) -> tuple[Language, ...]:
    """Parse and validate ``data/languages.yml``."""
    if not path.is_file():
        raise SnippetError("missing language catalogue", path=str(path))
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list) or not raw:
        raise SnippetError("language catalogue must be a non-empty list", path=str(path))
    rows: list[Language] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise SnippetError(
                f"language catalogue entry {index} must be a mapping",
                path=str(path),
            )
        unknown = set(item) - _KEYS
        if unknown:
            raise SnippetError(
                f"unknown key {sorted(unknown)[0]}",
                path=str(path),
            )
        slug = item.get("slug")
        name = item.get("name")
        summary = item.get("summary")
        if not isinstance(slug, str) or not _SLUG.match(slug):
            raise SnippetError("invalid slug", path=str(path), field="slug")
        if slug in _RESERVED:
            raise SnippetError("reserved slug", path=str(path), field="slug")
        if slug in seen:
            raise SnippetError("duplicate slug", path=str(path), field="slug")
        if not isinstance(name, str) or not name.strip():
            raise SnippetError("invalid name", path=str(path), field="name")
        if not isinstance(summary, str) or not summary.strip():
            raise SnippetError("invalid summary", path=str(path), field="summary")
        seen.add(slug)
        rows.append(Language(slug=slug, name=name, summary=summary))
    return tuple(rows)


def language_profile(catalogue: Catalogue, slug: str) -> tuple[str, str]:
    """Display name and blurb for a language slug."""
    for row in catalogue.languages:
        if row.slug == slug:
            return (row.name, row.summary)
    name = slug.capitalize()
    return (name, f"Copy-paste helpers written in {name}.")


def listed_slugs(catalogue: Catalogue, snippets: list[Snippet]) -> list[str]:
    """Language slugs that currently have at least one snippet."""
    listed = {item.language for item in snippets}
    return sorted(listed, key=lambda slug: language_profile(catalogue, slug)[0].casefold())


def language_mark_slug(catalogue: Catalogue, slug: str) -> str:
    """PNG stem for a language, or ``code`` when unknown or the file is missing."""
    known = {row.slug for row in catalogue.languages}
    if slug not in known:
        return "code"
    if catalogue.marks_dir is None:
        return slug
    if (catalogue.marks_dir / f"{slug}.png").is_file():
        return slug
    return "code"


def language_labels(catalogue: Catalogue) -> dict[str, str]:
    """Slug to display name for every YAML row."""
    return {row.slug: row.name for row in catalogue.languages}
