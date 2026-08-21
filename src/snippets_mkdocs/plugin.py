"""MkDocs plugin: generate catalogue pages from snippets/."""

from __future__ import annotations

from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files

from snippets_mkdocs.languages import Catalogue, load_languages
from snippets_mkdocs.models import Snippet
from snippets_mkdocs.navbuild import extra_nav, snippet_language_prefixes
from snippets_mkdocs.render import (
    render_catalogue,
    render_home,
    render_languages_index,
    render_snippet_page,
)
from snippets_mkdocs.scan import scan_snippets


class SnippetsPlugin(BasePlugin):  # type: ignore[type-arg,no-untyped-call]
    """Inject virtual snippet and listing pages."""

    def __init__(self) -> None:
        super().__init__()
        self._snippets: list[Snippet] = []
        self._catalogue: Catalogue | None = None

    def _repo(self, config: MkDocsConfig) -> Path:
        return Path(config.config_file_path).resolve().parent

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        repo = self._repo(config)
        self._catalogue = Catalogue(
            languages=load_languages(repo / "data" / "languages.yml"),
            marks_dir=repo / "mkdocs" / "assets" / "images" / "languages",
        )
        root = repo / "snippets"
        self._snippets = scan_snippets(root) if root.is_dir() else []
        extra = extra_nav(self._snippets)
        if extra:
            nav = list(config["nav"])
            nav.extend(extra)
            config["nav"] = nav
        config.extra["snippet_language_prefixes"] = snippet_language_prefixes(self._snippets)
        return config

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        catalogue = self._catalogue
        if catalogue is None:
            raise RuntimeError("on_config must run before on_files")
        generated: list[tuple[str, str]] = [
            (
                f"{item.language}/{item.slug}.md",
                render_snippet_page(item, catalogue),
            )
            for item in self._snippets
        ]
        generated.append(("index.md", render_home(self._snippets, catalogue)))
        generated.append(("snippets.md", render_catalogue(self._snippets, catalogue)))
        generated.append(("languages.md", render_languages_index(self._snippets, catalogue)))
        kept = [item for item in files if item.src_uri != "index.md"]
        files = Files(kept)
        for src_uri, content in generated:
            files.append(File.generated(config, src_uri, content=content))
        return files
