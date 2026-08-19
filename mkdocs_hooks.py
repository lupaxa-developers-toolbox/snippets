"""Load the snippets catalogue without an installed MkDocs plugin entry point."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files

_SRC = Path(__file__).resolve().parent / "src"


def _ensure_src_on_path() -> None:
    """MkDocs restores sys.path after loading this file; re-add src/."""
    src = str(_SRC)
    if src not in sys.path:
        sys.path.insert(0, src)


_ensure_src_on_path()

_PLUGIN_MODULES = (
    "snippets_mkdocs.errors",
    "snippets_mkdocs.models",
    "snippets_mkdocs.header",
    "snippets_mkdocs.scan",
    "snippets_mkdocs.languages",
    "snippets_mkdocs.render",
    "snippets_mkdocs.navbuild",
    "snippets_mkdocs.plugin",
)

_plugin = None


def _load_plugin():
    """Import or reload the in-repo plugin so `mkdocs serve` picks up edits."""
    _ensure_src_on_path()
    for name in _PLUGIN_MODULES:
        module = importlib.import_module(name)
        importlib.reload(module)
    return sys.modules["snippets_mkdocs.plugin"].SnippetsPlugin()


def on_config(config: MkDocsConfig) -> MkDocsConfig:
    """Forward to the in-repo catalogue plugin."""
    global _plugin
    _plugin = _load_plugin()
    return _plugin.on_config(config)


def on_files(files: Files, config: MkDocsConfig) -> Files:
    """Forward to the in-repo catalogue plugin."""
    if _plugin is None:
        raise RuntimeError("on_config must run before on_files")
    return _plugin.on_files(files, config)
