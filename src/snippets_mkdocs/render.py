"""Render virtual Markdown pages for the catalogue."""

from __future__ import annotations

import json
from html import escape

from snippets_mkdocs.languages import (
    Catalogue,
    language_labels,
    language_mark_slug,
    language_profile,
    listed_slugs,
)
from snippets_mkdocs.models import Snippet


def fence_language(language: str) -> str:
    """Pygments hint is the language folder name."""
    return language


def _fence_ticks(body: str) -> str:
    """Use enough backticks so the body cannot close the fence."""
    longest = 0
    run = 0
    for char in body:
        if char == "`":
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return "`" * max(3, longest + 1)


def _markdown_fence(language: str, body: str) -> list[str]:
    ticks = _fence_ticks(body)
    return [f"{ticks}{language}", body.rstrip("\n"), ticks]


def _info_admonition(title: str, text: str) -> list[str]:
    lines = [f'!!! info "{title}"', ""]
    paragraphs = text.strip().splitlines() or [""]
    for line in paragraphs:
        lines.append(f"    {line}" if line else "    ")
    lines.append("")
    return lines


def render_snippet_page(snippet: Snippet) -> str:
    """Markdown for `/<language>/<slug>/` (also the modal source)."""
    lines = [
        f"# {snippet.title}",
        "",
        snippet.summary,
        "",
        '<div data-snippet-article markdown="1">',
        "",
        '<div class="snippet-modal-meta" data-snippet-meta>',
        f'<p class="snippet-modal-date" data-snippet-added>Added on: {_format_added(snippet)}</p>',
        _format_submitted_by(snippet),
        "</div>",
        "",
    ]
    lines.extend(_markdown_fence(fence_language(snippet.language), snippet.body))
    lines.append("")
    if snippet.caveats:
        lines.extend(_info_admonition("Caveats", snippet.caveats))
    lines.extend(["</div>", ""])
    return "\n".join(lines)


def _render_home_hero(*, actions: bool) -> list[str]:
    """Lupaxa hero block used on the catalogue home page."""
    lines = [
        '<div class="lupaxa-hero">',
        "    <img",
        '        class="lupaxa-hero-logo"',
        '        src="assets/images/logo.png"',
        '        alt="Snippets"/>',
        '    <h1 class="lupaxa-hero-title">',
        "        Snippets",
        "    </h1>",
        "",
        '    <p class="lupaxa-hero-subtitle">',
        "        A searchable catalogue of reusable code snippets and helpers,",
        "        organised by language and tags, providing developers with a",
        "        central place to discover practical examples, reusable utilities,",
        "        and ready-to-use solutions for common programming tasks and",
        "        everyday development workflows.",
        "    </p>",
    ]
    if actions:
        lines.extend(
            [
                "",
                '    <div class="lupaxa-hero-actions">',
                '        <a class="md-button lupaxa-button" href="snippets/">',
                "            Browse Snippets",
                "        </a>",
                '        <a class="md-button lupaxa-button" href="languages/">',
                "            Browse Languages",
                "        </a>",
                "    </div>",
            ]
        )
    lines.extend(["</div>", ""])
    return lines


HOME_LATEST_LIMIT = 8


def _day_ordinal_suffix(day: int) -> str:
    """English ordinal suffix for a calendar day (1st, 2nd, 3rd, 11th)."""
    if 10 <= day % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")


def _format_added(snippet: Snippet) -> str:
    """Human date for snippet metadata (day<sup>st</sup> Month year)."""
    added = snippet.added
    suffix = _day_ordinal_suffix(added.day)
    return f"{added.day}<sup>{suffix}</sup> {added.strftime('%B %Y')}"


def github_profile_url(userid: str) -> str:
    """Public GitHub profile for a userid."""
    return f"https://github.com/{userid}"


def _format_submitted_by(snippet: Snippet) -> str:
    """Modal/page line linking the submitter to their GitHub profile."""
    user = escape(snippet.submitted_by)
    href = escape(github_profile_url(snippet.submitted_by), quote=True)
    return (
        f'<p class="snippet-modal-submitted" data-snippet-submitted>'
        f'Submitted by: <a href="{href}" target="_blank" rel="noopener">{user}</a>'
        f"</p>"
    )


def latest_snippets(snippets: list[Snippet], *, limit: int = HOME_LATEST_LIMIT) -> list[Snippet]:
    """Newest snippets first, then title / language / slug."""
    return sorted(
        snippets,
        key=lambda item: (
            -item.added.timestamp(),
            item.card_title.casefold(),
            item.language,
            item.slug,
        ),
    )[:limit]


