import os
import subprocess
import sys
from pathlib import Path

import yaml
from mkdocs.config.base import load_config

REPO = Path(__file__).resolve().parents[1]


def test_load_plugin_after_mkdocs_restores_sys_path(tmp_path: Path) -> None:
    """MkDocs puts the hook dir on sys.path only while exec'ing the file."""
    import mkdocs_hooks

    src = str(Path(mkdocs_hooks.__file__).resolve().parent / "src")
    saved_path = sys.path[:]
    saved_modules = {
        name: module
        for name, module in sys.modules.items()
        if name == "snippets_mkdocs" or name.startswith("snippets_mkdocs.")
    }
    try:
        sys.path[:] = [entry for entry in sys.path if entry != src]
        for name in saved_modules:
            del sys.modules[name]

        docs = tmp_path / "mkdocs"
        docs.mkdir()
        (docs / "index.md").write_text("# Home\n", encoding="utf-8")
        data = tmp_path / "data"
        data.mkdir()
        (data / "languages.yml").write_text(
            "- slug: shell\n  name: Shell\n  summary: POSIX.\n",
            encoding="utf-8",
        )
        cfg_path = tmp_path / "mkdocs.yml"
        cfg_path.write_text(
            "site_name: t\ndocs_dir: mkdocs\nnav:\n  - Home: index.md\nplugins: []\n",
            encoding="utf-8",
        )
        config = load_config(str(cfg_path))
        assert mkdocs_hooks.on_config(config) is config
    finally:
        sys.path[:] = saved_path
        sys.modules.update(saved_modules)


def test_bare_mkdocs_build_without_editable_install() -> None:
    """Global pyenv `mkdocs` has no snippets-mkdocs package."""
    mkdocs = Path(sys.base_prefix) / "bin" / "mkdocs"
    if not mkdocs.is_file():
        return
    env = os.environ.copy()
    env["PYTHONPATH"] = ""
    result = subprocess.run(
        [str(mkdocs), "build", "--strict"],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stderr + result.stdout


def test_mkdocs_loads_catalogue_via_hook_not_plugin_entry() -> None:
    """Bare `mkdocs` (pyenv/global) has no snippets entry point."""

    class _Loader(yaml.SafeLoader):
        pass

    def _ignore_unknown(_loader: yaml.Loader, _tag: str, _node: yaml.Node) -> None:
        return None

    _Loader.add_multi_constructor("tag:yaml.org,2002:python/name:", _ignore_unknown)
    config = yaml.load((REPO / "mkdocs.yml").read_text(encoding="utf-8"), Loader=_Loader)
    plugins = config.get("plugins") or []
    names = []
    for item in plugins:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict):
            names.extend(item.keys())
    assert "snippets" not in names
    assert "mkdocs_hooks.py" in (config.get("hooks") or [])
    assert {
        "data",
        "mkdocs_hooks.py",
        "overrides",
        "snippets",
        "src/snippets_mkdocs",
    } <= set(config.get("watch") or [])
