"""Errors for snippet parsing and scanning."""

from __future__ import annotations


class SnippetError(Exception):
    """A snippet header or tree problem, with optional path and field."""

    def __init__(
        self,
        message: str,
        path: str | None = None,
        field: str | None = None,
    ) -> None:
        self.path = path
        self.field = field
        parts = [message]
        if path:
            parts.append(f"path={path}")
        if field:
            parts.append(f"field={field}")
        super().__init__(" ".join(parts))