def render_home(snippets: list[Snippet], catalogue: Catalogue) -> str:
    """Markdown for the catalogue home page."""
    lines = _render_home_hero(actions=bool(snippets))
    if not snippets:
        lines.append("No snippets yet.")
        lines.append("")
        return "\n".join(lines)

    cards = "\n\n".join(
        render_catalogue_card(
            item,
            catalogue,
            mark_src=language_mark_src(item.language, catalogue, root=True),
            root=True,
        )
        for item in latest_snippets(snippets)
    )
    lines.extend(
        [
            "## Latest snippets",
            "",
            '<div class="grid cards catalogue-grid catalogue-grid--latest" markdown>',
            "",
            cards,
            "",
            "</div>",
            "",
        ]
    )
    return "\n".join(lines)


def snippet_page_href(snippet: Snippet, *, root: bool = False) -> str:
    """Directory URL for a snippet page, relative to Home or Snippets."""
    path = f"{snippet.language}/{snippet.slug}/"
    return path if root else f"../{path}"


def language_mark_src(language: str, catalogue: Catalogue, *, root: bool = False) -> str:
    """Relative path to the language mark used on snippet cards."""
    slug = language_mark_slug(catalogue, language)
    prefix = "assets/images/languages" if root else "../assets/images/languages"
    return f"{prefix}/{slug}.png"


