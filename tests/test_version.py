"""Smoke test that the package version matches the installed distribution."""

from importlib.metadata import version

from snippets_mkdocs import __version__


def test_version() -> None:
    assert __version__ == version("snippets-mkdocs")
