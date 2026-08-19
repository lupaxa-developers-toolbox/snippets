"""Lint snippets marked runnable: true."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from snippets_mkdocs.scan import scan_snippets

TOOLS: dict[str, list[str]] = {
    "shell": ["shellcheck"],
    "python": ["ruff", "check"],
    "ruby": ["ruby", "-c"],
}


def lint_runnable(root: Path) -> int:
    """Return 0 on success, 2 when a wired linter is missing or fails."""
    snippets = scan_snippets(root)
    exit_code = 0
    for item in snippets:
        if not item.runnable:
            continue
        tool = TOOLS.get(item.language)
        if tool is None:
            print(
                f"NOTICE: skipping runnable lint for {item.path} (no linter wired)",
                flush=True,
            )
            continue
        if shutil.which(tool[0]) is None:
            print(
                f"ERROR: {tool[0]} is required to lint runnable {item.language} "
                f"snippet {item.path}",
                file=sys.stderr,
            )
            exit_code = 2
            continue
        result = subprocess.run(
            [*tool, str(item.path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            sys.stderr.write(result.stdout)
            sys.stderr.write(result.stderr)
            exit_code = 2
    return exit_code


def main(argv: list[str] | None = None) -> int:
    """CLI: lint runnable snippets under ./snippets."""
    del argv
    root = Path.cwd() / "snippets"
    return lint_runnable(root)


if __name__ == "__main__":
    raise SystemExit(main())
