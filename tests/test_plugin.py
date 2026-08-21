from pathlib import Path

import pytest
from mkdocs.config.base import load_config
from mkdocs.structure.files import get_files

from snippets_mkdocs.errors import SnippetError
from snippets_mkdocs.plugin import SnippetsPlugin

_MINIMAL_LANGUAGES = """\
- slug: shell
  name: Shell
  summary: POSIX shells.
"""


def _write_languages(tmp_path: Path, body: str = _MINIMAL_LANGUAGES) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "languages.yml").write_text(body, encoding="utf-8")


HEADER = """# snippet:
# title: Retry a command
# card_title: Retry a command
# summary: Backoff retry.
# tags: [process, retry]
# added: "2026-08-18T18:03:18+01:00"
# submitted_by: Lupraxus
# end-snippet

retry() { :; }
"""


def test_plugin_injects_files_and_nav(tmp_path: Path) -> None:
    _write_languages(tmp_path)
    docs = tmp_path / "mkdocs"
    docs.mkdir()
    (docs / "index.md").write_text("# Home\n", encoding="utf-8")
    snippets = tmp_path / "snippets" / "shell"
    snippets.mkdir(parents=True)
    (snippets / "retry.sh").write_text(HEADER, encoding="utf-8")
    cfg_path = tmp_path / "mkdocs.yml"
    cfg_path.write_text(
        "site_name: t\ndocs_dir: mkdocs\nnav:\n  - Home: index.md\nplugins: []\n",
        encoding="utf-8",
    )
    config = load_config(str(cfg_path))
    plugin = SnippetsPlugin()
    config = plugin.on_config(config)
    config.plugins._current_plugin = "snippets"
    files = plugin.on_files(get_files(config), config)
    uris = {item.src_uri for item in files}
    assert "shell/retry.md" in uris
    assert "shell/index.md" not in uris
    assert "languages/index.md" not in uris
    assert "languages.md" in uris
    assert "snippets.md" in uris
    assert "tags/retry.md" not in uris
    assert "tags/index.md" not in uris
    assert "index.md" in uris
    home = files.get_file_from_path("index.md")
    assert home is not None
    assert "# Home" not in home.content_string
    listing = files.get_file_from_path("snippets.md")
    assert listing is not None
    assert "Retry a command" in listing.content_string
    nav_titles = [
        list(item.keys())[0] if isinstance(item, dict) else item for item in config["nav"]
    ]
    assert "Snippets" in nav_titles
    assert "Languages" in nav_titles
    assert "Tags" not in nav_titles


def test_plugin_missing_languages_yml_fails(tmp_path: Path) -> None:
    docs = tmp_path / "mkdocs"
    docs.mkdir()
    (docs / "index.md").write_text("# Home\n", encoding="utf-8")
    cfg_path = tmp_path / "mkdocs.yml"
    cfg_path.write_text(
        "site_name: t\ndocs_dir: mkdocs\nnav:\n  - Home: index.md\nplugins: []\n",
        encoding="utf-8",
    )
    config = load_config(str(cfg_path))
    plugin = SnippetsPlugin()
    with pytest.raises(SnippetError, match="missing language catalogue"):
        plugin.on_config(config)


def test_plugin_missing_snippets_is_empty_catalogue(tmp_path: Path) -> None:
    _write_languages(tmp_path)
    docs = tmp_path / "mkdocs"
    docs.mkdir()
    (docs / "index.md").write_text("# Home\n", encoding="utf-8")
    cfg_path = tmp_path / "mkdocs.yml"
    cfg_path.write_text(
        "site_name: t\ndocs_dir: mkdocs\nnav:\n  - Home: index.md\nplugins: []\n",
        encoding="utf-8",
    )
    config = load_config(str(cfg_path))
    plugin = SnippetsPlugin()
    config = plugin.on_config(config)
    config.plugins._current_plugin = "snippets"
    files = plugin.on_files(get_files(config), config)
    uris = {item.src_uri for item in files}
    assert "tags/index.md" not in uris
    assert "languages/index.md" not in uris
    assert "languages.md" in uris
    assert "snippets.md" in uris
    assert "index.md" in uris
    home = files.get_file_from_path("index.md")
    assert home is not None
    assert "No snippets yet." in home.content_string
    nav_titles = [
        list(item.keys())[0] if isinstance(item, dict) else item for item in config["nav"]
    ]
    assert "Snippets" in nav_titles
    assert "Languages" in nav_titles
    assert "Tags" not in nav_titles
