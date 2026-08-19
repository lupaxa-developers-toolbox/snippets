"""Parse fenced snippet headers from source comments."""

from __future__ import annotations

import re
from datetime import UTC, date, datetime, time
from typing import Any

import yaml

from snippets_mkdocs.errors import SnippetError
from snippets_mkdocs.models import HeaderMeta

_TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_GITHUB_USER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
CARD_TITLE_MAX = 28
_PREFIXES = ("# ", "// ", "-- ", "#", "//", "--")
_START = "snippet:"
_END = "end-snippet"


def _split_prefix(line: str) -> tuple[str, str] | None:
    raw = line.rstrip("\n")
    for prefix in _PREFIXES:
        if raw.startswith(prefix):
            return prefix, raw[len(prefix) :]
    return None


def _prefix_family(prefix: str) -> str:
    """Comment marker without the optional trailing space (`#`, `//`, `--`)."""
    return prefix.rstrip()


def parse_header(text: str, *, path: str | None = None) -> tuple[HeaderMeta, str]:
    """Return metadata and the body after ``end-snippet``.

    Raises:
        SnippetError: fence, YAML, or field validation failed.
    """
    lines = text.splitlines(keepends=True)
    start = None
    prefix_used: str | None = None
    for index, line in enumerate(lines):
        split = _split_prefix(line)
        if split is None:
            continue
        prefix, rest = split
        if rest.strip() == _START:
            start = index
            prefix_used = prefix
            break
    if start is None or prefix_used is None:
        raise SnippetError("missing snippet: / end-snippet fence", path=path)

    yaml_lines: list[str] = []
    end = None
    for index in range(start + 1, len(lines)):
        split = _split_prefix(lines[index])
        if split is None:
            raise SnippetError("comment style cannot be stripped to a fence", path=path)
        prefix, rest = split
        if _prefix_family(prefix) != _prefix_family(prefix_used):
            raise SnippetError("inconsistent comment prefix in fence", path=path)
        if rest.strip() == _END:
            end = index
            break
        yaml_lines.append(rest + "\n")
    if end is None:
        raise SnippetError("missing snippet: / end-snippet fence", path=path)

    try:
        loaded: Any = yaml.safe_load("".join(yaml_lines)) or {}
    except yaml.YAMLError as exc:
        raise SnippetError(f"invalid YAML in header: {exc}", path=path) from exc
    if not isinstance(loaded, dict):
        raise SnippetError("header YAML must be a mapping", path=path)

    def _require_str(key: str) -> str:
        value = loaded.get(key)
        if not isinstance(value, str) or not value.strip():
            raise SnippetError(f"missing or empty {key}", path=path, field=key)
        return value.strip()

    title = _require_str("title")
    card_title = _require_str("card_title")
    if len(card_title) > CARD_TITLE_MAX:
        raise SnippetError(
            f"card_title must be at most {CARD_TITLE_MAX} characters",
            path=path,
            field="card_title",
        )
    summary = _require_str("summary")
    tags_raw = loaded.get("tags")
    if not isinstance(tags_raw, list) or not tags_raw:
        raise SnippetError("tags must be a non-empty list", path=path, field="tags")
    tags: list[str] = []
    for item in tags_raw:
        if not isinstance(item, str) or not _TAG_RE.match(item):
            raise SnippetError(
                "each tag must match ^[a-z0-9]+(-[a-z0-9]+)*$",
                path=path,
                field="tags",
            )
        tags.append(item)

    added = _parse_added(loaded.get("added"), path=path)
    submitted_by = _parse_submitted_by(loaded.get("submitted_by"), path=path)

    runnable_raw = loaded.get("runnable", False)
    if not isinstance(runnable_raw, bool):
        raise SnippetError("runnable must be a boolean", path=path, field="runnable")

    caveats_raw = loaded.get("caveats")
    caveats: str | None
    if caveats_raw is None:
        caveats = None
    elif isinstance(caveats_raw, str) and caveats_raw.strip():
        caveats = caveats_raw.strip()
    else:
        raise SnippetError("caveats must be a string", path=path, field="caveats")

    body = "".join(lines[end + 1 :])
    if body.startswith("\n"):
        body = body[1:]

    return (
        HeaderMeta(
            title=title,
            card_title=card_title,
            summary=summary,
            tags=tuple(tags),
            added=added,
            submitted_by=submitted_by,
            runnable=runnable_raw,
            caveats=caveats,
        ),
        body,
    )


def _parse_added(raw: Any, *, path: str | None) -> datetime:
    """Require an ISO-8601 date or date-time for ``added``."""
    parsed: datetime | None = None
    if isinstance(raw, datetime):
        parsed = raw
    elif isinstance(raw, date):
        parsed = datetime.combine(raw, time.min)
    elif isinstance(raw, str) and raw.strip():
        try:
            parsed = datetime.fromisoformat(raw.strip())
        except ValueError:
            parsed = None
    if parsed is None:
        raise SnippetError(
            "added must be an ISO-8601 date or date-time",
            path=path,
            field="added",
        )
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _parse_submitted_by(raw: Any, *, path: str | None) -> str:
    """Require a GitHub userid (profile URL is https://github.com/<id>)."""
    if not isinstance(raw, str) or not raw.strip():
        raise SnippetError(
            "missing or empty submitted_by",
            path=path,
            field="submitted_by",
        )
    userid = raw.strip()
    if not _GITHUB_USER_RE.match(userid):
        raise SnippetError(
            "submitted_by must be a GitHub userid",
            path=path,
            field="submitted_by",
        )
    return userid
