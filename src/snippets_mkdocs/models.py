"""Dataclasses for parsed snippets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class HeaderMeta:
    """Metadata from a snippet: / end-snippet fence."""

    title: str
    card_title: str
    summary: str
    tags: tuple[str, ...]
    added: datetime
    submitted_by: str
    runnable: bool
    caveats: str | None


@dataclass(frozen=True)
class Snippet:
    """A catalogue entry loaded from snippets/<language>/<file>."""

    language: str
    slug: str
    path: Path
    title: str
    card_title: str
    summary: str
    tags: tuple[str, ...]
    added: datetime
    submitted_by: str
    runnable: bool
    caveats: str | None
    body: str
    extension: str