def _md_label(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


# Material filter-variant / filter-off icons for Show / Hide Filters.
_FILTER_EXPAND_ICONS = """\
<span class="filter-panel-expand__icon filter-panel-expand__icon--show" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" focusable="false">
                <path d="M6 13h12v-2H6m-3-5v2h18V6M10 18h4v-2h-4v2Z"/>
            </svg>
        </span>
        <span class="filter-panel-expand__icon filter-panel-expand__icon--hide" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" focusable="false">
                <path d="M14.76 20.83 17.6 18l-2.84-2.83 1.41-1.41L19 16.57l2.83-2.81 1.41 1.41
L20.41 18l2.83 2.83-1.41 1.41L19 19.41l-2.83 2.83-1.41-1.41
M6 13h7.07c.14-.71.4-1.38.76-2H6m-3-5v2h18V6H3Z"/>
            </svg>
        </span>"""


def render_filter_panel(catalogue: Catalogue, snippets: list[Snippet]) -> str:
    """Projects-page filter box: search, language, tag, A–Z/Newest, clear."""
    labels = json.dumps(language_labels(catalogue), separators=(",", ":"))
    listed = json.dumps(listed_slugs(catalogue, snippets), separators=(",", ":"))
    return f"""
<div class="filter-panel filter-panel--with-sort" data-snippet-filters>
    <script type="application/json" id="language-labels">{labels}</script>
    <script type="application/json" id="listed-languages">{listed}</script>
    <div class="filter-panel-toolbar">
        <button
            type="button"
            class="md-button lupaxa-button filter-panel-expand"
            data-filter-expand
            aria-expanded="false"
        >
            {_FILTER_EXPAND_ICONS}
            <span class="filter-panel-expand__label">Show Filters</span>
        </button>
        <div
            class="filter-panel-summary"
            aria-live="polite"
            data-snippet-summary
        >
            Showing…
        </div>
    </div>
    <div class="filter-panel-search">
        <label for="snippet-search">Search snippets</label>
        <input
            id="snippet-search"
            type="search"
            placeholder="Search by title, description, language, or tag..."
            autocomplete="off"
            data-snippet-search
        />
    </div>
    <div class="filter-panel-select">
        <label for="snippet-language">Language</label>
        <select id="snippet-language" data-snippet-language>
            <option value="">All Languages</option>
        </select>
    </div>
    <div class="filter-panel-select">
        <label for="snippet-tag">Tag</label>
        <select id="snippet-tag" data-snippet-tag>
            <option value="">All Tags</option>
        </select>
    </div>
    <div class="filter-panel-toggle" role="group" aria-labelledby="snippet-sort-label">
        <label id="snippet-sort-label">Sort</label>
        <div class="filter-panel-toggle__options">
            <button
                type="button"
                class="filter-panel-toggle__option"
                data-snippet-sort="alpha"
                aria-pressed="true"
            >
                A–Z
            </button>
            <button
                type="button"
                class="filter-panel-toggle__option"
                data-snippet-sort="newest"
                aria-pressed="false"
            >
                Newest
            </button>
        </div>
    </div>
    <div class="filter-panel-actions">
        <button
            type="button"
            class="md-button lupaxa-button filter-panel-clear"
            data-snippet-clear
        >
            Clear filters
        </button>
    </div>
</div>
""".strip()


def render_catalogue_empty() -> str:
    """Empty state shown when filters match no snippet cards."""
    return """
<div class="catalogue-empty-state" data-snippet-empty hidden markdown>

**No matching snippets**

Try changing the search text or selecting different filters.

</div>
""".strip()


def render_catalogue_card(
    snippet: Snippet,
    catalogue: Catalogue,
    *,
    mark_src: str | None = None,
    root: bool = False,
) -> str:
    """One Material catalogue card for a snippet."""
    summary = escape(snippet.summary)
    language = escape(snippet.language)
    language_name = escape(language_profile(catalogue, snippet.language)[0], quote=True)
    mark = mark_src if mark_src is not None else language_mark_src(snippet.language, catalogue)
    pills = "\n".join(
        f'    <button type="button" class="catalogue-category">{escape(tag)}</button>'
        for tag in snippet.tags
    )
    href = snippet_page_href(snippet, root=root)
    card_html = escape(snippet.card_title)
    full_title = escape(snippet.title, quote=True)
    logo = f"""<img
        class="catalogue-logo"
        src="{mark}"
        alt="{language_name}"
        title="{language_name}"
        data-language="{language}"
        data-added="{escape(snippet.added.isoformat(), quote=True)}"
    />"""
    if root:
        logo = f"<span>\n        {logo}\n    </span>"
    return f"""
-   **<a href="{href}" data-snippet-card data-full-title="{full_title}">{card_html}</a>**

    ---

    {logo}

    {summary}

{pills}
""".strip()


def render_catalogue(snippets: list[Snippet], catalogue: Catalogue) -> str:
    """Markdown for the Snippets page."""
    if not snippets:
        return "No snippets yet.\n"

    cards = "\n\n".join(
        render_catalogue_card(item, catalogue)
        for item in sorted(
            snippets, key=lambda snip: (snip.card_title.casefold(), snip.language, snip.slug)
        )
    )
    return "\n".join(
        [
            render_filter_panel(catalogue, snippets),
            "",
            '<div class="grid cards catalogue-grid" data-snippet-catalogue markdown>',
            "",
            cards,
            "",
            "</div>",
            "",
            render_catalogue_empty(),
            "",
        ]
    )


def render_language_card(language: str, catalogue: Catalogue) -> str:
    """One organisations-style card that opens Snippets filtered by language."""
    name, description = language_profile(catalogue, language)
    title = _md_label(name)
    slug = escape(language, quote=True)
    mark = language_mark_src(language, catalogue)
    name_attr = escape(name, quote=True)
    return f"""
-   **<a href="../snippets/?language={slug}">{title}</a>**

    ---

    <a href="../snippets/?language={slug}">
        <img
            class="catalogue-logo"
            src="{mark}"
            alt="{name_attr}"
        />
    </a>

    {escape(description)}
""".strip()


def catalogue_languages(snippets: list[Snippet], catalogue: Catalogue) -> list[str]:
    """Visible catalogue languages plus any extra folders that already have snippets."""
    return listed_slugs(catalogue, snippets)


def render_languages_index(snippets: list[Snippet], catalogue: Catalogue) -> str:
    """Markdown for the Languages page."""
    languages = catalogue_languages(snippets, catalogue)
    cards = "\n\n".join(render_language_card(language, catalogue) for language in languages)
    return "\n".join(
        [
            '<div class="grid cards catalogue-grid catalogue-grid--languages" markdown>',
            "",
            cards,
            "",
            "</div>",
            "",
        ]
    )


def render_language_index(language: str, snippets: list[Snippet]) -> str:
    """Markdown for `/<language>/`."""
    lines = [f"# {language.capitalize()}", ""]
    for item in sorted(snippets, key=lambda snip: snip.slug):
        lines.append(f"- [{item.title}]({item.slug}.md) — {item.summary}")
    lines.append("")
    return "\n".join(lines)


def render_tags_index(tag_map: dict[str, list[Snippet]]) -> str:
    """Markdown for `/tags/`."""
    lines = ["# Tags", ""]
    for tag in sorted(tag_map):
        count = len(tag_map[tag])
        lines.append(f"- [{tag}]({tag}.md) ({count})")
    lines.append("")
    return "\n".join(lines)


def render_tag_page(tag: str, snippets: list[Snippet]) -> str:
    """Markdown for `/tags/<tag>/`."""
    lines = [f"# {tag}", ""]
    for item in sorted(snippets, key=lambda snip: (snip.language, snip.slug)):
        lines.append(f"- [{item.title}](../{item.language}/{item.slug}.md) (`{item.language}`)")
    lines.append("")
    return "\n".join(lines)
