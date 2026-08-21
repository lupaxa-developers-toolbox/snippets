from datetime import UTC, datetime
from pathlib import Path

import pytest

from snippets_mkdocs.errors import SnippetError
from snippets_mkdocs.languages import (
    Catalogue,
    Language,
    language_labels,
    language_mark_slug,
    language_profile,
    listed_slugs,
    load_languages,
)
from snippets_mkdocs.models import Snippet


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_load_languages_reads_rows(tmp_path: Path) -> None:
    path = _write(
        tmp_path / "languages.yml",
        "- slug: shell\n  name: Shell\n  summary: POSIX shells.\n"
        "- slug: kotlin\n  name: Kotlin\n  summary: JVM.\n",
    )
    rows = load_languages(path)
    assert [row.slug for row in rows] == ["shell", "kotlin"]
    assert rows[0].name == "Shell"
    assert rows[1].name == "Kotlin"


def test_load_languages_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "missing.yml"
    with pytest.raises(SnippetError, match="missing language catalogue") as exc:
        load_languages(path)
    assert exc.value.path == str(path)


@pytest.mark.parametrize(
    "body, match",
    [
        ("", "must be a non-empty list"),
        ("slug: shell\n", "must be a non-empty list"),
        ("[]\n", "must be a non-empty list"),
        (
            "- slug: shell\n  name: Shell\n  summary: x\n  extra: 1\n",
            "unknown key",
        ),
        ("- slug: Shell\n  name: Shell\n  summary: x\n", "invalid slug"),
        ("- slug: code\n  name: Code\n  summary: x\n", "reserved slug"),
        (
            "- slug: shell\n  name: Shell\n  summary: x\n"
            "- slug: shell\n  name: Other\n  summary: y\n",
            "duplicate slug",
        ),
        ("- slug: shell\n  name: Shell\n  summary: x\n  visible: true\n", "unknown key"),
    ],
)
def test_load_languages_rejects_bad_yaml(tmp_path: Path, body: str, match: str) -> None:
    path = _write(tmp_path / "languages.yml", body)
    with pytest.raises(SnippetError, match=match):
        load_languages(path)


def _snip(language: str) -> Snippet:
    return Snippet(
        language=language,
        slug="x",
        path=Path(f"snippets/{language}/x.txt"),
        title="x",
        card_title="x",
        summary="s",
        tags=("t",),
        added=datetime(2026, 1, 1, tzinfo=UTC),
        submitted_by="Lupraxus",
        runnable=False,
        caveats=None,
        body="1\n",
        extension=".txt",
    )


def _cat(*rows: Language, marks_dir: Path | None = None) -> Catalogue:
    return Catalogue(languages=rows, marks_dir=marks_dir)


SHELL = Language("shell", "Shell", "POSIX shells.")
KOTLIN = Language("kotlin", "Kotlin", "JVM.")


def test_listed_slugs_empty_when_no_snippets() -> None:
    assert listed_slugs(_cat(SHELL, KOTLIN), []) == []


def test_listed_slugs_are_alphabetical_by_display_name() -> None:
    """Languages page order follows A–Z names, not YAML row order."""
    python = Language("python", "Python", "Scripts.")
    rust = Language("rust", "Rust", "Systems.")
    c_lang = Language("c", "C", "Systems.")
    snippets = [_snip("python"), _snip("rust"), _snip("c"), _snip("shell")]
    assert listed_slugs(_cat(python, rust, c_lang, SHELL), snippets) == [
        "c",
        "python",
        "rust",
        "shell",
    ]


def test_listed_slugs_includes_language_when_it_has_snippets() -> None:
    assert listed_slugs(_cat(SHELL, KOTLIN), [_snip("kotlin")]) == ["kotlin"]


def test_listed_slugs_includes_unknown_scanned_language() -> None:
    assert listed_slugs(_cat(SHELL), [_snip("elixir")]) == ["elixir"]


def test_language_profile_unknown_capitalises() -> None:
    assert language_profile(_cat(SHELL), "elixir") == (
        "Elixir",
        "Copy-paste helpers written in Elixir.",
    )


def test_language_mark_slug_unknown_is_code() -> None:
    assert language_mark_slug(_cat(SHELL), "elixir") == "code"


def test_language_mark_slug_yaml_without_file_is_code(tmp_path: Path) -> None:
    marks = tmp_path / "marks"
    marks.mkdir()
    assert language_mark_slug(_cat(SHELL, marks_dir=marks), "shell") == "code"


def test_language_mark_slug_yaml_with_file(tmp_path: Path) -> None:
    marks = tmp_path / "marks"
    marks.mkdir()
    (marks / "shell.png").write_bytes(b"x")
    assert language_mark_slug(_cat(SHELL, marks_dir=marks), "shell") == "shell"


def test_language_labels_include_every_yaml_row() -> None:
    assert language_labels(_cat(SHELL, KOTLIN)) == {"shell": "Shell", "kotlin": "Kotlin"}
