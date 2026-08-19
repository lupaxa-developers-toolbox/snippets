from pathlib import Path

import pytest

from snippets_mkdocs.lint import lint_runnable

RUNNABLE = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [demo]
# added: "2026-01-01T00:00:00+00:00"
# submitted_by: Lupraxus
# runnable: true
# end-snippet

echo hi
"""

FRAGMENT = """# snippet:
# title: T
# card_title: T
# summary: S
# tags: [demo]
# added: "2026-01-01T00:00:00+00:00"
# submitted_by: Lupraxus
# runnable: false
# end-snippet

echo hi
"""


def test_fragment_not_linted(tmp_path: Path) -> None:
    (tmp_path / "shell").mkdir()
    (tmp_path / "shell" / "x.sh").write_text(FRAGMENT, encoding="utf-8")
    assert lint_runnable(tmp_path) == 0


def test_unknown_language_notice(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "javascript").mkdir()
    (tmp_path / "javascript" / "x.js").write_text(
        RUNNABLE.replace("echo hi", "export default 1"),
        encoding="utf-8",
    )
    assert lint_runnable(tmp_path) == 0
    assert "NOTICE" in capsys.readouterr().out


def test_missing_shellcheck_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (tmp_path / "shell").mkdir()
    (tmp_path / "shell" / "x.sh").write_text(RUNNABLE, encoding="utf-8")

    def no_shellcheck(name: str) -> str | None:
        if name == "shellcheck":
            return None
        return "/usr/bin/" + name

    monkeypatch.setattr("snippets_mkdocs.lint.shutil.which", no_shellcheck)
    assert lint_runnable(tmp_path) == 2
    assert "shellcheck" in capsys.readouterr().err
