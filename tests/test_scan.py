from pathlib import Path

import pytest

from snippets_mkdocs.errors import SnippetError
from snippets_mkdocs.scan import scan_snippets

HEADER = """# snippet:
# title: Retry a command
# card_title: Retry a command
# summary: Backoff retry.
# tags: [process, retry]
# added: "2026-08-18T18:03:18+01:00"
# submitted_by: Lupraxus
# end-snippet

body
"""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_scan_one_level_and_skip_readme(tmp_path: Path) -> None:
    _write(tmp_path / "shell" / "retry.sh", HEADER)
    _write(tmp_path / "shell" / "README.md", "ignore")
    _write(tmp_path / "shell" / ".gitkeep", "")
    snippets = scan_snippets(tmp_path)
    assert len(snippets) == 1
    item = snippets[0]
    assert item.language == "shell"
    assert item.slug == "retry"
    assert item.extension == ".sh"
    assert item.body == "body\n"


def test_file_in_root_fails(tmp_path: Path) -> None:
    _write(tmp_path / "retry.sh", HEADER)
    with pytest.raises(SnippetError, match="snippets/<language>/<file>"):
        scan_snippets(tmp_path)


def test_nested_path_fails(tmp_path: Path) -> None:
    _write(tmp_path / "shell" / "net" / "retry.sh", HEADER)
    with pytest.raises(SnippetError, match="snippets/<language>/<file>"):
        scan_snippets(tmp_path)


def test_reserved_language_tags_fails(tmp_path: Path) -> None:
    _write(tmp_path / "tags" / "retry.sh", HEADER)
    with pytest.raises(SnippetError, match="reserved"):
        scan_snippets(tmp_path)


def test_duplicate_slug_fails(tmp_path: Path) -> None:
    _write(tmp_path / "shell" / "retry.sh", HEADER)
    _write(tmp_path / "shell" / "retry.bash", HEADER)
    with pytest.raises(SnippetError, match="duplicate"):
        scan_snippets(tmp_path)


def test_missing_root_fails(tmp_path: Path) -> None:
    with pytest.raises(SnippetError, match="missing"):
        scan_snippets(tmp_path / "snippets")
