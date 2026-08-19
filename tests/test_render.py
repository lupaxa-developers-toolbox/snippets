import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

from snippets_mkdocs.languages import Catalogue, Language
from snippets_mkdocs.models import Snippet
from snippets_mkdocs.render import (
    latest_snippets,
    render_catalogue,
    render_home,
    render_language_index,
    render_languages_index,
    render_snippet_page,
    render_tag_page,
    render_tags_index,
)


def _catalogue(*extra: Language) -> Catalogue:
    rows = (
        Language("shell", "Shell", "POSIX and Bourne-family shell snippets.", True),
        Language("python", "Python", "A readable general-purpose language.", True),
        Language("php", "PHP", "A server-side language.", True),
        Language("go", "Go", "A compiled language.", True),
        Language("markdown", "Markdown", "A lightweight markup language.", True),
        Language("kotlin", "Kotlin", "A JVM language.", False),
        Language("objc", "Objective-C", "The older Apple language.", False),
        *extra,
    )
    return Catalogue(languages=rows)


def _snip(
    language: str,
    slug: str,
    *,
    tags: tuple[str, ...] = ("retry",),
    caveats: str | None = None,
    runnable: bool = False,
    added: datetime | None = None,
) -> Snippet:
    return Snippet(
        language=language,
        slug=slug,
        path=Path(f"snippets/{language}/{slug}.txt"),
        title=f"{slug} in {language}",
        card_title=slug,
        summary="A helper.",
        tags=tags,
        added=added or datetime(2026, 1, 1, tzinfo=UTC),
        submitted_by="Lupraxus",
        runnable=runnable,
        caveats=caveats,
        body="print(1)\n",
        extension=".txt",
    )


def test_snippet_page_includes_body() -> None:
    shell = _snip("shell", "retry", tags=("process", "retry"), caveats="Idempotent only.")
    md = render_snippet_page(shell)
    assert "# retry in shell" in md
    assert "Idempotent only." in md
    assert "```shell" in md
    assert "print(1)" in md
    assert "snippet:" not in md
    assert "## Related" not in md
    assert "data-snippet-article" in md
    assert "data-snippet-added" in md
    assert "data-snippet-submitted" in md
    assert "Added on: 1<sup>st</sup> January 2026" in md
    assert "Submitted by:" in md
    assert 'href="https://github.com/Lupraxus"' in md
    assert "1<sup>st</sup> January 2026" in md
    assert '!!! info "Caveats"' in md
    assert "Runnable" not in md


def test_snippet_page_date_uses_ordinal_suffix() -> None:
    eleventh = _snip(
        "shell",
        "eleventh",
        added=datetime(2026, 1, 11, tzinfo=UTC),
    )
    twenty_second = _snip(
        "shell",
        "twenty-second",
        added=datetime(2026, 1, 22, tzinfo=UTC),
    )
    twenty_third = _snip(
        "shell",
        "twenty-third",
        added=datetime(2026, 1, 23, tzinfo=UTC),
    )
    assert "11<sup>th</sup> January 2026" in render_snippet_page(eleventh)
    assert "22<sup>nd</sup> January 2026" in render_snippet_page(twenty_second)
    assert "23<sup>rd</sup> January 2026" in render_snippet_page(twenty_third)


def test_snippet_page_omits_caveats_block_when_empty() -> None:
    item = _snip("python", "tool", runnable=True)
    md = render_snippet_page(item)
    assert '!!! info "Caveats"' not in md
    assert "Runnable" not in md


def test_indexes() -> None:
    items = [_snip("shell", "retry"), _snip("python", "retry")]
    lang = render_language_index("shell", [items[0]])
    assert "[retry in shell](retry.md)" in lang
    langs = render_languages_index(items, _catalogue())
    assert not langs.startswith("# ")
    assert 'class="grid cards catalogue-grid catalogue-grid--languages"' in langs
    assert 'href="../snippets/?language=shell"' in langs
    assert 'href="../snippets/?language=python"' in langs
    assert 'href="../snippets/?language=php"' in langs
    assert 'href="../snippets/?language=go"' in langs
    assert 'href="../snippets/?language=markdown"' in langs
    assert "Shell" in langs
    assert "Python" in langs
    assert "PHP" in langs
    assert "Go" in langs
    assert "Markdown" in langs
    assert "Kotlin" not in langs
    assert 'src="../assets/images/languages/shell.png"' in langs
    assert 'src="../assets/images/languages/php.png"' in langs
    assert "Bourne-family" in langs
    assert "general-purpose" in langs
    assert "../shell/index.md" not in langs
    tags = render_tags_index({"retry": items})
    assert "[retry](retry.md)" in tags
    tag = render_tag_page("retry", items)
    assert "[retry in python](../python/retry.md)" in tag


def test_home_lists_snippets_not_repo_docs() -> None:
    items = [_snip("shell", "retry"), _snip("python", "retry")]
    md = render_home(items, _catalogue())
    assert 'class="lupaxa-hero"' in md
    assert 'class="lupaxa-hero-title"' in md
    assert 'src="assets/images/logo.png"' in md
    assert 'href="snippets/"' in md
    assert "Browse Snippets" in md
    assert 'href="languages/"' in md
    assert "Browse Languages" in md
    assert "reusable code snippets and helpers" in md
    assert 'href="tags/"' not in md
    assert "## Latest snippets" in md
    assert 'class="grid cards catalogue-grid catalogue-grid--latest"' in md
    assert 'href="shell/retry/" data-snippet-card' in md
    assert 'src="assets/images/languages/shell.png"' in md
    assert 'title="Shell"' in md
    assert "Getting started" not in md
    assert "end-snippet" not in md
    assert 'class="about-introduction"' not in md
    assert "Why “Lupaxa”" not in md
    assert 'class="about-name"' not in md


def test_catalogue_cards_have_title_mark_description_and_pills() -> None:
    items = [_snip("shell", "retry"), _snip("python", "retry")]
    md = render_catalogue(items, _catalogue())
    assert not md.startswith("# ")
    assert "Every snippet in one place" not in md
    assert "data-snippet-filters" in md
    assert "data-snippet-search" in md
    assert "data-snippet-language" in md
    assert "data-snippet-tag" in md
    assert 'data-snippet-sort="alpha"' in md
    assert 'data-snippet-sort="newest"' in md
    assert 'data-added="' in md
    assert "data-snippet-catalogue" in md
    assert "data-snippet-empty" in md
    assert 'class="grid cards catalogue-grid"' in md
    card = 'data-snippet-card data-full-title="retry in shell">retry</a>'
    assert f'href="../shell/retry/" {card}' in md
    assert 'src="../assets/images/languages/shell.png"' in md
    assert 'src="../assets/images/languages/python.png"' in md
    assert 'data-language="shell"' in md
    assert 'title="Shell"' in md
    assert 'title="Python"' in md
    assert "A helper." in md
    assert '<button type="button" class="catalogue-category">retry</button>' in md
    assert "catalogue-banner" not in md
    assert "View on GitHub" not in md
    assert "Documentation" not in md


def test_languages_index_is_alphabetical_by_name_not_yaml_order() -> None:
    catalogue = Catalogue(
        languages=(
            Language("python", "Python", "Scripts.", True),
            Language("rust", "Rust", "Systems.", True),
            Language("c", "C", "Systems.", True),
            Language("shell", "Shell", "POSIX.", True),
        )
    )
    md = render_languages_index([], catalogue)
    assert md.index("?language=c") < md.index("?language=python")
    assert md.index("?language=python") < md.index("?language=rust")
    assert md.index("?language=rust") < md.index("?language=shell")


def test_languages_index_lists_catalogue_languages() -> None:
    md = render_languages_index([], _catalogue())
    assert 'class="grid cards catalogue-grid catalogue-grid--languages"' in md
    assert 'href="../snippets/?language=php"' in md
    assert 'href="../snippets/?language=go"' in md
    assert 'href="../snippets/?language=markdown"' in md
    assert 'href="../snippets/?language=shell"' in md
    assert "Kotlin" not in md
    assert "No languages yet." not in md


def test_languages_index_includes_hidden_when_it_has_snippets() -> None:
    md = render_languages_index([_snip("kotlin", "flow")], _catalogue())
    assert 'href="../snippets/?language=kotlin"' in md
    assert "Kotlin" in md
    assert 'src="../assets/images/languages/kotlin.png"' in md


def test_languages_index_includes_unknown_scanned_language() -> None:
    md = render_languages_index([_snip("elixir", "pipe")], _catalogue())
    assert 'href="../snippets/?language=elixir"' in md
    assert "Elixir" in md
    assert 'src="../assets/images/languages/code.png"' in md


def test_filter_panel_embeds_language_labels() -> None:
    md = render_catalogue([_snip("python", "retry")], _catalogue())
    match = re.search(
        r'<template id="language-labels">(.*?)</template>',
        md,
        re.S,
    )
    assert match is not None
    labels = json.loads(match.group(1))
    assert labels["shell"] == "Shell"
    assert labels["kotlin"] == "Kotlin"
    assert labels["objc"] == "Objective-C"


def test_filter_panel_lists_visible_languages_without_snippets() -> None:
    md = render_catalogue([_snip("python", "retry")], _catalogue())
    match = re.search(
        r'<template id="listed-languages">(.*?)</template>',
        md,
        re.S,
    )
    assert match is not None
    listed = json.loads(match.group(1))
    assert listed == ["go", "markdown", "php", "python", "shell"]
    assert "kotlin" not in listed
    assert "objc" not in listed


def test_filter_panel_select_lists_visible_and_used_languages() -> None:
    md = render_catalogue(
        [_snip("python", "retry"), _snip("kotlin", "flow")],
        _catalogue(),
    )
    assert 'value="go">Go</option>' in md
    assert 'value="markdown">Markdown</option>' in md
    assert 'value="php">PHP</option>' in md
    assert 'value="python">Python</option>' in md
    assert 'value="shell">Shell</option>' in md
    assert 'value="kotlin">Kotlin</option>' in md
    assert 'value="objc"' not in md


def test_home_empty_catalogue() -> None:
    md = render_home([], _catalogue())
    assert 'class="lupaxa-hero"' in md
    assert "No snippets yet." in md
    assert "## Latest snippets" not in md
    assert 'href="snippets/"' not in md
    assert 'href="languages/"' not in md
    assert 'class="about-introduction"' not in md
    assert "Browse by tag" not in md
    assert "Browse Languages" not in md


def test_home_latest_cards_are_newest_first() -> None:
    older = _snip(
        "shell",
        "old",
        added=datetime(2026, 1, 1, tzinfo=UTC),
    )
    newer = _snip(
        "python",
        "new",
        added=datetime(2026, 8, 18, tzinfo=UTC),
    )
    md = render_home([older, newer], _catalogue())
    assert md.index("new in python") < md.index("old in shell")


def test_latest_snippets_are_newest_eight() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    items = [
        _snip("shell", f"s{index:02d}", added=start + timedelta(days=index)) for index in range(10)
    ]
    latest = latest_snippets(items)
    assert [item.slug for item in latest] == [
        "s09",
        "s08",
        "s07",
        "s06",
        "s05",
        "s04",
        "s03",
        "s02",
    ]
